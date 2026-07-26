# Critical review and thesis-gap analysis

This LaTeX project critically reviews the four supplied papers, checks what
their evidence transfers to CRESCO8, audits the relevant `llama.cpp` controls,
and converts the remaining questions into a decision-gated thesis programme.

The review is intentionally corpus-bounded. It does not describe a question as
field-wide novel until a systematic literature search has been completed.

## Build

```bash
make analysis
make analysis-overview
```

The first command builds `analysis/analysis.pdf`. The second builds the
three-page supervisor brief at `analysis/overview/overview.pdf`.

Both projects use the centralized bibliography in `thesis/references.bib`.

## Structure

| File | Purpose |
|---|---|
| `chapters/01-corpus.tex` | Review boundary, source verification, and a critical reading of each paper |
| `chapters/02-synthesis.tex` | Cross-paper conclusions, contradictions, and unsupported claims |
| `chapters/03-audit.tex` | Provisional source audit of `llama.cpp` commit `ff067f7` |
| `chapters/04-gaps.tex` | Four ranked research questions and optional extensions |
| `chapters/05-programme.tex` | Evidence-gated work programme and stopping rules |
| `chapters/06-methodology.tex` | Experimental controls, validity, falsification, and next actions |
| `overview/overview.tex` | Three-page discussion brief for supervisors |

## Maintenance

The runtime audit is pinned to commit
`ff067f76dd8e9e05f0528056f1274adf01a54d70` (26 July 2026). Re-check every
source path before quoting it in the final thesis, and confirm all static
findings at runtime on CRESCO8.
