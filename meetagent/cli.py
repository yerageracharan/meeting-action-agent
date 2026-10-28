"""CLI entry point for Meeting Action Agent."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import AgentOutputError, analyze_notes
from .provider import ModelError
from .render import save_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Turn meeting notes into an evidence-backed action plan.")
    parser.add_argument("notes", help="Path to a UTF-8 .txt file containing meeting notes")
    parser.add_argument("--out", default="output/action_plan.md", help="Markdown report path (default: output/action_plan.md)")
    args = parser.parse_args(argv)
    path = Path(args.notes)
    try:
        notes = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Could not read {path}: {exc}", file=sys.stderr)
        return 2
    try:
        data = analyze_notes(notes)
        report = save_report(data, args.out)
    except (ValueError, ModelError, AgentOutputError) as exc:
        print(f"Meeting Action Agent: {exc}", file=sys.stderr)
        return 1
    print(f"Action plan saved to: {report}")
    print(f"JSON data saved to: {report.with_suffix('.json')}")
    print(f"Action items: {len(data['action_items'])}; needs clarification: {sum(x['status'] == 'needs_clarification' for x in data['action_items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
