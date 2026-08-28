# Candidate literature

Result of a targeted literature search (28 August 2026) against the four
research questions in `research/analysis/sections/04-gaps.tex`. This file is a
**shortlist to read and triage**, not a bibliography — entries graduate into
`references.bib` once they have been read and are actually cited.

Nothing here was selected for being "about LLMs" or "about HPC". Every entry
earns its place by doing one of three specific jobs:

| Job | Meaning | Where it lands in the thesis |
|---|---|---|
| **Baseline** | Reports numbers on comparable hardware/runtime that our results can be put next to. | Results & discussion chapter, comparison tables. |
| **Foundation** | Establishes a claim, method, or model we build on or argue against. | State of the art / literature review chapter. |
| **Method** | Constrains how we must measure and report. | Methodology chapter, threats to validity. |

**Verification column (`V`)**: ✔ = abstract fetched and checked directly;
○ = from search results only, **confirm before citing**. Many 2026 entries are
arXiv preprints — check for a refereed version before the final bibliography.

---

## 1. Confrontation baselines — papers we can put our numbers against

These are the ones that matter most for your stated goal ("we beat this paper,
we get beaten by that one"). All of them either use `llama.cpp` as a baseline,
run on Sapphire-Rapids-class Xeon, or report CPU-side prefill/decode throughput.

| V | Paper | Link | What it does | What we confront it with |
|---|---|---|---|---|
| ✔ | **Cache-Resident LLM Inference in GB-Scale Last-Level Caches** — Zhang, Gu, Canini, Xu, Weng (Jun 2026) | [arXiv:2606.25353](https://arxiv.org/abs/2606.25353) | Cache-resident execution model on a **multi-socket CPU cluster**: decouples weight-centric operators from attention/KV management into separate resource domains, keeps weights in a GB-scale LLC, scales KV independently. Baseline is **`llama.cpp` at equal resource provisioning**; reports **2.04×–11.51× TPOT** for Llama-3.2-3B and Llama-2-7B. | **The single most important paper on this list.** It makes exactly our thesis argument — CPU LLM inference is dominated by data movement, and the fix is placing the reusable weight stream in a faster tier — but chooses **SRAM (LLC)** as that tier where we choose **HBM**. Confrontation: their gain requires a redesigned runtime and a decoupled architecture; ours (RQ1) is the *unmodified-runtime, placement-only* delta. Their TPOT numbers are the ceiling our HBM result should be reported against. Also directly pressures RQ4: they already show weight/KV separation pays off, which raises the bar for our selective-tiering contribution. |
| ✔ | **FairyFuse: Multiplication-Free LLM Inference on CPUs via Fused Ternary Kernels** — Zuo, Xi, Zeng, Wang, Leung (Apr 2026) | [arXiv:2604.20913](https://arxiv.org/abs/2604.20913) | Ternary weights, eight sub-GEMVs fused into one AVX-512 loop with masked add/sub. **Intel Xeon 8558P**, baseline **`llama.cpp` Q4_K_M**: 29.6× kernel-level, **1.24× end-to-end, 32.4 tok/s**, ppl 5.52 vs 5.47 FP16. | The cleanest "compute-side lever" counterpoint. Note the gap between 29.6× kernel and 1.24× end-to-end — that collapse *is* the memory wall, and it is our argument's best borrowed evidence. Confrontation: if our DDR→HBM placement delta on decode exceeds 1.24× with **zero kernel changes**, that is a strong positioning claim. If it does not, the honest framing is that the memory-side lever and the compute-side lever are complementary and roughly comparable in size. |
| ✔ | **Which Quantization Should I Use? A Unified Evaluation of `llama.cpp` Quantization on Llama-3.1-8B-Instruct** — Kurt (Jan 2026) | [arXiv:2601.14277](https://arxiv.org/abs/2601.14277) | Unified sweep of 3–8 bit K-quant and legacy GGUF formats: downstream task accuracy, perplexity, **CPU prefill and decode throughput**, model size, compression ratio, quantization time. | Same runtime, same quantization family, same phase decomposition as us. Use it to **justify the choice of quantization level** in the methodology rather than defending it ad hoc, and to bound the quality cost of whatever GGUF format we standardise on. Its CPU throughput table is a per-format baseline our Xeon Max numbers slot into. (Hardware not stated in the abstract — read the PDF and record the exact CPU before using its numbers comparatively.) |
| ○ | **Deploying LLMs on CPU-only Environments with `llama.cpp`: MedLocalGPT Project Case** — CEUR-WS Vol-4164, paper 11 (Feb 2026) | [ceur-ws.org/Vol-4164/paper11.pdf](https://ceur-ws.org/Vol-4164/paper11.pdf) | Seven instruction-tuned models (1B–24B) at 4-bit GGUF across three CPU environments, including a **Xeon Platinum 8480+**: ~120 tok/s (Llama-3.2-1B), ~45 tok/s (Qwen2.5-7B), ~15 tok/s (Mistral-24B); ~25/8/2 tok/s on an older E5-2695 v2. | **The 8480+ is the DDR-only sibling of our 9480** — same Sapphire Rapids generation, same core count class, no HBM. That makes it the closest thing in the literature to a published control for RQ1. Their numbers are the "what a Sapphire Rapids socket does without HBM" reference; ours are "the same socket with the tier isolated". Verify the exact SKU, memory configuration, thread count, and `llama.cpp` build before using it as a quantitative control — the comparison is only as good as those details. |
| ✔ | **Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers (THInfer)** — Lu, Luan, Li, Qi, Ma, Han, Shang, Yang, Qian (May 2026) | [arXiv:2605.25655](https://arxiv.org/abs/2605.25655) | Inference framework for the **MT-3000 (Tianhe)** VLIW-SIMD many-core processor: hand-tuned operator library, density-driven graph fusion, and a **Prefill–Buffer–Decode pipeline** with bounded buffers. Beats DeepSpeed on 2×V100S by 62–73% (7B) and an A800 by 67–84%; runs 70B where GPU frameworks fail. | The strongest existing "non-GPU supercomputer runs LLM inference competitively" result, and it is framed explicitly as a **bandwidth-constrained locality problem** — our framing. Use it in the literature review to establish that the thesis question is live in HPC, not just a local-inference curiosity. Confrontation: they win by co-designing the runtime to the memory system; we ask how much is available from *placement alone* on commodity Xeon. Their P-B-D pipeline is also a concrete design to cite if RQ4 turns into an implementation. |
| ✔ | **Efficient LLM Inference on CPUs** — Shen, Chang, Dong, Meng, Luo (Intel), NeurIPS 2023 ENLSP | [arXiv:2311.00502](https://arxiv.org/abs/2311.00502) | Automatic INT4 weight-only quantization plus a tuned CPU LLM runtime. **20–80 ms per generated token for 6B–20B models on a single 4th-gen Xeon socket**, within 1% of FP32 accuracy. | The canonical single-socket Sapphire Rapids latency reference, and the origin of the "one socket is enough" claim that our single-socket RQ1 design inherits. Use as the earliest anchor in the CPU-inference narrative and as a sanity band for our own ITL numbers. |
| ✔ | **T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge** — Wei, Cao, Cao, Ma, Wang, Zhang, Yang, **EuroSys 2025** | [arXiv:2407.00088](https://arxiv.org/abs/2407.00088) | Lookup-table mpGEMM with no dequantization and no multiplications. Baseline **`llama.cpp`**: up to **4× throughput, 70% less energy**; BitNet-b1.58-3B at 71 tok/s on M2-Ultra (8 cores), 11 tok/s on a Raspberry Pi 5. | Refereed, `llama.cpp`-baselined, and the reference point for "how big a CPU inference speedup gets published". Note that its best platform, **M2-Ultra, is itself a wide unified-memory machine** — an implicit argument that memory bandwidth is the CPU-inference lever, which we make explicitly and with the tier isolated. Its energy result is the model to follow if the energy extension goes ahead. |
| ○ | **KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models** — Chen et al., **SOSP 2025** | [dl.acm.org/10.1145/3731569.3764843](https://dl.acm.org/doi/10.1145/3731569.3764843) · [PDF](https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/SOSP25-chen.pdf) | AMX-specialised CPU kernels plus asynchronous CPU–GPU scheduling for large MoE (DeepSeek-V3/R1 671B): **4.62–19.74× prefill, 1.25–4.09× decode** over prior hybrid systems. | The refereed statement of "the CPU side of inference is bounded by CPU memory and compute, not by the GPU". Use it to motivate why improving the CPU memory path matters even in GPU-attached deployments — this widens the thesis's relevance beyond CPU-only clusters without requiring us to run a GPU comparison. |
| ✔ | **CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU–GPU Co-Execution** — Son, Chen, Yoo, Choi, Kim, **DAC 2026** | [arXiv:2605.17889](https://arxiv.org/abs/2605.17889) | Coalescing-aware batching and expert stratification across an AMX CPU and a GPU; up to **7.1× over FlexGen, 2.4× over MoE-Lightning**. | Secondary. Useful as evidence that AMX-class CPUs are now a first-class part of serving pipelines, and as a citation for why AMX kernel coverage in `llama.cpp` is worth auditing. Not a direct baseline — different workload class and a hybrid setup. |
| ○ | **TriMoE: Augmenting GPU with AMX-Enabled CPU and DIMM-NDP for High-Throughput MoE Inference via Offloading** — (Mar 2026) | [arXiv:2603.01058](https://arxiv.org/abs/2603.01058) | Three-way split across GPU, AMX CPU, and near-data processing in DIMMs. | Optional. Cite only if the thesis discusses where CPU-side memory-tier placement sits relative to near-data processing as an alternative answer to the same bandwidth problem. |

---

## 2. Our hardware, without LLMs — the HBM/DDR evidence base

These are what let you claim in Chapter 2 that the HBM-versus-DDR question has a
serious prior literature, and what set the *expected* size of the effect before
any LLM is involved.

| V | Paper | Link | What it does | What we take from it |
|---|---|---|---|---|
| ✔ | **Comparative Evaluation of Bandwidth-Bound Applications on the Intel Xeon CPU MAX Series** — Reguly (Sep 2023) | [arXiv:2309.09084](https://arxiv.org/abs/2309.09084) | One of the first independent studies of the **Xeon CPU MAX 9480** on bandwidth-sensitive HPC proxies and applications, against Ice Lake and Milan-X (3D V-Cache). **2.0×–4.3×** over the previous generation; for some codes the bottleneck **shifts from bandwidth to communication latency**. | **Our exact CPU.** This is the reference for what HBM is worth on this silicon for bandwidth-bound work, and therefore the yardstick our LLM result is measured against: an LLM decode speedup well below 2.0× is a finding that needs explaining, not a failure. The bottleneck-shift observation is the direct precedent for hypothesis **H1b** — the achieved ratio falls short of the STREAM ratio because something other than streaming becomes limiting. The Milan-X comparison also connects this literature to the LLC-tier argument in arXiv:2606.25353. |
| ✔ | **Exploring the Performance Benefit of Hybrid Memory System on HPC Environments** — Peng, Gioiosa, Kestor, Laure, Markidis, **IPDPSW 2017** | [arXiv:1704.08273](https://arxiv.org/abs/1704.08273) | KNL MCDRAM + DRAM. Regular access patterns gain **up to 3× over DRAM-only**; **irregular patterns are latency-bound and can be *slower* in MCDRAM-only**; more hardware threading recovers bandwidth utilisation for random access. | The historical foundation of the whole flat-mode-placement method, and — more usefully — a **pre-registered prediction for our own null result**. It states the mechanism by which a high-bandwidth tier fails to help: latency-bound, low-concurrency access. Low-batch decode is exactly that shape. Cite it when framing H1a/H1b, and again in the discussion whichever way the result falls. It also justifies reporting thread/concurrency sweeps rather than a single thread count. |
| ○ | **Evaluating Emerging CXL-Enabled Memory Pooling for HPC Systems** — (Nov 2022) | [arXiv:2211.02682](https://arxiv.org/abs/2211.02682) | Characterisation of CXL-attached memory pools for HPC workloads. | Background for the "tiered memory is now normal in HPC" paragraph. Keeps the thesis from reading as though HBM/DDR were the only tiering story. Low priority. |
| ○ | **The Hitchhiker's Guide to Programming and Optimizing Cache Coherent Heterogeneous Systems: CXL, NVLink-C2C, and AMD Infinity Fabric** — (Nov 2024) | [arXiv:2411.02814](https://arxiv.org/abs/2411.02814) | Measurement methodology and pitfalls for cache-coherent heterogeneous memory. | **Methodological**, more than topical. Useful for how to measure and report loaded latency, achieved bandwidth, and remote-access counters credibly — the exact instrumentation RQ1 and RQ3 depend on. |

---

## 3. Placement of weights and KV across memory tiers — RQ2 and RQ4

This is the cluster that most directly threatens (and most sharply defines) the
novelty of RQ4. Read these before committing to the selective-tiering contribution.

| V | Paper | Link | What it does | What we take from it |
|---|---|---|---|---|
| ✔ | **Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System** — Fang, Xie, Haq, Ma, El Maghraoui, Wang, Wang, Liu, Zhang (Aug 2025, rev. Sep 2025) | [arXiv:2508.13231](https://arxiv.org/abs/2508.13231) | Formalises **dynamic KV cache placement across HBM + high-speed off-package DRAM** as an optimisation problem, derives theoretical bounds, and shows large headroom over current practice. Explicitly framed around accelerators integrating HBM with off-package DRAM (NVLink/LPDDR5X). | **The closest published relative of RQ4, and the reason to read it first.** It provides the formal model and the vocabulary for the weights-vs-KV split, so we do not have to invent either. It is also where our contribution differentiates: it is **theoretical and accelerator-side**, whereas RQ4 is an **empirical, CPU-side, real-hardware** result on `llama.cpp` with verified page residency. Frame RQ4 as supplying the measurement their bound predicts, and report our numbers against their headroom claim. |
| ✔ | **ITME: Inference Tiered Memory Expansion with Disaggregated CXL-Hybrid Memories** — Jang, Min, Kim, Ahn, Kim, Joo, Kim, Kim (Jun 2026) | [arXiv:2606.12556](https://arxiv.org/abs/2606.12556) | Host DRAM → CXL-hybrid memory → NVMe tiering for KV cache and weights, exploiting the **deterministic access pattern of weights and prefix caches**; **+35.7% throughput** at TB scale. | The "what happens past the capacity cliff" paper, which is precisely **RQ2**. Its key transferable idea is that *weights and prefix state are predictable enough to place statically, while the rest is not* — the same asymmetry that motivates our weights-in-HBM / KV-in-DDR policy. Confrontation: their capacity direction is outward (expand beyond host memory); ours is inward (fit inside a small, very fast tier). Both hit the same boundary from opposite sides. |
| ✔ | **A CXL Memory Rack for Multi-Turn LLM Serving (HyMCache)** — Jang, Song, Kim, Noh, Kim (Jul–Aug 2026) | [arXiv:2607.18141](https://arxiv.org/abs/2607.18141) | Three-tier GPU HBM → CXL-HM DRAM → SSD stack for multi-turn KV reuse; **3.0× over local LMCache**, 1.45× disaggregated, 16× less DRAM than distributed-DRAM Mooncake at ~30% performance cost. | Use for the discussion, not the core. It is the strongest available statement that **KV state is worth managing across tiers explicitly**, which supports RQ4's premise; and its DRAM-versus-performance trade curve is a good model for how to present our own HBM-capacity-versus-performance results in RQ2. |
| ○ | **From Tensor Buffer to Distributed Memory Hierarchy: A Survey of KV Cache Management for LLM Serving** — (Jul 2026) | [arXiv:2607.02574](https://arxiv.org/abs/2607.02574) | Survey of KV cache management across the memory hierarchy. | **Highest-leverage single read for the literature review chapter.** A recent survey gives you the taxonomy, the standard terminology, and a large citation set for free. Use it to structure the KV-management section and to harvest further references — but cite the primary works for any specific claim. |
| ○ | **Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference** — (Apr 2026) | [arXiv:2604.26968](https://arxiv.org/html/2604.26968) | Argues current systems wrongly confine KV to a single tier despite an available hierarchy (GPU HBM, CPU DRAM, CXL, NVMe, RDMA, PFS). | One clean citation for the framing sentence "confining state to one memory tier is a design choice, not a necessity". Read the abstract; probably nothing more. |

---

## 4. Why decode is memory-bound — the model behind H1a and H1b

| V | Paper | Link | What it does | What we take from it |
|---|---|---|---|---|
| ○ | **LLM Inference Unveiled: Survey and Roofline Model Insights** — Yuan et al. (Feb 2024, rev. v4) | [arXiv:2402.16363](https://arxiv.org/abs/2402.16363) | Survey of inference efficiency built on an explicit **roofline analysis** of LLM inference, with a released analysis tool. | The bridge between Williams' roofline (already in `references.bib`) and the LLM-specific arithmetic-intensity argument. This is the standard citation for "low-batch decode sits far left on the roofline", which is the entire justification for H1a. Cite it wherever the thesis asserts that decode has lower arithmetic intensity than prefill. |
| ✔ | **Memory-Bound but Not Bandwidth-Limited: The Physical AI Inference Gap in Batch-1 LLM Decode** — Chen (May 2026) | [arXiv:2605.30571](https://arxiv.org/abs/2605.30571) | 44-cell study across H100 / A100 / L40S / L4 on 7–8B GQA models. Batch-1 decode is memory-*dominated*, but **faster memory does not give proportional latency gains**: 81% of peak bandwidth utilisation on an L4 versus **27% on an H100**. Launch overhead (CUDA Graphs: 1.26× on H100) and quantized kernel choice matter more than raw bandwidth. | **The single best independent support for H1b, and the most useful paper here for keeping a null result publishable.** It says a big bandwidth ratio need not produce a proportional speedup, and names the reasons: overhead-bound execution and poor bandwidth utilisation on the wider-memory part. Directly predicts that a 4–5× HBM/DDR STREAM ratio may yield far less decode gain. Caveat: it is GPU-side, so cite it as a mechanism and an expectation, not as a comparable measurement. |
| ✔ | **RooflineBench: A Benchmarking Framework for On-Device LLMs via Roofline Analysis** — Bi, Chen, Sun, Yao, Shen, Lou, Deng (Feb 2026, rev. Aug 2026) | [arXiv:2602.11506](https://arxiv.org/abs/2602.11506) | Systematic roofline-based benchmarking of small LMs across compute tiers; introduces **Relative Inference Potential**; shows operational intensity varies with sequence length and model depth; names an "efficiency trap" from hardware heterogeneity. | A ready-made **methodology** for turning our measurements into roofline positions rather than bare tok/s. Its finding that operational intensity moves with sequence length is exactly the mechanism behind the RQ2 capacity/context sweep, and gives us a principled way to choose sweep points instead of arbitrary ones. |
| ✔ | **Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles** — Arif, Maurya, Vazhkudai, Nicolae, **ISCA 2026** (industry track) | [arXiv:2605.19775](https://arxiv.org/abs/2605.19775) | 8B–671B on GPU clusters. Reasoning workloads shift inference into a **capacity-bound regime**; identifies a data-parallel "capacity trap" driven by **KV-cache fragmentation**; tensor parallelism unlocks stranded memory with sublinear gains near ~32B. | Refereed vocabulary for RQ2. "Capacity-bound regime" and "capacity trap" name the transition we are trying to locate, and the fragmentation mechanism is a concrete alternative explanation to test before attributing a cliff to tier capacity. Also relevant to RQ3: their parallelism trade-offs are the GPU analogue of our socket/SNC placement policies. |
| ○ | **Prefill vs. Decode Bottlenecks: SRAM–Frequency Trade-offs and the Memory-Bandwidth Ceiling** — (Dec 2025) | [arXiv:2512.22066](https://arxiv.org/abs/2512.22066) | Once decode is memory-bound, raising frequency yields little latency reduction. | A short, quotable statement of the ceiling effect. Useful as a supporting citation when arguing that on this hardware the memory tier, not the clock or the core count, is the variable worth manipulating. Verify before citing. |

---

## 5. How we are required to measure — methodology chapter

| V | Paper | Link | What it does | What we take from it |
|---|---|---|---|---|
| ✔ | **On Evaluating Performance of LLM Inference Serving Systems** — Agrawal, Kedia, Agarwal, Mohan, Kwatra, Kundu, Ramjee, Tumanov (Jul 2025) | [arXiv:2507.09019](https://arxiv.org/abs/2507.09019) | Catalogues evaluation anti-patterns across **baseline fairness** (conflating engineering effort with algorithmic novelty), **setup** (unrepresentative workloads), and **metric design** (normalised metrics hiding generation stalls), with a checklist. | **Cite this in the methodology and then actually follow it.** It is the defence for our comparison design: matched build, matched thread count, matched model and quantization, with only the memory tier varying. Its warning about normalised metrics hiding variability is why we must report ITL distributions and not just mean tok/s. It also pre-empts the obvious examiner question of why we do not compare against a GPU. |
| ✔ | **Meta-Metrics and Best Practices for System-Level Inference Performance Benchmarking (FMwork)** — Salaria, Liu, Mimura Gonzalez (Aug 2025) | [arXiv:2508.10251](https://arxiv.org/abs/2508.10251) | Metrics for the **cost of benchmarking itself** and for how closely a sampled sweep approximates the full experimental space; up to 24× saving; e.g. 1024→128 output tokens keeps 96.6% accuracy at 2.7× less cost. | Practical and immediately usable on a shared allocation. It gives a **defensible, citable justification for a reduced sweep** — how many prompt/generation lengths, how many repetitions — instead of either an exhaustive grid we cannot afford or an arbitrary subset a reviewer can attack. |
| ✔ | **Bench360: Benchmarking Local LLM Inference from 360 Degrees** — Stuhlmann, Fadel Argerich, Fürst (Nov 2025, rev. Jan 2026) | [arXiv:2511.16682](https://arxiv.org/abs/2511.16682) | Benchmarks local inference across tasks, usage patterns, engines, and quantizations, reporting latency, throughput, **energy**, and startup time together; concludes there is no configuration that wins everywhere. | A template for the shape of our results chapter: multiple metrics side by side, configuration-dependent conclusions, no single winner. Also the model to follow for the energy extension. Its scope is GPU, so use it for **structure and reporting practice**, not for numbers. |

---

## 6. Positioning and contrast — cite sparingly

Useful for the introduction and for answering "why not just use a GPU", but not
part of the core argument. Do not let these expand the scope.

| V | Paper | Link | Why it might be worth one sentence |
|---|---|---|---|
| ✔ | **Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective** — Li et al. (Oct 2024, rev. Jun 2025) | [arXiv:2410.04466](https://arxiv.org/abs/2410.04466) | Cross-platform survey (CPU / GPU / FPGA / ASIC / PIM-NDP) with **tokens/s and tokens/joule at batch 1 and 8**. The one citation that lets you place CPU inference on a hardware landscape in a single sentence, and the natural source for the energy-efficiency framing if the energy extension goes ahead. |
| ○ | **Characterizing and Optimizing LLM Inference Workloads on CPU–GPU Coupled Architectures** — (Apr 2025, ISPASS) | [arXiv:2504.11750](https://arxiv.org/abs/2504.11750) | Closely- vs loosely-coupled CPU–GPU (GH200): 1.9×–2.7× faster prefill at large batch. Evidence that the CPU-side memory path is a first-order term even in GPU systems. |
| ✔ | **DAK: Direct-Access-Enabled GPU Memory Offloading** — Lin, Guo, Lin (Apr 2026) | [arXiv:2604.26074](https://arxiv.org/abs/2604.26074) | The GPU-side mirror of our question: fetch weights and KV directly from a slower remote tier instead of staging into HBM. Up to 3× on NVLink-C2C. Good for one contrast sentence — the field is converging on explicit tier-aware data movement on both sides of the CPU/GPU line. |
| ○ | **Understanding and Improving Communication Performance in Multi-node LLM Inference** — (Nov 2025) | [arXiv:2511.09557](https://arxiv.org/abs/2511.09557) | Only if the thesis needs to justify **excluding** multi-node from scope; it shows how many new variables that would add. |
| ○ | **NoMAD-Attention: Efficient LLM Inference on CPUs Through Multiply-Add-Free Attention** — **NeurIPS 2024** | [arXiv:2403.01273](https://arxiv.org/abs/2403.01273) | SIMD-register lookups instead of MAD in attention; **2× on 4-bit LLaMA-7B at 16k context**, no fine-tuning. Refereed, and the long-context result makes it a useful contrast for RQ2: they attack attention cost algorithmically where we attack KV-state placement. |
| ✔ | **Distributed Inference Performance Optimization for LLMs on CPUs** — He et al., ICLR 2024 workshop | [arXiv:2407.00029](https://arxiv.org/abs/2407.00029) | 72B at 140 ms/token on 5th-gen Xeon via distributed CPU inference. The precedent for **RQ3**: scaling CPU inference past one socket is an established practice, so our negative control (unmanaged cross-socket) is testing something the field actually does. |

---

## 7. Coverage against the research questions

| Research question | Prior work that constrains it | Status after this search |
|---|---|---|
| **RQ1** — local HBM vs local DDR, phase-resolved, one Xeon Max socket | 2309.09084 (our CPU, non-LLM); 1704.08273 (mechanism); 2605.30571 (H1b); 2402.16363 (H1a); Na et al. 2024 | **Survives.** No paper found that isolates a verified HBM/DDR placement for quantized `llama.cpp` on Xeon Max with prefill/decode separated. |
| **RQ2** — capacity and KV boundary | 2605.19775 ("capacity trap", fragmentation); 2606.12556 (ITME); 2607.18141; 2602.11506 (OI vs sequence length) | **Survives, but crowded.** Others study the boundary from the *expansion* side. Our angle — locating the cliff from inside a small fast tier, with page residency verified — is still open. Fragmentation must be ruled out as a confound. |
| **RQ3** — topology as a controlled factor | 2407.00029; 2605.19775; 2606.25353 (multi-socket, locality-aware); Na et al. 2024 | **Survives, weakest of the four.** Named-policy comparison with remote-traffic counters is not something the found literature does for CPU LLM inference, but the contribution is incremental. Keep it secondary as planned. |
| **RQ4** — selective weight/KV tiering | **2508.13231 (closest relative)**; 2606.12556; 2606.25353; 2607.18141 | **Survives, but the framing must change.** The idea is no longer novel — it is formalised (2508.13231) and demonstrated in adjacent settings. The defensible contribution is the **empirical CPU-side measurement on real HBM/DDR hardware with residency verification**, positioned as testing an existing prediction. Read 2508.13231 before writing the RQ4 section. |

---

## 8. What the search did *not* find

These absences are the evidence for the novelty claim that
`research/analysis/sections/04-gaps.tex` deliberately declines to make yet.
They are stated as search outcomes, not as proof.

- **No study measuring verified local-HBM versus local-DDR placement for quantized `llama.cpp` inference on Xeon Max, with prefill and decode reported separately.** The nearest neighbours each miss one axis: 2309.09084 has the hardware but no LLM; 2508.13231 has the tiering question but is theoretical and accelerator-side; 2606.25353 has the CPU and the runtime but targets LLC, not HBM.
- **No reported comparison of the achieved HBM/DDR inference ratio against the measured STREAM bandwidth ratio for transformer decode.** H1b appears to be unaddressed as a stated hypothesis.
- **No empirical weights-versus-KV split across CPU HBM and DDR tiers on real hardware.** 2508.13231 models it; nobody found measures it on a Xeon Max.
- **No study of SNC4 with explicit placement for LLM inference.** Only Na et al.'s naive-configuration result exists.

Before freezing the proposal, repeat this search on the ACM DL, IEEE Xplore, and
the ISC/SC/IPDPS/ICS 2026 proceedings — the searches behind this file were
web-first and will under-represent venue-only publications.

---

## 9. Suggested reading order

1. **arXiv:2606.25353** — Cache-Resident LLM Inference. Closest competitor; read before writing any positioning text.
2. **arXiv:2508.13231** — Dynamic KV Cache Placement. Decides how RQ4 must be framed.
3. **arXiv:2309.09084** — Xeon MAX bandwidth-bound evaluation. Sets the expected effect size for RQ1.
4. **arXiv:2605.30571** — Memory-Bound but Not Bandwidth-Limited. The insurance policy for a small or null H1 result.
5. **arXiv:1704.08273** — Hybrid memory on KNL. The mechanism, and the prediction for when HBM does not help.
6. **arXiv:2507.09019** — Evaluating inference serving systems. Read before finalising the experimental protocol, not after.
7. **arXiv:2604.20913** and the **CEUR MedLocalGPT** paper — the two nearest quantitative baselines on Sapphire-Rapids-class Xeon.
8. **arXiv:2607.02574** — KV cache management survey. Harvest citations for the literature review chapter.

---

## 10. BibTeX for the verified entries

Paste into `references.bib` as each paper is read and actually cited. Preprint
entries are `@misc` deliberately — promote to `@inproceedings` once a refereed
version exists.

```bibtex
@misc{zhang2026cacheresident,
  author        = {Zhang, Wanning and Gu, Tongzhou and Canini, Marco and
                   Xu, Ceyu and Weng, Jian},
  title         = {Cache-Resident {LLM} Inference in {GB}-Scale Last-Level Caches},
  year          = {2026},
  month         = jun,
  eprint        = {2606.25353},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AR},
  url           = {https://arxiv.org/abs/2606.25353}
}

@misc{zuo2026fairyfuse,
  author        = {Zuo, Fei and Xi, Xiaoyan and Zeng, Quanyi and
                   Wang, Feiyu and Leung, Ho Fai},
  title         = {{FairyFuse}: Multiplication-Free {LLM} Inference on {CPU}s
                   via Fused Ternary Kernels},
  year          = {2026},
  month         = apr,
  eprint        = {2604.20913},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2604.20913}
}

@misc{kurt2026quantization,
  author        = {Kurt, Uygar},
  title         = {Which Quantization Should {I} Use? {A} Unified Evaluation of
                   \texttt{llama.cpp} Quantization on {Llama-3.1-8B-Instruct}},
  year          = {2026},
  month         = jan,
  eprint        = {2601.14277},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2601.14277}
}

@misc{lu2026thinfer,
  author        = {Lu, Yao and Luan, Zhongzhi and Li, Gen and Qi, Jiaxing and
                   Ma, Shiqing and Han, Bin and Shang, Shizhe and
                   Yang, Hailong and Qian, Depei},
  title         = {Bandwidth-Aware {LLM} Inference on Heterogeneous Many-Core
                   Supercomputers},
  year          = {2026},
  month         = may,
  eprint        = {2605.25655},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2605.25655}
}

@inproceedings{shen2023efficientcpu,
  author    = {Shen, Haihao and Chang, Hanwen and Dong, Bo and
               Meng, Hengyu and Luo, Yu},
  title     = {Efficient {LLM} Inference on {CPU}s},
  booktitle = {NeurIPS 2023 Workshop on Efficient Natural Language and
               Speech Processing (ENLSP)},
  year      = {2023},
  eprint    = {2311.00502},
  archivePrefix = {arXiv}
}

@inproceedings{wei2025tmac,
  author    = {Wei, Jianyu and Cao, Shijie and Cao, Ting and Ma, Lingxiao and
               Wang, Lei and Zhang, Yanyong and Yang, Mao},
  title     = {{T-MAC}: {CPU} Renaissance via Table Lookup for Low-Bit {LLM}
               Deployment on Edge},
  booktitle = {Proceedings of the Twentieth European Conference on Computer
               Systems (EuroSys '25)},
  year      = {2025},
  eprint    = {2407.00088},
  archivePrefix = {arXiv}
}

@misc{reguly2023xeonmax,
  author        = {Reguly, Istvan Z.},
  title         = {Comparative Evaluation of Bandwidth-Bound Applications on
                   the {Intel Xeon CPU MAX} Series},
  year          = {2023},
  month         = sep,
  eprint        = {2309.09084},
  archivePrefix = {arXiv},
  primaryClass  = {cs.PF},
  url           = {https://arxiv.org/abs/2309.09084}
}

@inproceedings{peng2017hybridmemory,
  author    = {Peng, Ivy Bo and Gioiosa, Roberto and Kestor, Gokcen and
               Laure, Erwin and Markidis, Stefano},
  title     = {Exploring the Performance Benefit of Hybrid Memory System on
               {HPC} Environments},
  booktitle = {2017 IEEE International Parallel and Distributed Processing
               Symposium Workshops (IPDPSW)},
  year      = {2017},
  eprint    = {1704.08273},
  archivePrefix = {arXiv}
}

@misc{fang2025kvplacement,
  author        = {Fang, Yunhua and Xie, Rui and Haq, Asad Ul and Ma, Linsen and
                   El Maghraoui, Kaoutar and Wang, Naigang and Wang, Meng and
                   Liu, Liu and Zhang, Tong},
  title         = {Accelerating {LLM} Inference via Dynamic {KV} Cache Placement
                   in Heterogeneous Memory System},
  year          = {2025},
  month         = aug,
  eprint        = {2508.13231},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2508.13231}
}

@misc{jang2026itme,
  author        = {Jang, Hakbeom and Min, Younghoon and Kim, Sunwoong and
                   Ahn, Taeyoung and Kim, Hanyee and Joo, Youngpyo and
                   Kim, Hoshik and Kim, Jongryool},
  title         = {{ITME}: Inference Tiered Memory Expansion with Disaggregated
                   {CXL}-Hybrid Memories},
  year          = {2026},
  month         = jun,
  eprint        = {2606.12556},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2606.12556}
}

@misc{jang2026hymcache,
  author        = {Jang, Hakbeom and Song, Inho and Kim, Hoshik and
                   Noh, Sam H. and Kim, Jongryool},
  title         = {A {CXL} Memory Rack for Multi-Turn {LLM} Serving},
  year          = {2026},
  month         = jul,
  eprint        = {2607.18141},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2607.18141}
}

@misc{yuan2024roofline,
  author        = {Yuan, Zhihang and others},
  title         = {{LLM} Inference Unveiled: Survey and Roofline Model Insights},
  year          = {2024},
  month         = feb,
  eprint        = {2402.16363},
  archivePrefix = {arXiv},
  note          = {Author list to be completed from the PDF before citing},
  url           = {https://arxiv.org/abs/2402.16363}
}

@misc{chen2026memorybound,
  author        = {Chen, Josef},
  title         = {Memory-Bound but Not Bandwidth-Limited: The Physical {AI}
                   Inference Gap in Batch-1 {LLM} Decode},
  year          = {2026},
  month         = may,
  eprint        = {2605.30571},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2605.30571}
}

@misc{bi2026rooflinebench,
  author        = {Bi, Zhen and Chen, Xueshu and Sun, Luoyang and Yao, Yuhang and
                   Shen, Qing and Lou, Jungang and Deng, Cheng},
  title         = {{RooflineBench}: A Benchmarking Framework for On-Device
                   {LLM}s via Roofline Analysis},
  year          = {2026},
  month         = feb,
  eprint        = {2602.11506},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2602.11506}
}

@inproceedings{arif2026inferencescaling,
  author    = {Arif, Moiz and Maurya, Avinash and Vazhkudai, Sudharshan and
               Nicolae, Bogdan},
  title     = {Understanding Inference Scaling for {LLM}s: Bottlenecks,
               Trade-offs, and Performance Principles},
  booktitle = {Proceedings of the 53rd Annual International Symposium on
               Computer Architecture (ISCA '26), Industry Track},
  year      = {2026},
  eprint    = {2605.19775},
  archivePrefix = {arXiv}
}

@misc{agrawal2025evaluating,
  author        = {Agrawal, Amey and Kedia, Nitin and Agarwal, Anmol and
                   Mohan, Jayashree and Kwatra, Nipun and Kundu, Souvik and
                   Ramjee, Ramachandran and Tumanov, Alexey},
  title         = {On Evaluating Performance of {LLM} Inference Serving Systems},
  year          = {2025},
  month         = jul,
  eprint        = {2507.09019},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2507.09019}
}

@misc{salaria2025metametrics,
  author        = {Salaria, Shweta and Liu, Zhuoran and
                   Mimura Gonzalez, Nelson},
  title         = {Meta-Metrics and Best Practices for System-Level Inference
                   Performance Benchmarking},
  year          = {2025},
  month         = aug,
  eprint        = {2508.10251},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2508.10251}
}

@misc{stuhlmann2025bench360,
  author        = {Stuhlmann, Linus and Fadel Argerich, Mauricio and
                   F\"{u}rst, Jonathan},
  title         = {{Bench360}: Benchmarking Local {LLM} Inference from
                   360 Degrees},
  year          = {2025},
  month         = nov,
  eprint        = {2511.16682},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2511.16682}
}

@misc{li2024hardwareperspective,
  author        = {Li, Jinhao and Xu, Jiaming and Huang, Shan and Chen, Yonghua
                   and Li, Wen and Liu, Jun and Lian, Yaoxiu and Pan, Jiayi and
                   Ding, Li and Zhou, Hao and Wang, Yu and Dai, Guohao},
  title         = {Large Language Model Inference Acceleration: A Comprehensive
                   Hardware Perspective},
  year          = {2024},
  month         = oct,
  eprint        = {2410.04466},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2410.04466}
}

@inproceedings{son2026coxmoe,
  author    = {Son, Muyoung and Chen, Yi and Yoo, Seungjae and
               Choi, Soongyu and Kim, Joo-Young},
  title     = {{CoX-MoE}: Coalesced Expert Execution for High-Throughput
               {MoE} Inference with {AMX}-Enabled {CPU}-{GPU} Co-Execution},
  booktitle = {Proceedings of the 63rd ACM/IEEE Design Automation Conference
               (DAC '26)},
  year      = {2026},
  eprint    = {2605.17889},
  archivePrefix = {arXiv}
}

@inproceedings{he2024distributedcpu,
  author    = {He, Pujiang and Zhou, Shan and Li, Changqing and
               Huang, Wenhuan and Yu, Weifei and Wang, Duyi and
               Meng, Chen and Gui, Sheng},
  title     = {Distributed Inference Performance Optimization for {LLM}s
               on {CPU}s},
  booktitle = {ICLR 2024 Workshop on Practical ML for Low Resource Settings},
  year      = {2024},
  eprint    = {2407.00029},
  archivePrefix = {arXiv}
}

@inproceedings{nomadattention2024,
  author    = {Zhang, Tianyi and others},
  title     = {{NoMAD}-Attention: Efficient {LLM} Inference on {CPU}s Through
               Multiply-Add-Free Attention},
  booktitle = {Advances in Neural Information Processing Systems 37
               (NeurIPS 2024)},
  year      = {2024},
  eprint    = {2403.01273},
  archivePrefix = {arXiv},
  note      = {Author list to be completed from the PDF before citing}
}

@inproceedings{chen2025ktransformers,
  author    = {Chen, Jianwei and others},
  title     = {{KTransformers}: Unleashing the Full Potential of {CPU}/{GPU}
               Hybrid Inference for {MoE} Models},
  booktitle = {Proceedings of the ACM SIGOPS 31st Symposium on Operating
               Systems Principles (SOSP '25)},
  year      = {2025},
  doi       = {10.1145/3731569.3764843},
  note      = {Author list to be completed from the PDF before citing}
}

@inproceedings{medlocalgpt2026,
  author    = {{MedLocalGPT authors}},
  title     = {Deploying {LLM}s on {CPU}-only Environments with
               \texttt{llama.cpp} Library Set: {MedLocalGPT} Project Case},
  booktitle = {CEUR Workshop Proceedings},
  volume    = {4164},
  year      = {2026},
  month     = feb,
  issn      = {1613-0073},
  url       = {https://ceur-ws.org/Vol-4164/paper11.pdf},
  note      = {Author list and venue title to be completed from the PDF
               before citing}
}

@misc{lin2026dak,
  author        = {Lin, Shouxu and Guo, Zhiyuan and Lin, Jiaxin},
  title         = {{DAK}: Direct-Access-Enabled {GPU} Memory Offloading with
                   Optimal Efficiency for {LLM} Inference},
  year          = {2026},
  month         = apr,
  eprint        = {2604.26074},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2604.26074}
}
```
