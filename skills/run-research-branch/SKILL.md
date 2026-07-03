---
name: run-research-branch
description: Use when planning, continuing, or reviewing a branch-first experiment loop for one research question family.
---

# Run Research Branch

## Overview

The default unit of progress is a research branch, not a stage. A branch is one coherent question family, such as graph construction, curvature behavior, covariate injection, or a specific dataset thread.

## Branch Contract

- One branch should answer one main question family.
- A branch may contain several runs, ablations, and fixes.
- A branch ends by being kept, discarded, promoted, merged into another branch, or archived.
- Store the branch ledger at `research/branches/<branch-id>.md`.
- **REQUIRED SUB-SKILL:** Use `manage-experiment-branches` before code, config, or model edits begin.
- **REQUIRED SUB-SKILL:** Use `record-research-progress` whenever files, parameters, or model structures change.

Use `skills/run-research-branch/branch-note-template.md` when creating a new branch ledger.

## Loop

1. Start the git version branch from a clean base state.
2. Read or create the branch ledger.
3. State the current question, current belief, and kill signal.
4. Pick exactly one next move:
   - fill a missing baseline
   - fill a missing fairness control
   - fix a blocker or crash
   - mutate the branch mechanism
   - reproduce a promising gain
   - run geometry or covariate diagnosis
   - fork a new branch if the mechanism changes
5. Before editing files or changing parameters, log the intended change and reason.
6. If the move needs papers or external repos, use `skills/manage-references/SKILL.md`.
7. If the move needs a formal run, use `skills/record-official-run/SKILL.md`.
8. After the run or investigation, update the branch ledger with evidence, branch status, and the next best move.
9. If evidence improves enough, keep the branch. If not, discard it and return to the base branch.

## Decision Heuristics

| Situation | Preferred response |
| --- | --- |
| Baseline missing | Stop tuning HyC and fill the baseline gap first |
| Euclidean control missing | Add the control before claiming a HyC-specific benefit |
| Repeated crash or OOM | Stabilize the branch before opening more variants |
| No gain after 2-3 meaningful variants | Discard or fork the branch by changing mechanism, not by endless tuning |
| One-off gain with weak evidence | Reproduce and add controls before keep |
| Gain aligns with structural intuition | Keep first, then promote to a broader dataset or backbone |

## Status Vocabulary

- `active`: branch is still producing useful next steps
- `blocked`: current blocker needs environment, data, or missing implementation work
- `promising`: early evidence exists, but needs reproduction or controls
- `keep`: branch earned retention because evidence improved
- `discard`: branch is not worth further budget and should return to base
- `promoted`: branch earned expansion to more datasets, seeds, or backbones
- `archived`: preserved for reference, not active

## Common Mistakes

- Mixing multiple mechanisms into one branch so results stop being interpretable.
- Running new variants without writing down why the branch still deserves budget.
- Letting branch files turn into changelogs instead of research decisions.
- Continuing to edit a branch that should already have been discarded.
- Leaving humans to infer change reasons only from diffs.
