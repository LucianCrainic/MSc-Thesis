# Critical review and research-gap analysis

This LaTeX project critically reviews the four supplied papers, checks what
their evidence transfers to CRESCO8, audits the relevant `llama.cpp` controls,
and converts the remaining questions into a decision-gated thesis programme.

The review is intentionally corpus-bounded. It does not describe a question as
field-wide novel until a systematic literature search has been completed.

## Build

```bash
inv analysis
```

This produces `build/research-gap-analysis.pdf`. The three-page supervisor
brief derived from this review now lives in `research/briefings/` and is built
separately with `inv briefings`.

## Structure

| File | Purpose |
|---|---|
| `research-gap-analysis.tex` | Document preamble and section ordering |
| `sections/01-corpus.tex` | Review boundary, source verification, and a critical reading of each paper |
| `sections/02-synthesis.tex` | Cross-paper conclusions, contradictions, and unsupported claims |
| `sections/03-audit.tex` | Provisional source audit of `llama.cpp` commit `ff067f7` |
| `sections/04-gaps.tex` | Four ranked research questions and optional extensions |
| `sections/05-programme.tex` | Evidence-gated work programme and stopping rules |
| `sections/06-methodology.tex` | Experimental controls, validity, falsification, and next actions |

The bibliography is the shared one at `bibliography/references.bib`.

## Maintenance

The runtime audit is pinned to commit
`ff067f76dd8e9e05f0528056f1274adf01a54d70` (26 July 2026). Re-check every
source path before quoting it in the final thesis, and confirm all static
findings at runtime on CRESCO8.
