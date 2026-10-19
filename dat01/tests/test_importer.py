import sqlite3
import pytest
from dat01.importer import ValidationError, validate_csv, initialize, import_csv, verify_chain

GOOD = "timestamp;temperature [°C];power [kW]\n2026-01-01T00:00:00+00:00;155,5;430,0\n2026-01-01T00:10:00+00:00;160,0;440,0\n"

@pytest.mark.parametrize("raw,reason", [
    (GOOD.replace(";", ","), "invalid_delimiter"),
    (GOOD.replace("155,5", "155.5"), "invalid_decimal_format"),
    (GOOD.replace("temperature [°C]", "temperature"), "missing_unit"),
    (GOOD.replace("temperature [°C]", "temperature [F]"), "unknown_unit_or_header"),
    (GOOD.replace("00:10:00", "00:00:00").replace("00:00:00+00:00;160", "00:00:01+00:00;160"), "non_monotonic_timestamp"),
    (GOOD.replace("00:10:00", "00:00:00"), "duplicate_timestamp"),
    (GOOD.replace("+00:00", ""), "missing_or_invalid_timezone"),
    (GOOD.replace("155,5", "1500,0"), "outside_plausibility_limits"),
    ("", "empty_file"),
    (b"\xff\xfe", "invalid_encoding"),
])
def test_invalid(raw, reason):
    with pytest.raises(ValidationError, match=reason):
        validate_csv(raw if isinstance(raw, bytes) else raw.encode("utf-8"))

def test_import_duplicate_and_tamper_detection():
    db = sqlite3.connect(":memory:")
    initialize(db)
    first = import_csv(db, GOOD.encode(), "synthetic.csv")
    second = import_csv(db, GOOD.encode(), "synthetic.csv")
    assert not first["duplicate"] and second["duplicate"]
    assert db.execute("SELECT COUNT(*) FROM imports").fetchone()[0] == 1
    assert db.execute("SELECT COUNT(*) FROM audit").fetchone()[0] == 2
    assert verify_chain(db)
    with pytest.raises(sqlite3.DatabaseError):
        db.execute("UPDATE audit SET payload='x' WHERE seq=1")
    db.execute("DROP TRIGGER audit_no_update")
    db.execute("UPDATE audit SET payload='{}' WHERE seq=1")
    assert not verify_chain(db)
