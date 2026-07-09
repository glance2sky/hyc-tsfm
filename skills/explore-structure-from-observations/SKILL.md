---
name: explore-structure-from-observations
description: Use when repeated parameter tuning is not enough, when a model bottleneck needs evidence-driven diagnosis, or when considering architecture changes backed by observations and literature.
---

# Explore Structure From Observations

## Overview

Do not treat parameter tuning as the default improvement mechanism. When performance stalls or behavior looks unhealthy, collect observations, consult literature or references, and propose structure-level changes with explicit rationale.

## Default Order

1. Observe the model first.
2. Interpret the bottleneck.
3. Check literature, papers, or trusted references.
4. Propose a structure change.
5. Only use pure parameter tuning when you can explain why structure is not the right next move.

## What To Observe

Useful indicators include:

- per-module gradient norms
- update norms or near-frozen modules
- activation statistics or saturation
- gate values and collapse behavior
- attention entropy or sparsity
- graph edge utilization and relation sparsity
- curvature values or curvature collapse
- covariate ablation sensitivity
- validation-train gap by component-specific intervention
- inference latency, memory, or unstable numerics

## Logging Discipline

- Log observations with `python scripts/research_journal.py observe ...`
- Log paper findings with `python scripts/research_journal.py literature ...`
- Log architecture ideas with `python scripts/research_journal.py propose ...`
- Link proposal evidence back to observation and literature entries

## Good Structural Moves

- add or remove residual paths
- change gating placement or bypass behavior
- split one overloaded block into two narrower roles
- add projection or normalization around unstable interfaces
- simplify a component that is not receiving useful gradients
- move conditioning earlier or later if observations justify it

## When Parameter Tuning Is Acceptable

Parameter tuning is acceptable when:

- the structure already looks healthy
- the next uncertainty is clearly optimization-related
- the tuning run is explicitly supporting a structural hypothesis

If you do a tuning-only run, record why a structural change was deferred.

## Common Mistakes

- Running many tuning trials before collecting any observations.
- Making architecture changes with no evidence trail.
- Reading papers without recording what mechanism was actually borrowed.
- Treating all bad results as learning-rate problems.
