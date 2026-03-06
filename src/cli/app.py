from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.cli.dashboard import export_dashboard_snapshot
from src.core.pipeline import AnalysisPipeline
from src.detectors.command_abuse import CommandAbuseDetector
from src.detectors.exfiltration import ExfiltrationDetector
from src.detectors.prompt_injection import PromptInjectionDetector
from src.reporting.markdown_report import write_markdown_report
from src.storage.events import append_event_jsonl


def build_pipeline() -> AnalysisPipeline:
    return AnalysisPipeline(
        detectors=[
            PromptInjectionDetector(weight=0.9),
            ExfiltrationDetector(weight=1.0),
            CommandAbuseDetector(weight=0.9),
        ]
    )


def cmd_analyze_text(args: argparse.Namespace) -> int:
    pipeline = build_pipeline()
    result = pipeline.analyze_text(args.text, tool=args.tool, action=args.action)
    data = pipeline.to_dict(result)
    print(json.dumps(data, ensure_ascii=False, indent=2))

    export_dashboard_snapshot(data)
    if args.log_jsonl:
        append_event_jsonl(Path(args.log_jsonl), data)
    return 0


def cmd_analyze_file(args: argparse.Namespace) -> int:
    p = Path(args.path)
    text = p.read_text(encoding="utf-8", errors="ignore")
    return cmd_analyze_text(argparse.Namespace(text=text, tool=args.tool, action=args.action, log_jsonl=args.log_jsonl))


def cmd_batch(args: argparse.Namespace) -> int:
    pipeline = build_pipeline()
    inp = Path(args.input)
    lines = [x.strip() for x in inp.read_text(encoding="utf-8", errors="ignore").splitlines() if x.strip()]
    rows: list[dict] = []

    for t in lines:
        result = pipeline.analyze_text(t, tool=args.tool, action=args.action)
        d = pipeline.to_dict(result)
        rows.append(d)
        if args.log_jsonl:
            append_event_jsonl(Path(args.log_jsonl), d)

    out_json = Path(args.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.output_md:
        write_markdown_report(Path(args.output_md), "Batch Risk Report", rows)

    print(json.dumps({"processed": len(rows), "output_json": str(out_json)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Security Lab CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_text = sub.add_parser("analyze-text", help="Analyze one text")
    p_text.add_argument("text")
    p_text.add_argument("--tool", default="read")
    p_text.add_argument("--action", default="analyze")
    p_text.add_argument("--log-jsonl", default="")
    p_text.set_defaults(func=cmd_analyze_text)

    p_file = sub.add_parser("analyze-file", help="Analyze one text file")
    p_file.add_argument("path")
    p_file.add_argument("--tool", default="read")
    p_file.add_argument("--action", default="analyze")
    p_file.add_argument("--log-jsonl", default="")
    p_file.set_defaults(func=cmd_analyze_file)

    p_batch = sub.add_parser("batch", help="Analyze line-by-line batch input")
    p_batch.add_argument("input", help="txt file, one prompt per line")
    p_batch.add_argument("--tool", default="read")
    p_batch.add_argument("--action", default="analyze")
    p_batch.add_argument("--log-jsonl", default="")
    p_batch.add_argument("--output-json", default="artifacts/batch-output.json")
    p_batch.add_argument("--output-md", default="artifacts/batch-report.md")
    p_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
