# Editorial review

## 11 September 2026 - LLM inference primer and fifth-pass review

### Outcome

Chapter 1 now begins at the reader's actual entry point: text is tokenized,
the model scores a next token, the decoding policy selects it, and that token
is fed back into the next step. Two author-drawn figures make the serial
generation loop and the lifetimes of weights, KV state, and temporary buffers
explicit. A stage-by-stage table then connects model loading, tokenization,
prefill, decode, sampling, and detokenization to the memory or runtime limit
each can plausibly create on a CPU.

The scope remains inference-only. Training, optimization objectives, datasets,
back-propagation, and parameter updates are deliberately absent. The learned
parameters enter the chapter as fixed input to the runtime. This is enough to
define an LLM operationally for the thesis without adding a detached machine-
learning survey.

### Detailed content review

The former opening of the performance-model section assumed that the reader
already understood tokens and autoregressive generation. It also introduced
weights and KV state only immediately before their capacity equations. The new
order resolves that dependency: token sequence, next-token distribution,
decoder loop, transformer blocks, tensor lifetimes, pipeline stages, and only
then the cluster and hardware on which those stages execute. The quantitative
section no longer repeats the transformer description.

The older prefill/decode dataflow figure was removed after the rendered-page
review. Its relationships are now carried by the richer tensor-lifetime figure,
while the later performance-model subsection retains the phase-specific
parallelism, metrics, and caveats. Keeping both figures would have repeated the
same prompt-to-decode path without teaching a second concept.

The primer includes scaled dot-product attention because it explains why keys
and values exist and why retaining them avoids processing the complete prefix
again at every decode step. It does not enumerate architecture families or
derive every transformer component; those details do not change the memory-
placement argument. Likewise, sampling is explained only far enough to place
it inside the user-visible latency boundary.

The phrase "memory bottleneck" has been decomposed into three non-equivalent
conditions. Capacity pressure concerns whether simultaneously live weights,
KV state, activations, and runtime copies fit. Bandwidth pressure concerns the
sustained delivery rate of repeatedly accessed bytes. Latency or runtime
pressure concerns an inability to issue enough useful work to approach that
rate. Only bandwidth pressure predicts a proportional gain from HBM, so the
chapter now states that causal requirement before presenting the hardware.

Several qualifications prevent common overclaims:

- prefill has greater parallelism than low-batch decode, but is not declared
  universally compute-bound;
- KV memory grows with context and concurrency, but its access cost depends on
  attention type and runtime implementation;
- model file size is separated from the resident weight representation;
- tokenization, sampling, and detokenization remain inside end-to-end latency
  but are not attributed to the memory tier without evidence; and
- accelerator papers are used to establish tensor lifetimes, traffic, and
  fragmentation mechanisms, not to predict a CPU speedup.

### Literature additions and balance

Four primary sources were added. Vaswani et al. provide the transformer and
scaled dot-product attention foundation. Pope et al. connect generative
inference to weight and KV-cache traffic. FlexGen supplies the explicit
weights/activations/KV placement taxonomy across a memory hierarchy.
PagedAttention establishes that KV allocation and fragmentation can constrain
usable capacity independently of raw tensor size. The related-work chapter now
states why these accelerator-oriented results are informative and where their
transfer ends; CPU-specific phase claims remain grounded in Na et al. and the
existing CPU literature.

This is close to the maximum useful amount of general LLM explanation for this
thesis. Additional material on training, model quality, prompt engineering,
alignment, encoder-only models, or a taxonomy of sampling methods would not
help answer the placement questions. If Chapter 1 later needs shortening, the
sampling-policy examples and the textual metric definitions can be compressed;
the tensor-lifetime figure and pipeline table should remain because they carry
the bridge from LLM concepts to the experimental intervention.

### Build and visual QA

The revised thesis builds successfully with the repository's Tectonic task and
two citation reruns. The output is a 65-page A4 PDF. The final log contains no
overfull boxes, undefined citations, undefined cross-references, duplicate
labels, or multiply defined destinations. The remaining underfull-box messages
are the already known title-page and bibliography warnings.

The five-page primer, the transition into the HPC material, the revised
performance-model opening, and the added related-work paragraph were rendered
and inspected at page scale. Both new figures and the four-column pipeline
table are legible and stay inside the text block. Float barriers keep the
pipeline figure and table within their own section; without them, an early
render allowed the table to appear after the following HPC subsection had
started.

