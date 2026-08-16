from __future__ import annotations

import argparse
from pathlib import Path

from ruleshield.pipeline import run_pipeline
from ruleshield.report_generator import generate_report


def main() -> int:
    parser = argparse.ArgumentParser(description="RuleShield: educational automata-based NGINX access-control validator")
    parser.add_argument("config", help="Path to a simplified NGINX configuration file")
    parser.add_argument("--trace", action="store_true", help="Print model traces")
    parser.add_argument("--policy-ip", default=None)
    parser.add_argument("--policy-path", default="/")
    parser.add_argument("--policy-port", type=int, default=80)
    args = parser.parse_args()

    text = Path(args.config).read_text(encoding="utf-8")
    policy = {"client_ip": args.policy_ip, "path": args.policy_path, "port": args.policy_port} if args.policy_ip else None
    data = run_pipeline(text, policy)
    generate_report(data, text)
    final = data["final"]
    print("ACCEPT" if final.accepted else "REJECT")
    print(final.message)
    for result in data["results"]:
        status = "ACCEPT" if result.accepted else "REJECT"
        extra = f" ({result.error_code})" if result.error_code else ""
        print(f"{result.model_name}: {status}{extra}")
        if args.trace:
            for line in result.trace:
                print(f"  {line}")
    if data.get("policy"):
        print(data["policy"].message)
    print("Report written to output/validation_report.md")
    return 0 if final.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
