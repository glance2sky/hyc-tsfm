from __future__ import annotations

import argparse
from datetime import datetime

from _common import REPORTS_DIR, ensure_dirs


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a geometry diagnostics report stub.")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    ensure_dirs()
    dataset = args.dataset.lower()
    path = REPORTS_DIR / f"geometry_{dataset}.md"
    text = f"""# Geometry Report: {dataset}

- generated_at: `{datetime.now().isoformat(timespec="seconds")}`
- status: `stub`

## Required Diagnostics

- dependency graph construction method
- degree distribution
- clustering coefficient
- tree-likeness
- sampled Gromov hyperbolicity
- Euclidean embedding distortion
- hyperbolic embedding distortion
- HyC gain vs geometry metrics

## Notes

This is a harness placeholder. Do not claim that HyC works because of hyperbolic geometry until this report is populated with real diagnostics.
"""
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()