## 11 September 2026 - migration into the thesis and fourth-pass review

### Outcome

The technical notes have graduated into the thesis source tree. The rendered
document now has four draft body chapters and one appendix:

1. **Theoretical and Technical Background**: cluster-to-socket scope, Xeon Max
   architecture and memory modes, and the phase-resolved inference model.
2. **Experimental Platform**: CRESCO8's documented configuration, operational
   constraints, and the observations that must be repeated on the allocated
   node.
3. **Related Work and Research Gap**: thematic literature review followed by a
   close reading of the Xeon Max evidence and the four research questions.
4. **Methodology**: decision-gated experiment design, factors, controls,
   statistical analysis, validity threats, and the conditional implementation
   contribution.
5. **Reproducibility Checklist**: the Slurm topology-capture skeleton and the
   minimum platform manifest, moved out of the argumentative chapters.

The abstract is now a one-sentence placeholder. The title-page metadata,
advisor, author, course, academic-year, dedication, and acknowledgements were
not edited. The old standalone notes driver and notes build target were removed;
`research/notes/` is intentionally empty.

### Structural review

The former notes document was coherent as a research notebook but too broad as
one thesis chapter. It mixed four different scholarly jobs: teaching the
hardware concepts, documenting the particular machine, positioning the work,
and specifying the experiment. Separating those jobs produces a clearer chain:

    memory and workload theory
      -> observed platform
      -> prior evidence and gap
      -> controlled test

Chapter 1 is still substantial at 23 body pages, but it now contains material
needed to understand the intervention. The platform-specific chapter is four
pages, related work is twelve, methodology is six, and the reproducibility
appendix is two. This is a reasonable first draft balance. If Chapter 1 grows
again, the first candidate for extraction is the detailed metric taxonomy, not
the memory hierarchy or the prefill/decode model.

The standalone HPC primer was more elementary than the rest of the text and
made claims that were too absolute. It has been shortened and reframed around
the only boundary the thesis needs: a shared address space within a NUMA node
versus explicit communication between nodes. The unsupported numerical claim
that crossing the network is "roughly three orders of magnitude" slower was
removed. The claim that cluster experiments necessarily run without an
interactive allocation was also corrected: CRESCO8 documents interactive Slurm
sessions, while this thesis chooses batch execution for reproducibility.

The hardware section read partly like a product tour. The front-panel image,
enclosure image, and cooling-manifold image were removed from the rendered
chapter. The internal server photograph remains because it shows the physical
socket/DIMM locality that the experiment manipulates. The unused assets remain
under `thesis/figures/` as source material and can be deleted later if the
repository should contain only published figures.

The topology-capture shell script and platform-record table interrupted the
platform argument. They now live in Appendix A, where they are available for
reproduction without being mistaken for theoretical content.

### Technical-content review

The notes began the inference model with prefill and decode, assuming the reader
already understood which transformer state is persistent and which grows. A new
short subsection now explains the only transformer internals needed here:
weights are read-only and reused, KV state grows per sequence, and activations
and workspaces are implementation-dependent. This supplies the missing bridge
to object-level tier placement without expanding into a generic transformer
tutorial.

The Roofline discussion previously placed low-batch decode and prefill in fixed
regions of the chart. That was too categorical. The revision treats those
positions as workload-dependent hypotheses and requires the actual operating
points to be estimated from the chosen model, batch, prompt, precision, and
kernel counters.

TTFT was previously treated as a pure prefill metric and prefill throughput was
defined as prompt tokens divided by TTFT. That is not exact: TTFT also includes
the first decode step and any overhead inside the declared request boundary.
The thesis now distinguishes the runtime's direct prompt-evaluation timer from
TTFT and defines prefill throughput from the former.

The bandwidth-utilisation discussion made an overstrong causal inference from
a low achieved HBM bandwidth. Low utilisation rules out saturation of HBM's
bandwidth ceiling, but it does not uniquely identify insufficient concurrency;
latency and runtime overhead remain alternatives. Both the metric table and the
Little's-law discussion now state the weaker, defensible conclusion.

