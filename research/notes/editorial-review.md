# Editorial review

## 29 August 2026 (third pass) — hardware photographs, and no more em-dashes

**Photographs of the machine.** The July pass replaced all raster extracts with
original vector diagrams; that decision is now partly reversed, deliberately.
Vector diagrams are better at showing *relationships*, but they cannot show what
a thing is, and a reader who has never seen a water-cooled tray has no mental
picture to attach the argument to. Five images are now in the document:

- Front of the tray, showing two independent servers sharing only power and
  water, and the absence of video output or local console.
- Inside the tray, which is the useful one. Two processors per server with their
  DIMMs on either side is the physical form of the locality argument, and the
  HBM is conspicuously *not* visible because it sits inside the package under
  the cold plate. That is why its capacity is fixed at 64 GB and cannot be
  configured.
- Twelve nodes in the 6U enclosure, to make clear what an allocation yields.
- The rear water manifolds, in the cooling subsection.
- An `lstopo` capture from `cresco8x001.portici.enea.it`, which is a *real
  observation* rather than a vendor illustration. It shows two packages of 64
  cores with no memory-only NUMA nodes, identifying it as a general CPU
  partition node. An HBM node in Flat mode should show them, and confirming that
  is the first job of the first allocation.

Four of the five are reproduced from the Lenovo ThinkSystem SD650 V3 product
guide and are attributed in their captions. **Check the university's rules on
reproducing third-party figures before submission**; some faculties require
written permission rather than attribution alone, and the vector diagrams remain
available as replacements if so.

