from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from _common import (
    ROOT,
    RUNS_DIR,
    dump_yaml,
    ensure_dirs,
    get_git_branch,
    get_git_commit,
    load_yaml,
    now_run_id,
    validate_config,
    write_json,
)
from research_journal import append_event, build_experiment_event


def build_base_metrics(run_id: str, config: dict[str, Any], status: str, notes: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "branch": config.get("branch"),
        "git_branch": get_git_branch(),
        "commit": get_git_commit(),
        "hypothesis": config.get("hypothesis"),
        "backbone": config.get("backbone"),
        "adapter": config.get("adapter"),
        "dataset": config.get("dataset"),
        "horizon": config.get("horizon"),
        "seed": config.get("seed"),
        "status": status,
        "mse": None,
        "mae": None,
        "peak_vram_gb": None,
        "trainable_params_m": None,
        "training_minutes": None,
        "notes": notes,
    }


def run_smoke(run_dir: Path, run_id: str, config: dict[str, Any]) -> dict[str, Any]:
    log_path = run_dir / "run.log"
    t0 = time.time()
    lines = [
        "HyC-TSFM harness smoke run",
        f"run_id: {run_id}",
        f"branch: {config.get('branch')}",
        f"git_branch: {get_git_branch()}",
        f"dataset: {config.get('dataset')}",
        f"backbone: {config.get('backbone')}",
        f"adapter: {config.get('adapter')}",
        "No model training was executed.",
    ]
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    metrics = build_base_metrics(run_id, config, "inconclusive", "Smoke run completed; no scientific claim.")
    metrics.update(
        {
            "mse": 0.0,
            "mae": 0.0,
            "peak_vram_gb": 0.0,
            "trainable_params_m": 0.0,
            "training_minutes": round((time.time() - t0) / 60, 4),
        }
    )
    return metrics


def run_external(run_dir: Path, run_id: str, config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    command = config.get("command")
    if not command:
        metrics = build_base_metrics(run_id, config, "crash", "External runner requires a command field.")
        (run_dir / "run.log").write_text("Missing command in config.\n", encoding="utf-8")
        return metrics

    rendered = str(command).replace("${CONFIG_PATH}", str(run_dir / "config.yaml"))
    log_path = run_dir / "run.log"
    t0 = time.time()
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"command: {rendered}\n")
        log.write(f"git_branch: {get_git_branch()}\n")
        log.write(f"original_config: {config_path}\n\n")
        log.flush()
        proc = subprocess.run(
            rendered,
            cwd=Path.cwd(),
            shell=True,
            text=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    elapsed_min = (time.time() - t0) / 60
    status = "needs_rerun"
    notes = f"External command exited with code {proc.returncode}; parse metrics before making claims."
    if proc.returncode != 0:
        log_text = log_path.read_text(encoding="utf-8", errors="replace").lower()
        if "out of memory" in log_text or "cuda oom" in log_text:
            status = "oom"
            notes = "External run failed with probable OOM."
        else:
            status = "crash"
            notes = f"External run failed with exit code {proc.returncode}."
    metrics = build_base_metrics(run_id, config, status, notes)
    metrics["training_minutes"] = round(elapsed_min, 4)
    return metrics


def write_summary(run_dir: Path, metrics: dict[str, Any], config: dict[str, Any]) -> None:
    summary = f"""# Run Summary: {metrics["run_id"]}

- branch: `{metrics.get("branch")}`
- git_branch: `{metrics.get("git_branch")}`
- status: `{metrics.get("status")}`
- hypothesis: {metrics.get("hypothesis")}
- dataset: `{metrics.get("dataset")}`
- horizon: `{metrics.get("horizon")}`
- backbone: `{metrics.get("backbone")}`
- adapter: `{metrics.get("adapter")}`
- seed: `{metrics.get("seed")}`
- mse: `{metrics.get("mse")}`
- mae: `{metrics.get("mae")}`
- peak_vram_gb: `{metrics.get("peak_vram_gb")}`
- trainable_params_m: `{metrics.get("trainable_params_m")}`
- training_minutes: `{metrics.get("training_minutes")}`

## Notes

{metrics.get("notes")}

## Claim Discipline

Do not use this run for a main scientific claim unless it has matching baselines, required seeds, and reviewer checklist approval.
"""
    run_dir.joinpath("summary.md").write_text(summary, encoding="utf-8")


def maybe_log_experiment_event(
    config: dict[str, Any],
    config_path: Path,
    run_id: str,
    run_dir: Path,
    metrics: dict[str, Any],
) -> None:
    branch = str(config.get("branch") or "")
    if not branch:
        return

    try:
        config_display = config_path.relative_to(ROOT).as_posix()
    except ValueError:
        config_display = str(config_path)

    try:
        run_dir_display = run_dir.relative_to(ROOT).as_posix()
    except ValueError:
        run_dir_display = run_dir.as_posix()

    event = build_experiment_event(
        branch=branch,
        git_branch=str(metrics.get("git_branch") or get_git_branch()),
        run_id=run_id,
        config_path=config_display,
        metrics=metrics,
        run_dir=run_dir_display,
    )
    append_event(ROOT, branch, event)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one configured HyC-TSFM harness experiment.")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--run-id", default="", help="Optional explicit run id")
    parser.add_argument("--validate-only", action="store_true", help="Validate config without running")
    args = parser.parse_args()

    ensure_dirs()
    config_path = Path(args.config).resolve()
    config = load_yaml(config_path)
    errors = validate_config(config)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
    if args.validate_only:
        print(f"Config OK: {config_path}")
        return

    run_id = args.run_id or now_run_id()
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=False, exist_ok=False)
    dump_yaml(config, run_dir / "config.yaml")

    runner = config.get("runner", "external")
    try:
        if runner == "smoke":
            metrics = run_smoke(run_dir, run_id, config)
        elif runner == "external":
            metrics = run_external(run_dir, run_id, config, config_path)
        else:
            (run_dir / "run.log").write_text(f"Unknown runner: {runner}\n", encoding="utf-8")
            metrics = build_base_metrics(run_id, config, "crash", f"Unknown runner: {runner}")
    except RuntimeError as exc:
        metrics = build_base_metrics(run_id, config, "crash", repr(exc))
        (run_dir / "run.log").write_text(repr(exc) + "\n", encoding="utf-8")

    write_json(run_dir / "metrics.json", metrics)
    write_summary(run_dir, metrics, config)
    maybe_log_experiment_event(config, config_path, run_id, run_dir, metrics)
    print(f"run_id: {run_id}")
    print(f"status: {metrics['status']}")
    print(f"run_dir: {run_dir}")


if __name__ == "__main__":
    main()
