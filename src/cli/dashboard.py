import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]


def export_dashboard_snapshot(snapshot: dict) -> Path:
    out_dir = BASE / "artifacts"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "dashboard-latest.json"
    out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
