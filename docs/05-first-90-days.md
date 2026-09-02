# 5. First 90 Days

**Available:** one classical workstation, optionally one consumer GPU, cloud API
credits. **Not available:** quantum hardware, side-channel lab equipment.

The goal of 90 days is not a paper. It is to (a) eliminate one direction,
(b) reproduce two existing results so your tooling is trusted, and (c) own one
number that did not exist before.

---

## Weeks 1-3 — Read to a decision

Read with one question: *which of T1, T4, T2 am I actually going to do?*

**Standards and policy — read the documents, not summaries**
- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA)
- NIST IR 8547 (transition to PQC standards); NIST/NCCoE migration project
- NSA CNSA 2.0 and BSI/ANSSI hybrid guidance — read both, note where they conflict
- OWASP Top 10 for LLM Applications; NIST AI 100-2 (adversarial ML taxonomy)

**Technical foundations**
- Embedding inversion: Song & Raghunathan on information leakage in embeddings;
  the vec2text line on near-verbatim recovery
- Agentic security: <https://arxiv.org/pdf/2510.23883>, <https://arxiv.org/pdf/2506.08837>
- ML + side channels on PQC: <https://eprint.iacr.org/2025/1754.pdf>
- Constant-time analysis: PQDSS timing screening <https://arxiv.org/pdf/2509.04010>;
  CT-KAT <https://eprint.iacr.org/2026/1418>; DATA vs. MicroWalk <https://eprint.iacr.org/2026/611.pdf>
- PQC library support survey: <https://arxiv.org/pdf/2508.16078>
- QML skepticism (so you can *defend the exclusion*): barren-plateau theory,
  dequantization results, QML-for-cybersecurity taxonomy <https://arxiv.org/pdf/2512.15286>

**Method:** keep one table with columns
`paper | claim | evidence | what it does NOT show | what I would do next`.
Column four is where problems come from. Target 60-80 rows by week 6.

---

## Weeks 2-6 — Tooling and two reproductions

**Software stack (all runs on your workstation)**
```
liboqs + oqs-provider           # PQ primitives, OpenSSL 3.x integration
PQClean, pqm4 (source only)     # reference implementations to analyse
dudect, TIMECOP, MicroWalk      # constant-time / timing leakage analysis
DATA, Binsec/Rel2               # binary-level constant-time verification
Valgrind, perf, LLVM tooling    # microarchitectural measurement
CodeQL, Semgrep                 # crypto discovery ground truth (T2)
ELMO / MAPS                     # SIMULATED Cortex-M leakage — no hardware needed
sigstore / model-signing        # model artifact signing
AgentDojo, InjecAgent           # agent security benchmarks (T5/T9)
BEIR / MTEB subsets             # retrieval quality (T1)
vLLM or SGLang                  # serving stack (T7)
lattice-estimator               # PQ parameter security (T10)
```

**Public side-channel trace datasets — download early, they are large**
- DTDS, ~60k Dilithium power traces, Cortex-M4: <https://doi.org/10.57760/sciencedb.j00173.00001>
- Kyber pair-pointwise multiplication traces: <https://eprint.iacr.org/2025/811>
- Unified ML-KEM / ML-DSA hardware traces: <https://zenodo.org/records/18681117>

**Reproduction 1 — everyone does this.** Stand up hybrid PQ TLS with oqs-provider
(`X25519MLKEM768`) and measure handshake size and latency against classical on a
bandwidth-limited link. Trivial, but it makes the size problem concrete and gives
you numbers reused in three papers.

**Reproduction 2 — choose by direction:**
- *T1:* reproduce embedding inversion on one open embedding model; get measurable
  recovery on a held-out corpus.
- *T4:* run dudect and MicroWalk over liboqs ML-KEM at `-O0` and `-O2`, and check
  whether results differ. **If they differ, your paper exists.** This is a
  two-week pilot that decides a three-year direction — do it early.
- *T2:* run 2-3 LLMs over 10 real repositories and hand-audit the crypto
  inventory. That one recall number tells you whether T2 is a paper.
- *T3:* load DTDS, reproduce a published attack on it, and confirm you get the
  reported guessing entropy. If you cannot reproduce on a dataset with known
  results, your pipeline is wrong — find out now, not in month 14.

---

## Weeks 6-10 — Kill one direction

Write a two-page internal memo for each of your top two candidates: threat model,
the exact claim, the experiment that would falsify it, resources, and the three
most likely reasons it fails. Then kill one.

Killing a direction in month 2 is a success. Killing it in month 20 is a crisis.

**Decision heuristics for your setup:**
- No GPU at all, or shared/unreliable GPU access → **T4 and T2** (both CPU-only)
  over T1 and T3.
- One reliable GPU → **T1 first**, T4 in parallel since it does not contend for
  the GPU.
- Prefer systems/software work → T4, T2, T5.
- Prefer empirical ML work → T1, T3.
- Supervisor has industry contacts for deployment data → T1 and T6 gain a lot.

Answer honestly about what you *enjoy*. A four-year project you dislike fails
regardless of merit.

---

## Weeks 8-12 — Produce one novel measurement

By day 90 own one number that did not exist before. Each is ~4 weeks once tooling
works:

- **T1:** the fraction of N reachable embedding/vector-DB endpoints negotiating
  PQ-hybrid key exchange. Almost certainly near zero — which is the point, and it
  is now *your established fact*.
- **T4:** the count of constant-time violations that appear at `-O2` but not
  `-O0` across the algorithm × compiler matrix.
- **T2:** discovery recall of frontier LLMs on hand-audited real repositories,
  by hard-case category.
- **T3:** the cross-dataset transfer matrix — guessing entropy when training on
  dataset A and attacking dataset B.

Write it as a short paper immediately and **post to arXiv and IACR ePrint**. With
10-16 month Transactions cycles, the preprint is what protects you from being
scooped while under review. It also becomes Section 3 of the journal paper.

---

## Ongoing hygiene from day 1

- **One repository, versioned, artifact-minded.** Every experiment gets a seed, a
  config file, and a `make reproduce` path. Retrofitting costs months, and
  TSE/TOSEM/TDSC increasingly expect artifacts.
- **Running related-work file**, updated weekly. arXiv `cs.CR` alerts filtered on
  `post-quantum`, `ML-KEM`, `ML-DSA`, `constant-time`, `prompt injection`,
  `agent security`, `side-channel`; plus an IACR ePrint feed.
- **Weekly one-page written update** to your supervisor, even if unread. It forces
  falsifiable statements.
- **Track scoop risk monthly**, especially for T2 and T4 — both are active areas.
  If scooped: become the best extender and user of what landed rather than
  competing with it.
- **Keep two papers in flight.** With Transactions timelines this is the single
  most important scheduling habit you can build.

---

## The three things most likely to sink this PhD

1. **A year-one survey with no thesis.** See `03-thesis-architecture.md` §3.2 for
   the systematization you should write instead.
2. **Being talked into QML because it sounds impressive.** See T10 and §3.6 for
   the prepared answer. If a committee member insists on visible quantum content,
   offer quantum cryptanalytic resource estimation — laptop-only, honest,
   defensible.
3. **Underestimating Transactions review time.** A four-year plan with sequential
   submissions and no rejections is not a plan. Parallelize, preprint everything,
   and start Paper 1 in month 3.
