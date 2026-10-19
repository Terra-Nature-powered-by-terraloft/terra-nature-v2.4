"""DAT-01 v1: deterministic CSV validation and auditable imports (SQLite prototype).
Production PostgreSQL INSERT-only role and object-storage policies require deployment setup.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

LIMITS = Path(__file__).with_name("limits.v1.json")
HEADER = ("timestamp", "temperature [°C]", "power [kW]")
DECIMAL = re.compile(r"^-?\d+(?:,\d+)?$")
TZ = re.compile(r"(Z|[+-]\d{2}:\d{2})$")

class ValidationError(ValueError):
    pass

def validate_csv(raw: bytes, config_path: Path = LIMITS) -> tuple[list[dict], str]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("invalid_encoding") from exc
    if not text.strip():
        raise ValidationError("empty_file")
    if ";" not in text.splitlines()[0]:
        raise ValidationError("invalid_delimiter")
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter=";", strict=True)
    if reader.fieldnames is None:
        raise ValidationError("missing_header")
    if tuple(reader.fieldnames) != HEADER:
        if any("[" not in h or "]" not in h for h in reader.fieldnames[1:]):
            raise ValidationError("missing_unit")
        raise ValidationError("unknown_unit_or_header")
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    rows, previous = [], None
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise ValidationError("invalid_column_count")
        stamp = row["timestamp"].strip()
        if not TZ.search(stamp):
            raise ValidationError("missing_or_invalid_timezone")
        try:
            dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValidationError("invalid_timestamp") from exc
        if dt.utcoffset() is None:
            raise ValidationError("missing_or_invalid_timezone")
        instant = dt.timestamp()
        if previous is not None and instant == previous:
            raise ValidationError("duplicate_timestamp")
        if previous is not None and instant < previous:
            raise ValidationError("non_monotonic_timestamp")
        previous = instant
        parsed = {"timestamp": dt.isoformat()}
        for col, key in (("temperature [°C]", "temperature_c"), ("power [kW]", "power_kw")):
            token = row[col].strip()
            if not DECIMAL.fullmatch(token):
                raise ValidationError("invalid_decimal_format")
            value = float(token.replace(",", "."))
            bounds = cfg["measurements"][key]
            if not bounds["min"] <= value <= bounds["max"]:
                raise ValidationError("outside_plausibility_limits")
            parsed[key] = value
        rows.append(parsed)
    if not rows:
        raise ValidationError("empty_file")
    return rows, cfg["version"]

def _hash(previous: str, payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256((previous + canonical).encode("utf-8")).hexdigest()

def initialize(db: sqlite3.Connection) -> None:
    db.execute("CREATE TABLE IF NOT EXISTS imports (sha256 TEXT PRIMARY KEY, source TEXT NOT NULL, config_version TEXT NOT NULL, status TEXT NOT NULL CHECK(status='pending'), payload TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY AUTOINCREMENT, previous_hash TEXT NOT NULL, payload TEXT NOT NULL, entry_hash TEXT NOT NULL)")
    db.execute("CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit BEGIN SELECT RAISE(ABORT, 'append_only'); END")
    db.execute("CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit BEGIN SELECT RAISE(ABORT, 'append_only'); END")
    db.commit()

def import_csv(db: sqlite3.Connection, raw: bytes, source: str) -> dict:
    rows, version = validate_csv(raw)
    digest = hashlib.sha256(raw).hexdigest()
    with db:
        exists = db.execute("SELECT 1 FROM imports WHERE sha256=?", (digest,)).fetchone() is not None
        if not exists:
            db.execute("INSERT INTO imports VALUES (?,?,?,?,?)", (digest, source, version, "pending", json.dumps(rows)))
        previous_row = db.execute("SELECT entry_hash FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
        previous = previous_row[0] if previous_row else "0" * 64
        payload = {"action": "duplicate_import" if exists else "import", "sha256": digest, "source": source, "config_version": version}
        db.execute("INSERT INTO audit (previous_hash,payload,entry_hash) VALUES (?,?,?)", (previous, json.dumps(payload, sort_keys=True), _hash(previous, payload)))
    return {"sha256": digest, "duplicate": exists, "status": "pending"}

def verify_chain(db: sqlite3.Connection) -> bool:
    previous = "0" * 64
    for prev, raw, digest in db.execute("SELECT previous_hash,payload,entry_hash FROM audit ORDER BY seq"):
        if prev != previous or _hash(prev, json.loads(raw)) != digest:
            return False
        previous = digest
    return True
