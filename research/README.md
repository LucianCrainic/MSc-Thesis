# Research and documentation

Everything written *around* the thesis: the reading and reasoning that will
later be condensed into the thesis chapters. Nothing here is a thesis chapter
itself — material graduates from here into `thesis/` once it is settled.

| Directory | Purpose | Feeds into |
|---|---|---|
| `notes/` | Technical background: hardware, platform, and the literature, written up as a coherent argument. | The theoretical/background chapters of the thesis. |
| `analysis/` | Critical analysis work: reviewing evidence, auditing software, identifying and defending the research gap. | The related-work and methodology chapters. |
| `briefings/` | Short, dated documents written for supervisor meetings. | Nothing directly — they record decisions and open questions. |

All three cite the shared bibliography at `bibliography/references.bib`.

## `notes/`

`technical-background.tex` — the main background document, assembled from
`sections/`. Figures are in `figures/`; `editorial-review.md` records the
editorial decisions behind the current shape of the document, including which
claims were cut for being unsupported before measurement.

```bash
inv notes
```

## `analysis/`

`research-gap-analysis.tex` — the critical review of the corpus, the
`llama.cpp` audit, the ranked research questions, and the decision-gated work
programme. See [analysis/README.md](analysis/README.md).

```bash
inv analysis
```

## `briefings/`

One self-contained `.tex` file per briefing, named
`YYYY-MM-DD-topic.tex` for the meeting it was written for. They are short by
design — a few pages that a supervisor can read before a meeting — and they are
kept rather than overwritten, so the sequence of files is a record of how the
project's framing changed over time.

```bash
inv briefings                                    # build all of them
inv briefings --name 2026-07-26-supervisor-overview   # build just one
```

To start a new one, copy the most recent briefing and rename it to the new
meeting date.
