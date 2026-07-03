from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import ROOT, get_git_branch


ACTIVITY_DIR = ROOT / "research" / "activity"


def activity_paths(root: Path, branch: str) -> tuple[Path, Path]:
    base = root / "research" / "activity"
    return base / f"{branch}.jsonl", base / f"{branch}.md"


def ensure_branch_journal(root: Path, branch: str) -> tuple[Path, Path]:
    jsonl_path, md_path = activity_paths(root, branch)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    if not jsonl_path.exists():
        jsonl_path.write_text("", encoding="utf-8")
    if not md_path.exists():
        md_path.write_text(
            f"# Activity Journal: {branch}\n\n"
            "This file is an auto-appended timeline of research actions, code/config changes, file additions, and experiment outcomes.\n\n"
            "## Timeline\n\n",
            encoding="utf-8",
        )
    return jsonl_path, md_path


def build_file_record(path: str, purpose: str, change_type: str) -> dict[str, str]:
    return {
        "path": path,
        "purpose": purpose,
        "change_type": change_type,
    }


def build_branch_event(
    branch: str,
    git_branch: str,
    event_type: str,
    summary: str,
    reason: str = "",
    files: list[dict[str, str]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "branch": branch,
        "git_branch": git_branch,
        "event_type": event_type,
        "summary": summary,
        "reason": reason,
        "files": files or [],
    }
    if extra:
        event.update(extra)
    return event


def build_experiment_event(
    branch: str,
    git_branch: str,
    run_id: str,
    config_path: str,
    metrics: dict[str, Any],
    run_dir: str,
) -> dict[str, Any]:
    status = metrics.get("status")
    run_dir_path = Path(run_dir)
    run_dir_text = run_dir_path.as_posix()
    result = {
        "run_id": run_id,
        "config_path": config_path,
        "run_dir": run_dir_text,
        "metrics_path": (run_dir_path / "metrics.json").as_posix(),
        "summary_path": (run_dir_path / "summary.md").as_posix(),
        "log_path": (run_dir_path / "run.log").as_posix(),
        "status": status,
        "mse": metrics.get("mse"),
        "mae": metrics.get("mae"),
        "notes": metrics.get("notes"),
    }
    summary = f"Run {run_id} finished with status {status}"
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "branch": branch,
        "git_branch": git_branch,
        "event_type": "experiment_run",
        "summary": summary,
        "reason": metrics.get("notes") or "",
        "files": [
            build_file_record(
                path=config_path,
                purpose="Config used for the recorded run.",
                change_type="used",
            )
        ],
        "result": result,
    }


def render_event_markdown(event: dict[str, Any]) -> str:
    lines = [f"### {event.get('timestamp')} `{event.get('event_type')}` {event.get('summary')}", ""]
    git_branch = str(event.get("git_branch") or "")
    if git_branch:
        lines.append(f"- git_branch: `{git_branch}`")
    reason = str(event.get("reason") or "")
    if reason:
        lines.append(f"- reason: {reason}")

    files = event.get("files") or []
    if files:
        lines.append("- files:")
        for file_info in files:
            lines.append(
                f"  - `{file_info.get('path')}` ({file_info.get('change_type')}): {file_info.get('purpose')}"
            )

    result = event.get("result")
    if isinstance(result, dict):
        lines.append(f"- run_id: `{result.get('run_id')}`")
        lines.append(f"- status: `{result.get('status')}`")
        lines.append(f"- run_dir: `{result.get('run_dir')}`")
        lines.append(f"- metrics_path: `{result.get('metrics_path')}`")
        lines.append(f"- summary_path: `{result.get('summary_path')}`")
        if result.get("mse") is not None or result.get("mae") is not None:
            lines.append(f"- metrics: mse={result.get('mse')}, mae={result.get('mae')}")

    lines.append("")
    return "\n".join(lines)


def append_event(root: Path, branch: str, event: dict[str, Any]) -> tuple[Path, Path]:
    jsonl_path, md_path = ensure_branch_journal(root, branch)
    payload = dict(event)
    payload.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    payload.setdefault("branch", branch)
    payload.setdefault("git_branch", get_git_branch())
    payload.setdefault("files", [])
    payload.setdefault("reason", "")

    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    with md_path.open("a", encoding="utf-8") as f:
        f.write(render_event_markdown(payload))

    return jsonl_path, md_path


def parse_file_args(values: list[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for value in values:
        parts = value.split("|", 2)
        if len(parts) != 3:
            raise SystemExit("Each --file entry must look like path|change_type|purpose")
        records.append(build_file_record(parts[0], parts[2], parts[1]))
    return records


def cmd_change(args: argparse.Namespace) -> None:
    event = build_branch_event(
        branch=args.branch,
        git_branch=args.git_branch or get_git_branch(),
        event_type="change",
        summary=args.summary,
        reason=args.reason,
        files=parse_file_args(args.file or []),
    )
    jsonl_path, md_path = append_event(ROOT, args.branch, event)
    print(f"Logged change event to {jsonl_path}")
    print(f"Updated markdown journal {md_path}")


def cmd_note(args: argparse.Namespace) -> None:
    event = build_branch_event(
        branch=args.branch,
        git_branch=args.git_branch or get_git_branch(),
        event_type="note",
        summary=args.summary,
        reason=args.reason,
    )
    jsonl_path, md_path = append_event(ROOT, args.branch, event)
    print(f"Logged note event to {jsonl_path}")
    print(f"Updated markdown journal {md_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record structured research activity for a branch.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    change = subparsers.add_parser("change", help="Record a code, config, or model modification event")
    change.add_argument("--branch", required=True, help="Research branch id")
    change.add_argument("--summary", required=True, help="Short description of what changed")
    change.add_argument("--reason", required=True, help="Why the change was made")
    change.add_argument("--git-branch", default="", help="Optional explicit git branch name")
    change.add_argument(
        "--file",
        action="append",
        default=[],
        help="Repeated file record in the format path|change_type|purpose",
    )
    change.set_defaults(func=cmd_change)

    note = subparsers.add_parser("note", help="Record a reasoning note without file records")
    note.add_argument("--branch", required=True, help="Research branch id")
    note.add_argument("--summary", required=True, help="Short note title")
    note.add_argument("--reason", required=True, help="Detailed note body")
    note.add_argument("--git-branch", default="", help="Optional explicit git branch name")
    note.set_defaults(func=cmd_note)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
