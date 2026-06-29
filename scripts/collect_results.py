from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from _common import ALLOWED_STATUS, RESULTS_DIR, RUNS_DIR, append_jsonl, ensure_dirs, read_json


RESULTS_JSONL = RESULTS_DIR / "experiments.jsonl"


def existing_run_ids() -> set[str]:
    if not RESULTS_JSONL.exists():
        return set()
    ids = set()
    with RESULTS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                ids.add(str(item.get("run_id")))
            except json.JSONDecodeError:
                continue
    return ids


def append_run(run_id: str, force: bool = False) -> None:
    metrics_path = RUNS_DIR / run_id / "metrics.json"
    if not metrics_path.exists():
        raise SystemExit(f"metrics.json not found for run_id={run_id}")
    item = read_json(metrics_path)
    status = item.get("status")
    if status not in ALLOWED_STATUS:
        raise SystemExit(f"Invalid status {status!r}; allowed: {sorted(ALLOWED_STATUS)}")
    ids = existing_run_ids()
    if run_id in ids and not force:
        raise SystemExit(f"run_id={run_id} already exists in results; use --force to append anyway")
    append_jsonl(RESULTS_JSONL, item)
    print(f"Appended {run_id} to {RESULTS_JSONL}")


def print_summary() -> None:
    if not RESULTS_JSONL.exists():
        print("No results/experiments.jsonl yet.")
        return
    rows = []
    with RESULTS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    print(f"total_runs: {len(rows)}")
    print("status_counts:", dict(Counter(row.get("status") for row in rows)))
    print("stage_counts:", dict(Counter(str(row.get("stage")) for row in rows)))
    if rows:
        last = rows[-1]
        print("last_run:", last.get("run_id"), last.get("status"), last.get("dataset"), last.get("adapter"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect run metrics into results/experiments.jsonl")
    parser.add_argument("--run-id", help="Run id to append")
    parser.add_argument("--force", action="store_true", help="Allow duplicate append")
    parser.add_argument("--summary", action="store_true", help="Print result summary")
    args = parser.parse_args()

    ensure_dirs()
    if args.run_id:
        append_run(args.run_id, force=args.force)
    if args.summary or not args.run_id:
        print_summary()


if __name__ == "__main__":
    main()

