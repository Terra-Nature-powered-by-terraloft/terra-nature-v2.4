import csv
from pathlib import Path

REQUIRED_COLUMNS = ["timestamp", "id", "energy_kwh", "co2_kg", "miner", "proof"]


def test_template_has_required_columns():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "nrg_nft_events_template.csv"
    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == REQUIRED_COLUMNS
        rows = list(reader)
    assert rows, "Template should contain at least one sample row"
    for row in rows:
        assert set(row.keys()) == set(REQUIRED_COLUMNS)
