---
name: understand-project-scope
description: Use when deciding whether an experiment, code change, or claim still fits the HyC-TSFM paper thesis and comparison story.
---

# Understand Project Scope

## Overview

This project studies whether a curvature-aware hyperbolic adapter helps a frozen time-series foundation model use multivariate dependency structure and covariates more effectively.

## Default Story

- Paper direction: `Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`
- Default backbone: frozen `Chronos-2`
- Default method: `Lorentz HyC-Adapter`
- Default injection: `input-side conditioning`
- Default control: parameter-matched `Euclidean Adapter`

## What Counts As On-Track

- Strengthening the HyC vs frozen baseline vs matched Euclidean control story.
- Improving how structured multivariate relations or covariates are represented and injected.
- Adding geometry diagnostics that explain where HyC helps and where it does not.
- Extending the same method family to more datasets or backbones without changing the thesis.

## What Counts As Drift

- Switching to an unrelated forecasting model as the main line.
- Turning the repo into a generic benchmark harness with no HyC argument.
- Doing full-model fine-tuning as the primary contribution.
- Making claims about universal gains without structural or geometric evidence.

## Default Evidence Order

1. Make sure a frozen backbone baseline exists.
2. Add the matched Euclidean control.
3. Compare HyC against both.
4. Use geometry and covariate-focused analysis to explain the result.

## Adapter Defaults

- Graph builder: dynamic sparse relation graph, usually top-k.
- Geometry: Lorentz model with learnable curvature.
- Message passing: hyperbolic relation modeling, then map back to tangent space.
- Injection: input-side conditioning first; other insertion modes are secondary experiments.

## Common Mistakes

- Optimizing HyC before a fairness control exists.
- Claiming success from a single unstable setting.
- Mixing unrelated hypotheses into one implementation branch.
