from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "runs"
RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"

REQUIRED_CONFIG_KEYS = {
    "dataset",
    "split",
    "horizon",
    "context_length",
    "backbone",
    "adapter",
    "graph_builder",
    "curvature_mode",
    "injection_mode",
    "seed",
    "batch_size",
    "precision",
    "early_stopping",
    "output_dir",
    "hypothesis",
}

ALLOWED_STATUS = {
    "keep",
    "discard",
    "crash",
    "oom",
    "inconclusive",
    "needs_rerun",
}


def ensure_dirs() -> None:
    for path in (RUNS_DIR, RESULTS_DIR, REPORTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def now_run_id() -> str:
    base = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    candidate = base
    suffix = 1
    while (RUNS_DIR / candidate).exists():
        suffix += 1
        candidate = f"{base}_{suffix:02d}"
    return candidate


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    try:
        if re.fullmatch(r"[-+]?\d+", value):
            return int(value)
        if re.fullmatch(r"[-+]?(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?", value):
            return float(value)
    except ValueError:
        pass
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a small YAML subset; uses PyYAML if installed."""
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Config must be a mapping: {path}")
        return data
    except ModuleNotFoundError:
        data: dict[str, Any] = {}
        with path.open("r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    raise ValueError(f"Unsupported YAML line {line_no} in {path}: {raw.rstrip()}")
                key, value = line.split(":", 1)
                data[key.strip()] = parse_scalar(value)
        return data


def dump_yaml(data: dict[str, Any], path: Path) -> None:
    lines = []
    for key, value in data.items():
        if isinstance(value, bool):
            text = "true" if value else "false"
        elif value is None:
            text = "null"
        elif isinstance(value, (int, float)):
            text = str(value)
        else:
            text = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CONFIG_KEYS - set(config))
    if missing:
        errors.append("Missing required config keys: " + ", ".join(missing))
    if "max_epochs" not in config and "max_steps" not in config:
        errors.append("Config must include either max_epochs or max_steps")
    if config.get("record", False) and config.get("runner") == "smoke":
        errors.append("Smoke configs should not set record: true")
    return errors


def get_git_commit() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return proc.stdout.strip()
    except Exception:
        return "no-git"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def command_to_display(command: list[str] | str) -> str:
    if isinstance(command, str):
        return command
    return " ".join(command)

