---
name: manage-references
description: Use when downloading, reading, or borrowing from papers and external repositories for this project.
---

# Manage References

## Overview

Reference assets are allowed, but they must stay clearly separated from owned project code. This repository uses a read-only mirror model for papers and external repos.

## Directory Rules

- `references/papers/`
  Store downloaded papers or supplementary material here.
- `references/external-code/`
  Store cloned or unpacked external repositories here.
- `references/notes/`
  Store tracked notes describing what was downloaded, why it matters, and what is safe to borrow.

## Required Practice

- Do not edit files inside `references/papers/` or `references/external-code/`.
- Record source, license, local path, and relevance in `references/notes/<slug>.md`.
- If a useful implementation idea is found, rewrite or copy it into owned project code under `src/`, `scripts/`, or another project-controlled directory.
- Keep project-specific experiments, patches, and adapters out of mirrored external repos.
- When a paper materially changes the branch direction, also record it with `python scripts/research_journal.py literature ...`.

## Good Workflow

1. Add the paper PDF or repo snapshot to the proper `references/` subdirectory.
2. Create or update a note in `references/notes/`.
3. Summarize the mechanism or component worth borrowing.
4. Record the actionable conclusion in the branch activity journal.
5. Re-implement it in owned code only if it helps the active research branch.

## Common Mistakes

- Treating vendor code as the main implementation area.
- Downloading references without writing down source and relevance.
- Mixing project experiments into mirrored external repos so provenance becomes unclear.
- Reading papers without recording what they changed in the branch strategy.
