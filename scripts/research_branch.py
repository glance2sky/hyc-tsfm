from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import ROOT, get_git_branch, get_git_commit_full, git_worktree_clean, read_json, run_git, write_json
from research_journal import append_event, build_branch_event, ensure_branch_journal


BRANCHES_DIR = ROOT / "research" / "branches"
DEFAULT_PREFIX = "research/"


def branch_state_path(branch_id: str) -> Path:
    return BRANCHES_DIR / f"{branch_id}.json"


def branch_note_path(branch_id: str) -> Path:
    return BRANCHES_DIR / f"{branch_id}.md"


def build_note(
    branch_id: str,
    git_branch: str,
    base_branch: str,
    base_commit: str,
    question: str,
    reason: str,
) -> str:
    return f"""# Branch Note: {branch_id}

- question: {question or '<one main question family>'}
- owner_backbone: <chronos-2 or other>
- primary_dataset_scope: <dataset or dataset family>
- status: active
- git_branch: `{git_branch}`
- base_branch: `{base_branch}`
- base_commit: `{base_commit}`
- current_belief: <what the branch currently believes>
- promotion_bar: <what evidence would justify keeping or expanding this branch>
- kill_signal: <what evidence would stop this branch and send us back to the base branch>
- activity_journal: `research/activity/{branch_id}.md`

## Why This Branch Exists

{reason or '<two to five sentences>'}

## Observation Focus

- <which internal signals or diagnostics matter most for this branch>

## Literature Anchors

- <papers, repos, or notes that justify likely structure moves>

## Structural Hypotheses

- <proposed model change and why>

## Active Configs

- `configs/...`

## Run Ledger

| run_id | config | result | meaning |
| --- | --- | --- | --- |
| pending | `configs/...` | pending | first planned run |

## Decisions

- Branch created from `{base_branch}` at `{base_commit}`.
- Default rule: keep this branch only if evidence improves over the current best comparison; otherwise discard it and return to `{base_branch}`.

## Next Moves

- <next move>
"""


def load_state(branch_id: str) -> dict[str, Any]:
    path = branch_state_path(branch_id)
    if not path.exists():
        raise SystemExit(f"Branch state not found: {path}")
    return read_json(path)


def save_state(branch_id: str, state: dict[str, Any]) -> None:
    BRANCHES_DIR.mkdir(parents=True, exist_ok=True)
    write_json(branch_state_path(branch_id), state)


