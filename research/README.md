# Research and documentation

Everything written *around* the thesis: the reading and reasoning that will
later be condensed into the thesis chapters. Nothing here is a thesis chapter
itself — material graduates from here into `thesis/` once it is settled.

| Directory | Purpose | Feeds into |
|---|---|---|
| `notes/` | Drafts and reading notes awaiting review, including the parked related-work chapter. | A revised related-work chapter. |
| `analysis/` | Critical analysis work: reviewing evidence, auditing software, identifying and defending the research gap. | The related-work and methodology chapters. |

Both cite the shared bibliography at `bibliography/references.bib`.

## `notes/`

The former related-work chapter and its literature and close-reading
sections are in [notes/related-work/](notes/related-work/). They are not
included in the thesis while their scope and claims are reviewed. Start
with the [dated review](notes/related-work/review-2026-10-04.md).
Background, platform and methodology material remains under
`thesis/chapters/`, with figures under `thesis/figures/` and the
continuing editorial log at `thesis/editorial-review.md`.

## `analysis/`

`research-gap-analysis.tex` — the July 2026 critical review of the corpus,
the `llama.cpp` audit, the then-ranked research questions, and the original
decision-gated work programme. See [analysis/README.md](analysis/README.md).

```bash
inv analysis
```
