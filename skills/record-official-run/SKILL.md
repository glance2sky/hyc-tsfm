---
name: record-official-run
description: Use when validating, running, or registering an official experiment that should produce durable run artifacts and optional result aggregation.
---

# Record Official Run

## Overview

Official experiments go through the harness scripts, not ad hoc logging. Every formal run should leave a reproducible artifact trail under `runs/`.

## Required Config Shape

Each official config must define at least:

- `branch`
- `dataset`
- `split`
- `horizon`
- `context_length`
- `backbone`
- `adapter`
- `graph_builder`
- `curvature_mode`
- `injection_mode`
- `seed`
- `batch_size`
- `precision`
- `max_epochs` or `max_steps`
- `early_stopping`
- `output_dir`
- `hypothesis`

Useful optional fields for traceability:

- `change_scope`
- `change_target`
- `observation_refs`
- `literature_refs`
- `proposal_refs`

## Run Flow

1. Validate the config with `python scripts/run_experiment.py --config <path> --validate-only`
2. If the config or parameters were just changed, record that first through `skills/record-research-progress`
3. If this is a structure-motivated run, make sure the supporting observation and literature notes already exist
4. Execute the run with `python scripts/run_experiment.py --config <path>`
5. Inspect `runs/<run_id>/summary.md` and `runs/<run_id>/metrics.json`
6. Append the run with `python scripts/collect_results.py --run-id <run_id>` only when the config is meant to be recorded
7. Update the active branch ledger with the result and the next decision

## Artifact Contract

Every official run should write:

- `runs/<run_id>/config.yaml`
- `runs/<run_id>/run.log`
- `runs/<run_id>/metrics.json`
- `runs/<run_id>/summary.md`

## Automatic Journal Hook

After each run, `scripts/run_experiment.py` automatically appends an `experiment_run` event to the branch activity journal, including:

- which config was used
- where the run artifacts live
- status, MSE, MAE, and notes when available
- optional `change_scope` and `change_target` metadata when present

## Status Vocabulary

- `keep`
- `discard`
- `crash`
- `oom`
- `inconclusive`
- `needs_rerun`

## Common Mistakes

- Recording debug smoke runs as scientific evidence.
- Skipping the branch ledger update after a run completes.
- Writing conclusions before the fairness control or reproduction step exists.
- Running a tuning-only experiment without recording why a structure change was not chosen.
