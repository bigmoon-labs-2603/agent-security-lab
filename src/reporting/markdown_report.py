from __future__ import annotations

from pathlib import Path


def render_markdown_report(title: str, rows: list[dict]) -> str:
    lines = [f"# {title}", "", "| idx | level | score | decision |", "|---:|---|---:|---|"]
    for i, row in enumerate(rows, start=1):
        overall = row.get("overall", {})
        policy = row.get("policy", {})
        lines.append(
            f"| {i} | {overall.get('level','n/a')} | {overall.get('score','n/a')} | {policy.get('decision','n/a')} |"
        )
    return "\n".join(lines) + "\n"


def write_markdown_report(path: Path, title: str, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(title, rows), encoding="utf-8")
    return path