**Em-dashes removed.** Seventy-two of them across the notes, the analysis and
the abstract, now zero. Each was rewritten rather than swapped for a hyphen: the
parenthetical ones became commas or parentheses, the emphatic ones became
colons, and several sentences were split where the dash was holding together two
clauses that did not need joining. A few read better for it, since a dash often
concealed a sentence doing two jobs. Worth re-checking after any new writing:

    grep -rn -- '---' research/*/sections/*.tex research/*/*.tex thesis/front-matter/*.tex

---

## 29 August 2026 (second pass) — signposting, bibliography order, HPC primer

**Cross-references in the prose.** Thirty-three floats and equations existed;
twenty were never pointed at from the text. Every one now is — "as Table 4
shows", "Figure 1 contrasts", "Equation 5 gives" — so a reader is told when to
look away from the paragraph and at what. The analysis document had the same
problem in seven places, also fixed. The audit is worth re-running after any
new float is added:

    for lbl in $(grep -ho '\\label{\(fig\|tab\|eq\):[^}]*}' *.tex | sed 's/.*{//;s/}//' | sort -u); do
      grep -q "\\(figref\|tabref\|eqnref\){$lbl}" *.tex || echo "unreferenced: $lbl"
    done

**Bibliography order.** Research literature now precedes technical and
institutional sources. `biber` is not installed, so biblatex's category
mechanism was unavailable; instead the style is `unsrtnat`, which follows
first-citation order, and a `\nocite` block before the prose fixes that order.
Each document carries its own list containing only what it cites — the notes 28
papers then 8 sources, the analysis 8 then 1. **If a new work is cited, add its
key to that block**, or it will be appended at the end out of group.

**Removed from §5.1.** The old subsection described how the reading list was
built — a starting corpus of four supplied papers, a search performed in a named
month, a shortlist kept in a repository README, an admission that the search was
web-first. None of that belongs in a thesis: it describes the project's history
rather than the state of the field. The replacement states what the review
covers, what it excludes and why, and notes that some cited work is unrefereed —
which is a claim about evidence quality, not about process. The same phrasing
("the runtime this thesis will use") was corrected in two other places.

**New §1, Supercomputers, clusters and nodes.** The document previously opened
on a server tray, which assumes the reader already knows what a cluster is. It
now begins with the distinction that actually matters — *where direct memory
addressing stops* — contrasts a workstation with a cluster in a diagram, covers
the login/scheduler/batch model, and narrows to what the experiments use: one
node, one socket. The closing table states which levels are excluded and why,
since every excluded level is variability that cannot reach the comparison.
Sections renumbered accordingly; files are now `01-hpc-and-clusters` through
`07-thesis-methodology`.

**Emphasis.** Bold and italic were concentrated in the newer sections and thin
elsewhere. The older sections were brought up, targeting sentences that carry an
argument rather than decorating terms. Rough density check, emphasis per 100
lines of prose:

    for f in *.tex; do n=$(grep -o '\\textbf{\|\\emph{' $f | wc -l); \
      l=$(grep -vc '^%\|^\\' $f); echo "$f $(echo "scale=1;$n*100/$l"|bc)"; done

Anything below about 5 reads flat; the metrics and primer sections sit near 16
and do not need more.

---

## 29 August 2026 — typography, layout and the metrics section

**Layout.** The white gaps between text and floats came from three causes, now
all removed: `\FloatBarrier` after most floats, `[tbp]` placement forbidding
"here", and LaTeX's default willingness to strand a float on its own page. All
floats are `[htbp]`, the barriers are gone, `\raggedbottom` is set, and
`topfraction`/`textfraction` are tuned. Table 4 no longer sits alone on a page,
and §2.1 and §3.1 pack normally.

The three metrics tables are `xltabular` rather than floats: they break across
pages with a repeated header and a "continued" rule, so they stay next to the
text that introduces them instead of drifting. Long reference tables should use
this; short ones stay as ordinary floats.

**Table styling.** Tinted header row (`\headrow`), 1.22 row stretch
(`\tabsetup`), bold row labels, and emphasis inside cells to mark what matters.
Four-column reference tables were cut to three — at 15.8 cm four text columns
wrap so hard that the rows become unreadable. "Why it is here" and "how to read
a value" now share one wide column with an italic *Reading it:* lead-in.

**Colour by reference type.** Sources burgundy, figures green, tables blue,
equations purple, sections grey — applied both to the in-text reference and to
the caption label, so a caption and the reference pointing at it match. Use
`\figref`, `\tabref`, `\eqnref`, `\secref` rather than writing `Figure~\ref`
by hand. The same system is now in `research-gap-analysis.tex`.

**Equations.** The displayed equations that carry the argument are numbered and
captioned in the style of figures (`\eqcaption`), so they can be cited as
Equation N in the text. Nine of them: weight footprint, KV footprint, live set,
Roofline bound, step lower bound, arithmetic intensity, end-to-end latency, tier
ratio, bandwidth utilisation.

**New: §3.5, what we measure and what each number means.** Splits every quantity
into three kinds and keeps them apart — a *result* is defensible as an outcome,
an *explanation* says why the outcome came out that way and carries no weight
alone, a *validity check* decides whether the run counts at all. Two of these
matter more than the rest:

- The **tier ratio** \(R_\text{phase}\) is the headline result. Stated per
  phase, because one end-to-end ratio would average the two Roofline regimes
  into a number describing neither.
- **Bandwidth utilisation** is the decisive diagnostic. A low tier ratio with
  low utilisation means concurrency was the limit and the tier never got a
  chance; a low tier ratio with high utilisation means the tier genuinely did
  not matter. Without it, a null result cannot be diagnosed.

Validity checks run *before* timings are looked at. Page residency is the one
that turns "we ran numactl" into evidence; output equivalence across tiers
catches defects that would otherwise read as findings.

---

## 28 August 2026 — literature review added, background reworked

The notes now carry a literature review rather than a four-paper corpus reading.
Part II was split: Section 4 (`04-literature-review.tex`) surveys the field
thematically, and Section 5 (`05-corpus-evidence.tex`, formerly
`04-paper-aurora-hbm.tex`) keeps the close reading of the four papers actually
measured on Xeon Max hardware. The renumbering moved methodology to
`06-thesis-methodology.tex`.

**Argument the review is built on.** CPU inference was made viable by
arithmetic-side work — quantization, cheaper kernels, better matrix-unit use —
and that line is now saturating. FairyFuse reports 29.6× at the kernel and
1.24× end to end; the gap between those two numbers is the memory wall, and it
is the pivot the review turns on. The memory-side response has strong measured
results in HPC and weak ones in inference, where the evidence is dominated by
simulation, accelerator-attached hierarchies, or results that required
rebuilding the runtime. A Xeon Max socket removes all three qualifications at
once. That is the thesis's position, and it is now argued rather than asserted.

**Additions to the platform sections.**

- A storage-level table covering L1 through remote memory, organised by *who
  decides what occupies each level*. It locates the thesis one row below the
  cache-resident work of Zhang et al.: that tier is not addressable, which is
  why they had to rebuild the runtime and this thesis does not.
- A subsection on Little's law (`sec:littles-law`). Sustaining 840 GB/s at
  135 ns needs ~113 KB in flight — about 32 cache lines per core across 56
  cores — against under 8 for DDR5. The faster tier demands roughly four times
  the memory-level parallelism before its bandwidth is reachable. This is the
  mechanism behind Peng et al.'s finding that latency-bound codes can run
  *slower* in MCDRAM, and it is what makes H1b a prediction rather than an
  excuse. Thread count became a first-class factor as a result.
- An AMX datapath figure showing that 4-bit weights cannot reach the matrix
  engine in their stored format. The unpack stage sits between the memory tier
  and the matrix unit, which is exactly the region under study.
- A subsection on why CRESCO8 specifically, and what its scarcity costs: 14
  shared nodes and a 24-hour limit rule out a Cartesian sweep, and the firmware
  memory mode is a constraint discovered at allocation time, not a variable.

**A Roofline figure** now plots both tiers on one chart with the decode and
prefill operating regions marked. Left of the ridge points the vertical gap
between the roofs is the full bandwidth ratio; right of them the roofs coincide
with the compute ceiling and placement cannot move the bound. It carries the
thesis argument in one picture and is the reason the two phases are measured
separately.

**Removed.** The opening of the old related-work section recorded a supplied
file being replaced with the correct preprint. That is project housekeeping and
does not belong in anything heading toward a thesis chapter; the corrected
citation stands on its own. The research-gap subsection was rewritten to state
the four questions in the order the evidence requires, and to name the three
nearest pieces of work and the axis each one misses.

**Still outstanding.** The search behind the review was web-first and
under-represents venue-only publications; repeat it against the ACM DL, IEEE
Xplore and the 2026 ISC/SC/IPDPS/ICS proceedings before freezing the proposal.
Several cited works are unrefereed preprints and are used for direction rather
than for quantitative claims. Figures were verified to compile with no overfull
boxes but have not been checked visually — no PDF rasteriser is installed.

---

## 26 July 2026

## Decision

The notes now form a coherent technical-background and experimental-rationale
document. The central argument is narrow enough for a thesis: compare verified
local HBM and local DDR5 on the same Xeon Max socket, then explain changes
through workload phase, live-set size, and placement. Claims about general CPU
superiority, whole-cluster performance, or energy efficiency are not supported
before measurement and have been excluded.

## What should remain central

1. **Locality and memory modes.** HBM capacity and bandwidth are local to a
   socket; Flat, Cache, Quadrant, and SNC4 change what software can address and
   how placement must be controlled.
2. **Prefill and decode are different experiments.** TTFT and inter-token
   latency cannot be replaced by one end-to-end throughput value.
3. **Capacity is a live-set property.** Model-file size alone does not establish
   whether weights, KV state, packed representations, and runtime allocations
   fit in a 64 GB local HBM tier.
4. **Bandwidth is a mechanism, not a predicted speedup.** STREAM supports a
   Roofline bound; it does not supply an LLM speedup ratio.
5. **Placement is part of the method.** Core binding, first touch, page
   residency, remote traffic, and run manifests are necessary for a causal
   HBM-versus-DDR comparison.

## Material reduced or removed

- Repeated relevance, caution, and open-question boxes were replaced by a
  single argument that progresses from hardware to evidence to method.
- Product-family options, cooling construction, storage details, and Slurm
  particulars were retained only where they affect measurement or
  reproducibility.
- Copied screenshots and paper figures were replaced by four original vector
  diagrams. A generic cluster schematic and small partition table were removed
  because prose and the node-class table already conveyed the useful facts.
  The old raster extracts remain in `figures/` as a working-source archive but
  are not referenced by, or required for, the reviewed PDF.
- The repeated phase-comparison and literature-role tables were removed after
  their useful distinctions were incorporated into the surrounding analysis.
- Implementation ideas were made conditional on a measured, reproducible
  baseline rather than presented as a predetermined contribution.

## Source and bibliography findings

The supplied file named `Lessons from HPL and HPL-MxP on Aurora.pdf` has now
been replaced with the intended Goto et al. preprint, arXiv:2604.09517v1.
Its title, authors, twelve-page extent, and deployment results were checked
against the local copy. References to the earlier file mismatch have been
removed.

The corrected paper adds one important concept to the notes: on Aurora, the
global HPL matrix remains in DDR because it exceeds CPU HBM capacity, while
tiles used by CPU-side panel operations are staged into HBM. This is a
production example of deliberate tiering. It is not evidence for an isolated
HBM speedup in CPU-only LLM inference because the run is GPU-dominated and the
staging policy was not ablated.

The paper also reports an HPL-MxP increase from 10.6 to 11.64 EF/s between
ISC24 and SC24 and identifies AMX enablement as the primary configuration
change. The notes retain this as operational evidence, not a controlled 9.8%
AMX effect: the paper explicitly says its impact classes are engineering
assessments rather than controlled ablations.

The Dongarra, Hoefler, and Matsuoka manuscript is recorded as an unpublished
2026 manuscript, not as a published *Communications of the ACM* article. The
bibliography is centralized in `bibliography/references.bib` so the same checked
records can be reused by the thesis.

Three transfer limits require particular care in the thesis. Na et al.'s
3.2--6.3× and 48-core results are workload averages, and its CPU--GPU result
reverses for the tested offloaded H100 in at least one larger-batch,
longer-prompt regime. Ibeid et al.'s full memory-mode matrix was measured on the
Borealis Xeon Max 9470C testbed, not production Aurora. The Dongarra et al.
manuscript combines measured A64FX results with specification-based projections
from an unpublished companion study. The revised notes now state these limits
where the results are introduced.

The public CRESCO8 page calls the machine a 793-node system while its three
listed node classes sum to 792. The notes report the discrepancy instead of
silently choosing a number. Scheduler inventory, installed DIMM topology,
memory and clustering modes, firmware, and usable HBM capacity must be captured
again on the actual run date.

## Thesis integration

- Use Part I as the basis of a short **Experimental platform** section. Keep the
  locality and HBM-mode figures; move the allocation script and full platform
  record to an appendix or reproducibility repository.
- Use Sections 3 and 4 as **Technical background** and **Related work**.
  Retain the correct Goto et al. citation and its tier-staging lesson, but omit
  the historical file-mismatch note from the thesis prose.
- Use Part III as the initial **Methodology** chapter. Replace predictions with
  a preregistered experiment matrix after pilot runs establish feasible models,
  precisions, repetitions, and counters.
- Do not copy operational counts or mode availability without a dated system
  manifest. Report the observed CRESCO8 configuration alongside the document
  version used.

The next scholarly step is not more background prose. It is a pilot allocation
that validates topology, memory placement, achievable HBM/DDR bandwidth, and
the runtime's ability to separate prefill from sustained decode.