def cmd_start(args: argparse.Namespace) -> None:
    if not git_worktree_clean():
        raise SystemExit("Working tree is not clean. Commit or stash changes before starting a research branch.")

    branch_id = args.branch
    git_branch = args.git_branch or f"{args.prefix}{branch_id}"
    base_branch = args.base_branch or get_git_branch()
    base_commit = get_git_commit_full()

    if branch_state_path(branch_id).exists():
        raise SystemExit(f"Branch state already exists for {branch_id}")

    run_git(["switch", "-c", git_branch])

    state = {
        "branch_id": branch_id,
        "git_branch": git_branch,
        "base_branch": base_branch,
        "base_commit": base_commit,
        "decision": "active",
        "question": args.question,
        "reason": args.reason,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_state(branch_id, state)

    note_path = branch_note_path(branch_id)
    if not note_path.exists():
        note_path.write_text(
            build_note(branch_id, git_branch, base_branch, base_commit, args.question, args.reason),
            encoding="utf-8",
        )

    ensure_branch_journal(ROOT, branch_id)
    append_event(
        ROOT,
        branch_id,
        build_branch_event(
            branch=branch_id,
            git_branch=git_branch,
            event_type="branch_started",
            summary="Started research branch",
            reason=args.reason or f"Research question: {args.question}",
            extra={
                "base_branch": base_branch,
                "base_commit": base_commit,
                "question": args.question,
            },
        ),
    )

    print(f"Started research branch: {branch_id}")
    print(f"git_branch: {git_branch}")
    print(f"base_branch: {base_branch}")
    print(f"base_commit: {base_commit}")


def cmd_keep(args: argparse.Namespace) -> None:
    state = load_state(args.branch)
    state["decision"] = "keep"
    state["resolved_at"] = datetime.now().isoformat(timespec="seconds")
    if args.best_run_id:
        state["best_run_id"] = args.best_run_id
    if args.reason:
        state["keep_reason"] = args.reason
    save_state(args.branch, state)
    append_event(
        ROOT,
        args.branch,
        build_branch_event(
            branch=args.branch,
            git_branch=str(state.get("git_branch") or get_git_branch()),
            event_type="branch_kept",
            summary="Kept research branch",
            reason=args.reason or "Branch evidence improved enough to keep this line of work.",
            extra={"best_run_id": args.best_run_id},
        ),
    )
    print(f"Marked branch {args.branch} as keep")


def cmd_discard(args: argparse.Namespace) -> None:
    if not git_worktree_clean():
        raise SystemExit("Working tree is not clean. Commit or stash changes before discarding a research branch.")

    state = load_state(args.branch)
    state["decision"] = "discard"
    state["resolved_at"] = datetime.now().isoformat(timespec="seconds")
    if args.reason:
        state["discard_reason"] = args.reason
    save_state(args.branch, state)

    base_branch = str(state.get("base_branch") or "")
    if not base_branch:
        raise SystemExit("Branch state does not include a base_branch")

    append_event(
        ROOT,
        args.branch,
        build_branch_event(
            branch=args.branch,
            git_branch=str(state.get("git_branch") or get_git_branch()),
            event_type="branch_discarded",
            summary="Discarded research branch",
            reason=args.reason or "Branch evidence did not improve enough to justify keeping this version.",
            extra={"return_to": base_branch},
        ),
    )
    run_git(["switch", base_branch])
    print(f"Discarded branch {args.branch}")
    print(f"Returned to base branch: {base_branch}")
    print(f"Base commit recorded in state: {state.get('base_commit')}")


def cmd_status(args: argparse.Namespace) -> None:
    state = load_state(args.branch)
    for key in [
        "branch_id",
        "git_branch",
        "base_branch",
        "base_commit",
        "decision",
        "question",
        "reason",
        "created_at",
        "resolved_at",
        "best_run_id",
        "keep_reason",
        "discard_reason",
    ]:
        if key in state:
            print(f"{key}: {state[key]}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage keep-or-discard research git branches.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Create a research git branch from a clean base state")
    start.add_argument("--branch", required=True, help="Research branch id, used for configs and branch ledgers")
    start.add_argument("--git-branch", default="", help="Optional explicit git branch name")
    start.add_argument("--base-branch", default="", help="Optional explicit base branch name")
    start.add_argument("--question", default="", help="Main question family this branch is meant to answer")
    start.add_argument("--reason", default="", help="Why this branch is being created now")
    start.add_argument("--prefix", default=DEFAULT_PREFIX, help="Git branch prefix when --git-branch is omitted")
    start.set_defaults(func=cmd_start)

    keep = subparsers.add_parser("keep", help="Mark a research branch as worth keeping")
    keep.add_argument("--branch", required=True, help="Research branch id")
    keep.add_argument("--best-run-id", default="", help="Optional best run id supporting the keep decision")
    keep.add_argument("--reason", default="", help="Why this branch is worth keeping")
    keep.set_defaults(func=cmd_keep)

    discard = subparsers.add_parser("discard", help="Discard a research branch and switch back to its base branch")
    discard.add_argument("--branch", required=True, help="Research branch id")
    discard.add_argument("--reason", default="", help="Why this branch is being discarded")
    discard.set_defaults(func=cmd_discard)

    status = subparsers.add_parser("status", help="Show recorded state for a research branch")
    status.add_argument("--branch", required=True, help="Research branch id")
    status.set_defaults(func=cmd_status)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
