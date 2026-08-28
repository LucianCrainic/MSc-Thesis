<p align="center">
  <img src="assets/header.svg" alt="MSc Thesis — quantized LLM inference on HBM-equipped CPUs" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-800020?style=flat-square"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-work%20in%20progress-d57d1c?style=flat-square">
  <img alt="LaTeX" src="https://img.shields.io/badge/LaTeX-sapthesis-008080?style=flat-square&logo=latex&logoColor=white">
  <img alt="Tectonic" src="https://img.shields.io/badge/build-Tectonic-2b5797?style=flat-square">
  <img alt="Invoke" src="https://img.shields.io/badge/tasks-Invoke-3776AB?style=flat-square&logo=python&logoColor=white">
</p>

<p align="center">
  <a href="thesis/"><b>Thesis</b></a> ·
  <a href="slides/"><b>Slides</b></a> ·
  <a href="research/README.md"><b>Research</b></a> ·
  <a href="research/analysis/README.md"><b>Gap analysis</b></a> ·
  <a href="bibliography/references.bib"><b>Bibliography</b></a>
</p>

---

## What this thesis argues

> [!NOTE]
> **Work in progress.** This section is deliberately empty until the
> experimental phase produces results. Writing the argument here before
> measuring it would be stating a conclusion the work has not yet earned.

**To do**

- [ ] State the argument, once there is a measured result to state it from
- [ ] Summarise the four research questions and what each one settled
- [ ] Record the headline numbers and where they sit against related work

In the meantime the reasoning behind the project lives in
[`research/`](research/README.md): the background and literature review in
[`research/notes/`](research/README.md#notes), and the ranked research
questions with their pre-registered hypotheses in the
[gap analysis](research/analysis/README.md).

## Building

Requires [Tectonic](https://tectonic-typesetting.github.io/) and
[Invoke](https://www.pyinvoke.org/):

```bash
brew install tectonic && pip install -r requirements.txt
```

Then, from the repository root:

| Command | Builds |
|---|---|
| `inv thesis` | `build/thesis.pdf` — the thesis |
| `inv slides` | `build/slides.pdf` — the defence deck |
| `inv notes` | `build/technical-background.pdf` — hardware, platform and literature notes |
| `inv analysis` | `build/research-gap-analysis.pdf` — the critical review and research gap |
| `inv briefings` | Every dated supervisor briefing in `research/briefings/` |
| `inv all` | All of the above |
| `inv list` | Lists every buildable document |
| `inv clean` | Removes `build/` |

Add `--open-pdf` to any single-document task to open the result on success, and
`inv briefings --name <stem>` to build one briefing. Every PDF lands in `build/`;
nothing is ever written back into the source tree.

## License

[MIT](LICENSE) © Lucian D. Crainic
