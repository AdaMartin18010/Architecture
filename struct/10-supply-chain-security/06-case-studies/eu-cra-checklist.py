#!/usr/bin/env python3
"""EU Cyber Resilience Act (CRA) Compliance Checklist Tool.

Assesses software product compliance against EU CRA (EU) 2024/2847.
"""

import argparse
import json
import sys
from pathlib import Path

CHECKLIST_PATH = Path(__file__).with_suffix(".json")

ANSWER_MAP = {
    "y": "satisfied",
    "yes": "satisfied",
    "n": "not-satisfied",
    "no": "not-satisfied",
    "p": "partially-satisfied",
    "partial": "partially-satisfied",
    "na": "not-applicable",
    "not-applicable": "not-applicable",
    "": "not-satisfied",
}

ANSWER_LABELS = {
    "satisfied": "✅ Satisfied",
    "partially-satisfied": "⚠️  Partially Satisfied",
    "not-satisfied": "❌ Not Satisfied",
    "not-applicable": "➖ Not Applicable",
}

SEVERITY_SCORE = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def load_checklist(path: Path = CHECKLIST_PATH):
    if not path.exists():
        print(f"Checklist not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def score_color(rate: float) -> str:
    if rate >= 0.9:
        return "\033[92m"
    if rate >= 0.7:
        return "\033[93m"
    return "\033[91m"


def reset() -> str:
    return "\033[0m"


def assess_interactive(checklist: dict):
    answers = {}
    print("=== EU CRA Compliance Assessment ===\n")
    print("Answer: y=yes, n=no, p=partial, na=not-applicable\n")
    for annex_key, annex in checklist.get("annexes", {}).items():
        print(f"-- {annex['title']} --")
        for item in annex.get("items", []):
            prompt = f"[{item['id']}] {item['description']} (severity: {item['severity']}) [y/n/p/na]: "
            while True:
                raw = input(prompt).strip().lower()
                ans = ANSWER_MAP.get(raw)
                if ans:
                    answers[item["id"]] = {
                        "answer": ans,
                        "severity": item["severity"],
                        "description": item["description"],
                        "annex": annex_key,
                    }
                    break
                print("  Invalid input. Use y, n, p, or na.")
        print()
    return answers


def assess_from_input(checklist: dict, input_path: Path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    answers = {}
    lookup = {}
    for annex_key, annex in checklist.get("annexes", {}).items():
        for item in annex.get("items", []):
            lookup[item["id"]] = {
                "severity": item["severity"],
                "description": item["description"],
                "annex": annex_key,
            }
    for qid, val in data.items():
        if qid not in lookup:
            print(f"Warning: unknown question {qid}", file=sys.stderr)
            continue
        ans = ANSWER_MAP.get(str(val).strip().lower(), "not-satisfied")
        answers[qid] = {"answer": ans, **lookup[qid]}
    return answers


def calculate_metrics(answers: dict):
    total = len(answers)
    if total == 0:
        return {}, 0.0, "unknown"
    applicable = {k: v for k, v in answers.items() if v["answer"] != "not-applicable"}
    app_total = len(applicable)
    satisfied = sum(1 for v in applicable.values() if v["answer"] == "satisfied")
    partial = sum(1 for v in applicable.values() if v["answer"] == "partially-satisfied")
    score = satisfied + (partial * 0.5)
    rate = score / app_total if app_total else 0.0
    risk = "Low"
    if rate < 0.5:
        risk = "Critical"
    elif rate < 0.7:
        risk = "High"
    elif rate < 0.9:
        risk = "Medium"
    return applicable, rate, risk


def print_terminal_report(answers: dict):
    applicable, rate, risk = calculate_metrics(answers)
    app_total = len(applicable)
    satisfied = sum(1 for v in applicable.values() if v["answer"] == "satisfied")
    partial = sum(1 for v in applicable.values() if v["answer"] == "partially-satisfied")
    not_sat = sum(1 for v in applicable.values() if v["answer"] == "not-satisfied")
    na_total = len(answers) - app_total

    color = score_color(rate)
    print("\n========== EU CRA Compliance Report ==========")
    print(f"Overall Compliance Rate: {color}{rate:.1%}{reset()}")
    print(f"Risk Level: {color}{risk}{reset()}")
    print(f"  Total questions     : {len(answers)}")
    print(f"  Applicable          : {app_total}")
    print(f"  Satisfied           : {satisfied}")
    print(f"  Partially Satisfied : {partial}")
    print(f"  Not Satisfied       : {not_sat}")
    print(f"  Not Applicable      : {na_total}")
    print("\n-- Non-Compliant Items --")
    for qid, v in applicable.items():
        if v["answer"] != "satisfied":
            label = ANSWER_LABELS[v["answer"]]
            print(f"  {qid} [{v['severity'].upper()}] {label}")
            print(f"      {v['description']}")
    print("==============================================\n")


def generate_json_report(answers: dict, out_path: Path):
    applicable, rate, risk = calculate_metrics(answers)
    report = {
        "regulation": "EU Cyber Resilience Act (EU) 2024/2847",
        "compliance_rate": round(rate, 4),
        "risk_level": risk,
        "summary": {
            "total": len(answers),
            "applicable": len(applicable),
            "satisfied": sum(1 for v in applicable.values() if v["answer"] == "satisfied"),
            "partially_satisfied": sum(1 for v in applicable.values() if v["answer"] == "partially-satisfied"),
            "not_satisfied": sum(1 for v in applicable.values() if v["answer"] == "not-satisfied"),
            "not_applicable": len(answers) - len(applicable),
        },
        "details": answers,
    }
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON report written to {out_path.resolve()}")


def generate_markdown_report(answers: dict, out_path: Path):
    applicable, rate, risk = calculate_metrics(answers)
    lines = [
        "# EU CRA Compliance Declaration",
        "",
        f"> **Regulation**: EU Cyber Resilience Act (EU) 2024/2847  ",
        f"> **Assessment Date**: Auto-generated  ",
        f"> **Compliance Rate**: {rate:.1%}  ",
        f"> **Risk Level**: {risk}  ",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(answers)}",
        f"- Applicable: {len(applicable)}",
        f"- Satisfied: {sum(1 for v in applicable.values() if v['answer'] == 'satisfied')}",
        f"- Partially Satisfied: {sum(1 for v in applicable.values() if v['answer'] == 'partially-satisfied')}",
        f"- Not Satisfied: {sum(1 for v in applicable.values() if v['answer'] == 'not-satisfied')}",
        f"- Not Applicable: {len(answers) - len(applicable)}",
        "",
        "## Detail",
        "",
        "| ID | Annex | Severity | Status | Description |",
        "|---|---|---|---|---|",
    ]
    for qid, v in answers.items():
        status = ANSWER_LABELS[v["answer"]]
        lines.append(f"| {qid} | {v['annex']} | {v['severity']} | {status} | {v['description']} |")
    lines.append("")
    lines.append("---")
    lines.append("*This declaration is generated for internal governance and should be reviewed by legal/compliance teams before external submission.*")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown report written to {out_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="EU CRA Compliance Checklist Tool")
    sub = parser.add_subparsers(dest="command", required=True)

    assess_parser = sub.add_parser("assess", help="Run compliance assessment")
    assess_parser.add_argument("--interactive", action="store_true", help="Interactive Q&A mode")
    assess_parser.add_argument("--input", type=Path, help="Read answers from JSON file")
    assess_parser.add_argument("--output", type=Path, default=Path("cra-answers.json"), help="Save answers JSON")

    report_parser = sub.add_parser("report", help="Generate report from saved answers")
    report_parser.add_argument("--input", type=Path, default=Path("cra-answers.json"), help="Input answers JSON")
    report_parser.add_argument("--format", choices=["json", "markdown"], required=True)
    report_parser.add_argument("--output", type=Path, help="Output file path")

    args = parser.parse_args()
    checklist = load_checklist()

    if args.command == "assess":
        if args.interactive:
            answers = assess_interactive(checklist)
        elif args.input:
            answers = assess_from_input(checklist, args.input)
        else:
            print("Use --interactive or --input <file>", file=sys.stderr)
            sys.exit(1)
        args.output.write_text(json.dumps(answers, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nAnswers saved to {args.output.resolve()}")
        print_terminal_report(answers)
    elif args.command == "report":
        if not args.input.exists():
            print(f"Input not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        answers = json.loads(args.input.read_text(encoding="utf-8"))
        if args.format == "json":
            out = args.output or Path("cra-report.json")
            generate_json_report(answers, out)
        else:
            out = args.output or Path("cra-report.md")
            generate_markdown_report(answers, out)


if __name__ == "__main__":
    main()
