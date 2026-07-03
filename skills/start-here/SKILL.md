---
name: start-here
description: Use when entering this repository or resuming work after context loss, before reading other project files in bulk.
---

# Start Here

## Overview

This repository uses local skills for progressive disclosure. Do not batch-read `docs/` or every rules file at the start. Read this file first, then load only the next skill that matches the task.

## Core Rules

- Keep the paper direction centered on HyC-Adapter for covariate-aware TSFM forecasting.
- Treat `references/papers/` and `references/external-code/` as read-only mirrors.
- Start each new research thread from a clean git branch, then keep or discard that branch based on evidence.
- Record official experiments through `scripts/run_experiment.py` and `scripts/collect_results.py`.
- Record code/config/file changes through the research activity journal.
- Keep one research question family per branch note in `research/branches/`.

## Routing

- If you need the scientific thesis, default comparisons, or adapter direction, read `skills/understand-project-scope/SKILL.md`.
- If you need to start, keep, or discard a version branch, read `skills/manage-experiment-branches/SKILL.md`.
- If you need to log changes, notes, or file purposes during research, read `skills/record-research-progress/SKILL.md`.
- If you need to start or continue a research thread, read `skills/run-research-branch/SKILL.md`.
- If you need to fetch or study papers or external repos, read `skills/manage-references/SKILL.md`.
- If you are about to run or register a formal experiment, read `skills/record-official-run/SKILL.md`.

## Resume Protocol

When resuming work:

1. Check git status and current branch.
2. Read the relevant branch log in `research/branches/` if one exists.
3. Read the activity journal in `research/activity/` for the active branch.
4. Read only the configs, reports, or reference notes that the active task actually needs.

## Common Mistakes

- Reading the entire repository before choosing a branch task.
- Treating legacy `docs/` as the primary workflow source.
- Editing mirrored external code instead of rewriting needed pieces into owned project code.
- Running experiments on the base branch instead of on a dedicated research branch.
- Changing files without writing down why they changed.
