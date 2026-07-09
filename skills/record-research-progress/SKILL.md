---
name: record-research-progress
description: Use when changing code, configs, parameters, or files during autonomous research and you need a durable progress log for humans to inspect later.
---

# Record Research Progress

## Overview

This repository keeps a durable research activity journal per branch. Use it to record what changed, why it changed, which files were involved, and where experiment results were written.

## Automatic Logging

These events are logged automatically:

- `branch_started`, `branch_kept`, `branch_discarded` via `scripts/research_branch.py`
- `experiment_run` via `scripts/run_experiment.py`

## Manual Logging

When you change code, configs, parameters, or add files, record the action with:

- `python scripts/research_journal.py change --branch <branch-id> --summary "..." --reason "..." --file "path|modified|purpose"`
- `python scripts/research_journal.py note --branch <branch-id> --summary "..." --reason "..."`
- `python scripts/research_journal.py observe --branch <branch-id> --summary "..." --reason "..." --stage training --indicator "name=value" --takeaway "..."`
- `python scripts/research_journal.py literature --branch <branch-id> --title "..." --source "..." --finding "..." --implication "..."`
- `python scripts/research_journal.py propose --branch <branch-id> --summary "..." --reason "..." --target "..." --expected-effect "..." --evidence-ref "..."`

Repeat `--file`, `--indicator`, or `--evidence-ref` as needed.

## Where Logs Go

- `research/activity/<branch-id>.jsonl`
- `research/activity/<branch-id>.md`

## What To Record

- Parameter or model changes and why they were attempted.
- New files and their role.
- Important debugging notes or blockers.
- Observations from training, validation, or inference.
- Literature findings that influenced the next move.
- Structure-level proposals and which evidence supports them.
- Experiment outcomes and where the artifacts live.

## Common Mistakes

- Changing files without logging why.
- Adding helper or config files without recording their purpose.
- Recording experiments but not the observation that motivated them.
- Forcing humans to reconstruct the reasoning only from git diff.
