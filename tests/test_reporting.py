from pathlib import Path

from src.reporting.markdown_report import render_markdown_report


def test_render_markdown_report():
    md = render_markdown_report(
        "Demo",
        [
            {"overall": {"level": "low", "score": 0.1}, "policy": {"decision": "allow"}},
            {"overall": {"level": "high", "score": 0.8}, "policy": {"decision": "require_approval"}},
        ],
    )
    assert "| idx | level | score | decision |" in md
    assert "Demo" in md
