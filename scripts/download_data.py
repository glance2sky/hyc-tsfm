from __future__ import annotations

import argparse
from datetime import datetime

from _common import REPORTS_DIR, ROOT, ensure_dirs


KNOWN_DATASETS = {
    "ett": "ETT benchmark family; later map to ETTm1/ETTm2/ETTh1/ETTh2.",
    "weather": "Multivariate weather benchmark.",
    "electricity": "Electricity load benchmark with optional calendar/weather covariates.",
    "traffic": "Traffic or PEMS-style sensor data.",
    "solar": "Solar-energy multivariate benchmark.",
    "m5": "M5 hierarchy subset.",
    "smoke": "Synthetic harness-only dataset.",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Register or later download dataset requirements.")
    parser.add_argument("--dataset", required=True, help="Dataset name, e.g. electricity")
    parser.add_argument("--source", default="", help="Optional source URL or citation")
    parser.add_argument("--download", action="store_true", help="Reserved for future real downloaders")
    args = parser.parse_args()

    ensure_dirs()
    dataset = args.dataset.lower()
    description = KNOWN_DATASETS.get(dataset, "Unknown dataset; agent must document source and split before use.")
    path = REPORTS_DIR / f"data_request_{dataset}.md"
    text = f"""# Data Request: {dataset}

- created_at: `{datetime.now().isoformat(timespec="seconds")}`
- dataset: `{dataset}`
- description: {description}
- source: `{args.source or "not specified"}`
- local_data_dir: `{ROOT / "data" / dataset}`
- download_requested: `{args.download}`

## Policy

Harness v1 does not automatically download large datasets. Before enabling a downloader, document:

- original source and license
- exact split
- normalization
- horizon choices
- covariate fields
- checksum or file list

Do not use test data for early stopping or hyperparameter search.
"""
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path}")
    if args.download:
        print("Downloaders are not implemented in harness v1; this request was recorded only.")


if __name__ == "__main__":
    main()

