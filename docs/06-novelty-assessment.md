# 6. Novelty Assessment — read this before believing anything in §2

*Written September 2026. First round: a targeted prior-art check on four
proposals. Second round (§6.5 onward): T3, T5 and T6 checked as well.*

**Running tally: 7 proposals checked, 7 occupied. Two removed outright.**

## 6.1 The correction

The problem catalog in `02-open-problems.md` was written from broad orientation
searches, not from a systematic novelty check. Several of its gap statements —
phrases like *"nobody has composed the two"* and *"there is no benchmark
with..."* — were stated with more confidence than the evidence supported.

Targeted searches have now checked seven proposals and found substantial prior
art on **all seven**. Two (T5, T7) are dead as proposed. A 7/7 hit rate means the
correct prior for the three unchecked proposals is that they are occupied too.

**None of the proposals in this repository should be treated as verified novel
until the protocol in §6.4 has been run on it.**

---

## 6.2 Prior-art register — what was found

### T7 — Prefix-cache side channels in multi-tenant LLM serving → **DEAD AS PROPOSED**

Both halves of the proposal are published, repeatedly.

| Side | Prior work |
|---|---|
| Attacks | PROMPTPEEK, EarlyBird, InputSnatch — reported up to 100% attack success against unprotected vLLM and SGLang; "Shadow in the Cache"; agent-assisted attacks on non-prefix KV cache in RAG (<https://arxiv.org/abs/2606.21842>) |
| Defenses | SafeKV; PrefixWall (<https://arxiv.org/html/2603.10726v2>); Selective KV-Cache Sharing (<https://arxiv.org/html/2508.08438v1>); Governing the KV Cache (<https://arxiv.org/abs/2608.09225>) |

The proposed claim — *"we systematize the leakage and give a partitioning
mitigation with measured throughput cost"* — is the content of several existing
papers. **Remove T7 from the portfolio.** Any re-entry would need a genuinely
different axis, and the field is moving fast enough that this is not a good use of
a PhD slot.

### T1 — HNDL against RAG and embedding stores → **FRAMING OCCUPIED, MEASUREMENT LIKELY OPEN**

The Cloud Security Alliance published *AI Infrastructure Post-Quantum: Harvest Now,
Decrypt Later* in May 2026 —
<https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/ai-infrastructure-post-quantum-harvest-now-decrypt-later-v1-csa-styled.pdf>.
That is the exact composition claimed as novel. Also relevant: *Transform Before
You Query*, privacy-preserving vector retrieval via embedding-space alignment
(<https://arxiv.org/pdf/2507.18518>), and a comprehensive review of RAG threats
and defenses (<https://arxiv.org/pdf/2603.21654>).

**What plausibly survives:** the CSA document is an industry position paper, not a
peer-reviewed empirical study. The measurement — what fraction of deployed
embedding APIs and vector stores actually negotiate PQ-hybrid key exchange — and
the inversion-fidelity-weighted exposure model appear to remain open. **Restate
the claim as measurement, and cite CSA as the motivation rather than presenting
the framing as new.**

### T2 — Benchmark for LLM-assisted PQC migration → **SUBSTANTIALLY OCCUPIED**

- *Empirical Evaluation of LLMs for Migration of Cryptographic Code*
  (<https://arxiv.org/abs/2606.07341>): ~800 pre/post-quantum code pairs across
  seven categories with unit tests, static + dynamic + runtime validation
  pipeline, fine-tuned model reaching 92.5% dynamic functional correctness, plus
  validation on six open-source repositories.
- *Quantum-Safe Code Auditing* (<https://arxiv.org/pdf/2604.00560>): LLM-assisted
  static analysis across five libraries, 71.98% precision / 100% recall.
- *Assessing and Enhancing Quantum Readiness in Mobile Apps* (<https://arxiv.org/pdf/2506.00790>).
- *CryptanalysisBench* (<https://arxiv.org/html/2607.18538>): 191 tasks with
  automatic game-based verification — establishes the benchmark-with-automatic-oracle
  pattern in this space.
- *On the Formalization of Cryptographic Migration* (<https://arxiv.org/pdf/2408.05997>).

The claim "there is no benchmark with real repositories and executable
correctness checking" is **false as written** — 2606.07341 has both, at small
scale.

**What plausibly survives:** that paper explicitly reports limitations "in larger
projects with complex dependencies." That stated limitation is the opening. A
benchmark built on *adjudicated ground truth at scale* with the hard-case
taxonomy (config-driven selection, in-house wrappers, transitive dependencies,
stored artifact formats) and contamination control is a defensible extension —
but it must be positioned as extending 2606.07341, not replacing a void.

### T4 — Toolchain-introduced constant-time violations → **HEADLINE PUBLISHED**

- *Breaking Bad: How Compilers Break Constant-Time Implementations*
  (<https://arxiv.org/html/2410.13489>): 8 cryptographic libraries, 11 algorithms,
  6 architectures, 2 compilers across 9 and 13 versions, 7 optimization levels —
  **44,604 experiments.** This is precisely the matrix proposed as novel.
- **Clangover**: a real compiler-induced timing channel affecting ML-KEM
  implementations; variable-time integer division affected a wide range of Kyber
  implementations.
- *SoK: The Constant Time Model* (<https://arxiv.org/html/2606.13000v1>).
- LLVM gained explicit constant-time support in December 2025.
- Plus the screening tooling already noted in §2: CT-KAT, PQDSS timing analysis,
  DATA vs. MicroWalk.

The claim that toolchain-introduced violations are unstudied is **false**.

**What plausibly survives:** a PQC-focused treatment across the *newly
standardized* set (ML-KEM, ML-DSA, SLH-DSA, HQC) with the newer toolchains, and —
more defensibly — **the LLM-assisted localization and repair half**, which has an
automatic oracle and is not addressed by any of the above. Consider inverting the
paper: the compiler study becomes related work and setup; the repair evaluation
becomes the contribution.

### T3 — Cross-dataset generalization of DL-SCA on ML-KEM/ML-DSA → **CORE CLAIM FALSE**

Portability is not an unstudied gap. It is a named subfield with its own methods,
and it has already been applied to Kyber specifically.

- *Enhancing Portability in Deep Learning-Based Side-Channel Attacks Against
  Kyber* (<https://dl.acm.org/doi/10.1007/978-981-97-9053-1_9>): Ablated Multiple
  Leakage Point Model, explicitly optimizing **intra-board** (same device, different
  probe placement) and **inter-board** (different devices) portability, >99% accuracy.
- *A Second Look at the Portability of Deep Learning Side-Channel Attacks*,
  RAID 2024 (<https://homepages.uc.edu/~wang2ba/files/pub/raid24_mabon.pdf>).
- *AL-PA: cross-device profiled side-channel attack using adversarial learning*,
  DAC 2022 (<https://dl.acm.org/doi/10.1145/3489517.3530517>) — device-invariant
  feature learning.
- *Cross-device profiled side-channel attack with unsupervised domain adaptation* —
  portability treated as a domain-discrepancy problem, which is exactly the
  proposed method.
- *Portability of Deep-Learning Side-Channel Attacks against Software AES*
  (<https://dl.acm.org/doi/10.1145/3558482.3590177>).

The proposed **secondary** contribution — "establish a common evaluation protocol,
its absence is itself a problem" — is also occupied: *SoK: Deep Learning-based
Physical Side-channel Analysis* (ACM CSUR), *On the Evaluation of DL-based SCA*
(<https://eprint.iacr.org/2021/952.pdf>), *On the Attack Evaluation and the
Generalization Ability in Profiling SCA* (<https://eprint.iacr.org/2020/899>).
Guessing entropy as the generalization metric is long-settled.

The claim that "single-lab papers structurally cannot study portability" is
**false** — labs with two boards study exactly this, and have.

**What might survive:** the Kyber/ML-KEM work is done; **ML-DSA is less covered**,
and the rejection-loop leakage *under domain shift* is a narrow, specific question
that may be open. Verify directly against the ML+SCA survey's bibliography
(<https://eprint.iacr.org/2025/1754.pdf>) before investing.

### T5 — Post-quantum delegation for agentic systems → **DEAD AS PROPOSED**

Both the framing and the piece explicitly identified as "the research content"
are published.

*The framing* — "agent frameworks have no verifiable delegation chain":
- **AITH**: a *post-quantum continuous delegation protocol for AI agents*, with
  push-based revocation and five security theorems machine-verified in **Tamarin**
  under Dolev-Yao. This is T5, including the formal-methods layer proposed as the
  differentiator.
- **IBCT (Invocation-Bound Capability Tokens)**: identity + attenuated
  authorization + provenance in an append-only token chain, holder-side
  attenuation, chained Biscuit/Datalog mode, transport bindings across
  **MCP/A2A/HTTP**.
- *AIP: Agent Identity Protocol for Verifiable Delegation* (<https://arxiv.org/abs/2603.24775v1>).
- *Authorization Propagation in Multi-Agent AI Systems* (<https://arxiv.org/pdf/2605.05440>).
- *Governing Dynamic Capabilities: Cryptographic Binding* (<https://arxiv.org/html/2603.14332v1>).
- *The Provenance Paradox in Multi-Agent LLM Routing* (<https://arxiv.org/pdf/2603.18043>).
- IETF draft *Attenuating Authorization Tokens for Agentic Delegation Chains*;
  A2A capability-based authorization SEP (<https://github.com/a2aproject/A2A/discussions/1404>).
- Agent Passport System: Ed25519 delegation chains where sub-delegation can only
  narrow scope — the monotonic-attenuation property proposed as novel.

*The amortization construction* — proposed as "the research content is
amortization; if you cannot find a non-obvious construction there, downgrade":
- Merkle batch signing for PQ overhead is established: *Impact of Post-Quantum
  Signatures on InnoDB* (<https://eprint.iacr.org/2026/987.pdf>) reports batch-512
  Merkle-root signing at 28.1x insertion throughput and 97.6% per-record signature
  storage reduction, with O(log b) proofs.
- *Efficient post-quantum cryptographic signature aggregation*
  (<https://link.springer.com/article/10.1186/s13635-026-00228-8>).
- *Hash-Based Multi-Signatures for Post-Quantum Ethereum* (<https://eprint.iacr.org/2025/055.pdf>);
  cross-input PQ signature aggregation.

Applying Merkle batching to agent messages is engineering, not a construction.
**Remove T5 from the portfolio**, or find a genuinely different axis.

### T6 — Cryptographic agility as a measurable property → **METRIC MACHINERY OCCUPIED**

- *Cryptographic Agility for Applications: An Assessment Framework*
  (<https://link.springer.com/chapter/10.1007/978-3-032-28946-9_9>, arXiv 2606.13425):
  seven orthogonal dimensions, including coupling dimensions measuring what
  application code knows about algorithms and providers — the proposed metric.
- **CARS (Crypto-Agility Readiness Score)**: a five-dimensional weighted metric on
  a normalized [0,100] scale, evaluated across legacy system categories for
  migration prioritization.
- *Intent-Based Cryptographic API Design for Cryptographic Agility*
  (<https://arxiv.org/pdf/2606.13445>) — the proposed *remedy* (an intent-based
  crypto API shim), already published.
- *On the Formalization of Cryptographic Migration* (<https://arxiv.org/pdf/2408.05997>).
- <https://eprint.iacr.org/2026/1467.pdf> is formatted as an IEEE TIFS submission
  on quantum-safe migration for legacy systems — check its final venue.
- PQ artifact-size implications (ML-DSA-65 pk 1952B vs Ed25519 32B; ML-KEM-768
  ct 1088B) are already documented in the migration literature.

**What might survive:** the searches surfaced no ML-platform-specific agility
work. Applying an existing framework to ML platforms, and the derivative-lineage
and stored-artifact-format findings, may be open — but that is an *application*
paper, and its Transactions viability rests entirely on whether the ML-specific
findings are genuinely distinctive rather than a restatement. Thin.

---

## 6.6 Second-round tally: 7 checked, 7 occupied

| ID | Status | Verdict |
|---|---|---|
| T1 | Framing occupied (CSA May 2026); measurement plausibly open | Reposition as measurement |
| T2 | Substantially occupied (2606.07341, 2604.00560) | Reposition as extension |
| T3 | **Core claim false** — portability is a named subfield, done on Kyber | ML-DSA rejection loop only; verify hard |
| T4 | Headline published (Breaking Bad, 44,604 experiments; Clangover) | Invert; LLM repair carries it |
| T5 | **Dead** — AITH, IBCT cover framing; Merkle amortization established | Remove |
| T6 | Metric machinery and proposed remedy both published | ML-specific application only; thin |
| T7 | **Dead** — attacks and defenses both published | Remove |
| T8, T9, T10 | Unchecked | At 7/7, assume occupied |

**Two of the four committed thesis papers (T5 as a Paper-4 option, T7 as reserve)
are gone. The other five need their central claims rewritten from "gap" to
"delta".**

## 6.7 What the 7/7 result actually tells you

Not that the field is closed. That the **method of generating these proposals was
wrong**, and that the area is genuinely crowded by well-resourced groups moving
at preprint speed.

Note what the register shows: nearly every collision is a **2025-2026 arXiv or
ePrint preprint**, not a settled journal result. That cuts both ways — scoop risk
is high, and much of this work is unreplicated.

**Positions that stay defensible for a student without a lab, precisely because
resourced groups skip them:**

1. **Reproduction and negative results.** Much of the colliding work above is
   unreplicated preprints with self-reported numbers. Systematically reproducing
   them, and reporting where they do not hold, is real, publishable, and
   increasingly valued.
2. **Benchmarks and evaluation infrastructure.** Requires labor, not equipment.
   High citation. This is why T2 remains viable as an extension despite collision.
3. **Systematization with a defensible thesis** — as distinct from a survey.
4. **The unglamorous measurement nobody bothers to run.** T1's deployment scan is
   the surviving example.
5. **Adversarial re-evaluation of published defenses** under adaptive attackers —
   defense papers routinely under-evaluate, and this is where the field's
   evaluation crisis creates genuine openings.

**And the honest structural point:** a problem list generated from web searches is
terrain mapping, not problem selection. Problem selection needs a supervisor with
standing in the area, sustained immersion in the primary literature, and the
verification protocol in §6.4 run properly on every candidate. This repository is
useful as a map and as a set of checks. It is not a substitute for either.

### T8, T9, T10 — **UNCHECKED**

Not yet searched. Given 7/7 above, assume occupied until shown otherwise. Known
adjacent work already visible from earlier searches:

| Proposal | Nearest known prior work |
|---|---|
| T3 (DL-SCA portability) | Published work exists on enhancing portability in DL-SCA against Kyber; the ML+SCA survey (<https://eprint.iacr.org/2025/1754.pdf>) will list more |
| T5 (PQ agent delegation) | AI supply-chain MBOM-PQC provenance and PQC attestation (<https://www.mdpi.com/2079-8954/14/5/593>) |
| T6 (crypto agility metrics) | Assessment framework for application-level cryptographic agility (<https://arxiv.org/pdf/2606.13425>); intent-based cryptographic API design (<https://arxiv.org/pdf/2606.13445>) — the latter is the remedy T6 proposed |

---

## 6.3 What this actually means

**This is normal, and it is not a crisis.** Nearly every idea generated in month
zero is partly occupied; the literature is large and moves faster than any
individual can track. The finding is not "your topic is dead." It is:

1. **Novelty is a claim about the literature, and it must be earned by a
   systematic search.** No amount of plausibility reasoning substitutes.
2. **"Nobody has done this" is a fragile claim.** One reviewer with one citation
   destroys it, and at Transactions level that reviewer exists. Never build an
   abstract on it.
3. **The robust claim shape needs prior work to exist:**

   > *Prior work X established A under assumption B. We show B does not hold in
   > setting C, and give D.*

   Under that shape, every paper found above is **raw material, not an
   obstacle**. "Breaking Bad" makes T4 easier to write, not harder — it gives you
   a validated method, a baseline, and a stated scope you can extend.
4. **At Transactions level, novelty is not the only bar and often not the
   binding one.** A large fraction of accepted TIFS and TDSC papers are
   substantial extensions executed rigorously. Papers are rejected for being
   *incremental* — meaning a small delta with a thin evaluation — far more often
   than for being unoriginal. A well-scoped delta with an adaptive attacker,
   proper baselines, error bars, and a released artifact beats a novel idea with
   a weak evaluation nearly every time.

The practical consequence: **stop optimizing for novelty and start optimizing for
a defensible delta plus rigorous execution.** That is both more achievable and
more publishable.

---

## 6.4 Novelty verification protocol — run this per problem, before committing

Budget one focused week per candidate. Do this for your top two before month 3.

**Step 1 — Systematic search, not conversational.**
Query each of these independently; do not rely on one source or on an LLM's
summary:
- Google Scholar and Semantic Scholar, with and without date restriction
- **IACR ePrint** — where crypto work appears first, often a year before journals
- arXiv `cs.CR`, `cs.SE`, `cs.LG` full-text search
- DBLP author-page walks for the 3-5 groups most active in the area
- ACM DL and IEEE Xplore, since Transactions work is often not preprinted
- The reference lists and citation graphs of the two closest papers you find

**Step 2 — Forward citation walk.** Take the closest paper. Read everything that
cites it. This is where the "someone already did your extension" papers live, and
it is the step most often skipped.

**Step 3 — Fill the delta table.**

| Closest prior work | What it established | Its stated assumptions/limits | Which limit do I break | Why breaking it matters |
|---|---|---|---|---|

If you cannot complete the last two columns for a specific paper, you do not yet
have a contribution — you have a topic.

**Step 4 — Write the related-work paragraph first.** Before running any
experiment, write the paragraph that will appear in the paper positioning your
work against the three closest results. If that paragraph is uncomfortable to
write, the delta is too small. This is a two-hour test that saves months.

**Step 5 — Set alerts and re-run at submission.** arXiv and ePrint alerts on your
keywords; re-run the full search immediately before submitting, because
Transactions review cycles are 10-16 months and the field will move underneath
you.

---

## 6.5 Revised portfolio status

| ID | Status after checking | Action |
|---|---|---|
| **T1** | Framing occupied (CSA, May 2026); measurement likely open | Restate as an empirical measurement paper; cite CSA as motivation |
| **T2** | Substantially occupied (2606.07341, 2604.00560) | Reposition as an extension targeting their stated failure on large dependency-complex projects |
| **T3** | Core claim false — portability is an established subfield, done on Kyber | Only the ML-DSA rejection loop under domain shift may survive |
| **T4** | Headline published (Breaking Bad, Clangover) | Invert: compiler study becomes setup, LLM-assisted repair becomes the contribution |
| **T5** | **Dead** — AITH and IBCT cover the framing; Merkle amortization is established | Remove from portfolio |
| **T6** | Metric machinery (assessment framework, CARS) and the proposed remedy both published | ML-specific application only; thin |
| **T7** | **Dead** — attacks and defenses both published | Remove from portfolio |
| **T8** | Unchecked | Run §6.4 |
| **T9** | Unchecked; known to be highly competitive | Run §6.4 |
| **T10** | Unchecked | Run §6.4 |

The spine in `03-thesis-architecture.md` still stands as a *structure*. The
individual paper claims inside it need the rewrite described above before they
are submittable.