The literature review used the 29.6x kernel versus 1.24x end-to-end FairyFuse
result as proof that arithmetic had ceased to matter. The source supports those
two numbers, but their difference can include unchanged operators and runtime
overhead as well as data movement. The revision uses the result as evidence of
diminishing system-level returns and as motivation to measure traffic, not as
proof of a single bottleneck.

The HBM-only description was reconciled across chapters. Lenovo documents
HBM-only on a system without installed DDR5, while project-specific operational
guidance suggests CRESCO8 may expose a state in which populated DDR5 is
unavailable. The thesis now separates the observable condition from its
site-specific implementation and requires the mechanism to be recorded rather
than inferred.

The public CRESCO8 inventory has been dated explicitly to the operational page's
1 July 2025 update. The page still reports 793 nodes while its listed classes sum
to 792 and its core total matches 792; the thesis retains this discrepancy and
requires a dated scheduler manifest instead of silently choosing a count.

### Methodology and statistical review

The research-gap section listed four questions while the methodology table
listed three. They are now consistent: RQ1-RQ3 define the core empirical study;
RQ4, independent weight/KV placement, is conditional on first observing both a
repeatable tier effect and a capacity constraint.

The validity table previously said that every failed check caused a run to be
discarded and included a coefficient-of-variation threshold among those checks.
That would permit high-variance or small-effect observations to be removed after
seeing the data. The revision separates technical run invalidation from
study-level precision. Placement, affinity, output-equivalence, and predeclared
throttling failures may invalidate a run. High variance instead produces more
sampling or a wider uncertainty interval; it is never a reason to delete an
inconvenient result.

Tokens from one autoregressive request are not independent replications. The
method now defines a randomized or counterbalanced HBM-DDR run pair on a named
node as the independent unit for the tier effect. Confidence intervals resample
paired runs and preserve request-level grouping for within-run latency
distributions. This prevents thousands of correlated token timings from
creating a falsely narrow interval.

The related-work comparison table had described this thesis as "measured" even
though the campaign has not run. It now says "planned hardware evaluation" and
keeps the unmodified runtime and residency checks as requirements rather than
results.

### What is intentionally not written yet

- The abstract remains a placeholder until results and conclusions exist.
- The front-page title and institutional metadata remain exactly as supplied.
- No results, discussion, or conclusion chapter has been invented before the
  campaign.
- A conventional introductory chapter has not been added because the current
  request defines Chapter 1 as the theoretical chapter. Before submission, the
  university's expected chapter order should be checked; a concise introduction
  will probably be needed once the contribution can be stated from evidence.

### Remaining scholarly work

The prose is internally coherent, but several items cannot be finalized without
the first pilot allocation:

- active memory and clustering modes, NUMA node numbering, usable HBM capacity,
  DIMM population, and whether HBM-only can be exposed on populated nodes;
- the exact `llama.cpp` commit, compiler, build flags, quantized format, model
  revisions, prompt corpus, and context/batch levels;
- the practical page-residency threshold, available HBM/DDR/UPI counters, and
  counter collection overhead;
- pilot variance, the target confidence-interval width, number of independent
  run pairs, warm-up count, and node-to-node replication;
- permission to reproduce the remaining Lenovo photograph and diagrams, or a
  decision to replace them with author-drawn equivalents; and
- a systematic literature search across ACM DL, IEEE Xplore, and the relevant
  2026 conference proceedings before making any priority or novelty claim.

The document is therefore ready to serve as the theoretical, platform,
related-work, and methodological draft, but it is not yet evidence for a thesis
conclusion. The next substantive step is the pilot allocation and the freezing
of the preregistered experiment matrix.

### Build and visual QA

The migrated thesis builds successfully with the repository's Tectonic task and
two citation reruns. The output is a 60-page A4 PDF. The final log contains no
overfull boxes, undefined citations, undefined cross-references, duplicate
labels, or multiply defined PDF destinations. Two underfull-box messages come
from the unchanged title page and one from a bibliography entry; visual
inspection shows no clipping or malformed layout at those locations.

All pages were rendered to raster previews and reviewed as contact sheets. The
dense pages were then checked at higher resolution: the Xeon topology figures,
STREAM chart, three multipage metric tables, CRESCO8 inventory table,
methodology tables, listing, appendix table, and bibliography are legible and
remain inside the text block. Temporary render files were removed after the
review; the final artifact remains at `build/thesis.pdf`.

---

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
