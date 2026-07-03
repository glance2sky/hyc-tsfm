---
name: manage-experiment-branches
description: Use when starting a new experimental code or config variant that should be kept only if the results improve and discarded otherwise.
---

# Manage Experiment Branches

## Overview

This repository uses git branches as versioned research threads. Start from a clean base branch, create a dedicated experiment branch, and keep it only if the evidence improves over the current comparison point.

## Default Rule

- New idea: create a fresh branch first.
- Better result or stronger evidence: keep the branch.
- No improvement, negative result, or dead-end mechanism: discard the branch and return to the recorded base branch.

## Commands

- Start: `python scripts/research_branch.py start --branch <branch-id> --question "..." --reason "..."`
- Keep: `python scripts/research_branch.py keep --branch <branch-id> --best-run-id <run_id> --reason "..."`
- Discard: `python scripts/research_branch.py discard --branch <branch-id> --reason "..."`
- Status: `python scripts/research_branch.py status --branch <branch-id>`

## Notes

- The research branch id should match config field `branch`.
- The default git branch name is `research/<branch-id>`.
- Discard switches back to the recorded base branch and keeps the branch state file for audit.
- The exact base commit is stored in `research/branches/<branch-id>.json`.
- Lifecycle events are appended automatically to `research/activity/<branch-id>.md` and `.jsonl`.

## Common Mistakes

- Editing on `master` or another long-lived branch.
- Keeping a branch alive after repeated non-improving results.
- Forgetting to record which run justified a keep decision.
- Starting a branch without writing the question and reason.
