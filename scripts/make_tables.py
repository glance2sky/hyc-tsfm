from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _common import RESULTS_DIR, ensure_dirs


RESULTS_JSONL = RESULTS_DIR / "experiments.jsonl"
MAIN_TABLE = RESULTS_DIR / "main_table.md"


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def main() -> None:
    ensure_dirs()
    if not RESULTS_JSONL.exists():
        MAIN_TABLE.write_text("# Main Table\n\nNo experiments recorded yet.\n", encoding="utf-8")
        print(f"Wrote {MAIN_TABLE}")
        return

    rows = []
    with RESULTS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    headers = [
        "run_id",
        "branch",
        "status",
        "dataset",
        "horizon",
        "backbone",
        "adapter",
        "seed",
        "mse",
        "mae",
        "peak_vram_gb",
        "trainable_params_m",
        "training_minutes",
    ]
    lines = ["# Main Table", "", "| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(header)) for header in headers) + " |")
    lines.append("")
    lines.append("> Preliminary/debug runs must not be used for main scientific claims without matching baselines and required seeds.")
    MAIN_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {MAIN_TABLE}")


if __name__ == "__main__":
    main()
