# Editorial review

Date: 26 July 2026

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
  The old raster extracts remain in `images/` as a working-source archive but
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
bibliography is centralized in `thesis/references.bib` so the same checked
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
