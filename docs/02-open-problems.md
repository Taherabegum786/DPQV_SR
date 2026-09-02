# 2. Open Problem Catalog

**Constraints this catalog is built around:**
- Compute available: one classical workstation, optionally one consumer GPU, plus
  cloud API credits. **No quantum hardware. No side-channel lab equipment.**
- Publication target: **IEEE / ACM Transactions only.**

Every problem below is executable on a workstation and maps to a specific
Transactions venue. Anything requiring a QRNG, a quantum processor, an
oscilloscope, or a ChipWhisperer has been removed or re-engineered.

Schema per entry: **Gap** (what nobody established) → **Claim** (your abstract's
sentence) → **Method** → **Evidence a reviewer will demand** → **What you need**
→ **Transactions venue** → **Risk**.

Tiering: **A** = do this; **B** = strong second/third paper; **C** = viable with
a condition; **D** = avoid.

---

## T1 — [TIER A] Harvest-Now-Decrypt-Later against RAG and embedding stores

**Gap.** Two established results have never been composed: (a) dense embeddings
are invertible — text is substantially, sometimes near-verbatim, recoverable from
them; (b) TLS sessions recorded today under classical key exchange are
decryptable by a future CRQC. Nobody has established that vector databases are a
*distinctively severe* harvest-now-decrypt-later target, nor quantified it.

**Claim.** *Enterprise RAG deployments are a worst-case HNDL target: they
transmit and store invertible representations of documents whose confidentiality
lifetime exceeds any plausible CRQC horizon, and the overwhelming majority of
deployed embedding APIs and vector stores still negotiate classical key exchange.
We quantify the resulting exposure and give a hybrid-PQ plus
representation-hardening mitigation with a measured retrieval-utility cost.*

**Method.**
1. **Measurement.** Probe the reachable surface of embedding APIs, managed vector
   DBs (Pinecone, Weaviate, Qdrant, Milvus, pgvector deployments) and popular
   self-hosted stacks for negotiated key-exchange groups: how many offer
   `X25519MLKEM768` or equivalent versus pure classical. Passive TLS handshake
   observation only — no access attempts. This is a clean, citable measurement
   nobody has published for this stack.
2. **Inversion fidelity.** Reproduce embedding inversion across current embedding
   models and dimensionalities. Report recovery as a function of model family,
   dimension, and whether the attacker knows the embedding model. Use corpora
   with genuinely long confidentiality lifetimes (de-identified clinical notes,
   legal filings, unpublished technical documents).
3. **Exposure model.** Express risk as
   `P(CRQC by year t) × data_lifetime × inversion_fidelity × interception_feasibility`
   and report **parametrically over the CRQC term** — never as a prediction. This
   single choice neutralizes the "you are guessing about quantum timelines"
   objection that kills most PQC-motivated papers.
4. **Mitigation.** Hybrid PQ key exchange on the transport leg *plus*
   representation hardening at rest (bounded random rotation, calibrated noise,
   or dimensionality reduction). Map the retrieval-quality vs. inversion-
   resistance Pareto frontier on BEIR/MTEB subsets.

**Evidence needed.** Real measurement numbers, not a survey. Inversion
reproduction with a strong baseline. A mitigation with *measured* utility cost.
Threat model with adversary capabilities stated up front. Ethics approval and
disclosure documented (see `04-venues-and-rigor.md` §4.4).

**What you need.** One GPU for inversion training (a single 16-24GB consumer card
suffices; Colab/Kaggle/cloud credits work). Network access. Nothing else.

**Venue.** **IEEE TIFS** (primary), IEEE TDSC, ACM TOPS.

**Risk.** Low. Ingredients are public so scoop risk on the measurement is real —
run the measurement early, it ages fastest. **Cannot fully fail:** if inversion
fidelity turns out low on modern models, that is a bounding result and still a
paper. This is why it is your first paper.

---

## T2 — [TIER A] A benchmark for cryptographic discovery and PQC migration correctness

**Gap.** The PQC migration bottleneck is inventory and agility, not algorithms —
organizations cannot find their own crypto. Existing LLM evaluations use small
synthetic paired code fragments and show LLMs detect misuse but do not reliably
migrate. There is no benchmark with real repositories, verified ground-truth
inventory, executable behavioral-equivalence checking, and contamination control.

**Claim.** *We present the first benchmark for cryptographic discovery and PQC
migration on real repositories with adjudicated ground truth and
differential-execution correctness checking. State-of-the-art LLM agents achieve
D% discovery recall and only M% behaviorally-correct migration, with failures
concentrated in [indirect algorithm selection / in-house wrappers / stored
artifact formats]. A verifier-in-the-loop agent design raises correctness to M'.*

**Method.**
1. **The ground truth is the contribution.** Select N real OSS repositories across
   languages. Derive inventory by triangulating static analysis (CodeQL, Semgrep
   crypto queries), dynamic tracing of calls into libcrypto/JCA/`cryptography`,
   and expert adjudication of disagreements. **Publish inter-annotator
   agreement.** This is what makes it a benchmark rather than a demo.
2. **Include the hard cases deliberately:** config-driven algorithm selection,
   in-house crypto wrappers, crypto inside transitive dependencies, dead-but-
   present crypto, and — the real agility killer — *stored artifacts whose format
   encodes the algorithm*.
3. **Correctness oracle.** Differential testing: original vs. migrated under the
   project's own test suite plus generated property tests (round-trip, interop
   against liboqs/oqs-provider vectors, negative tests for downgrade).
4. **Agent design.** Compare single-shot LLM, RAG over standards and library docs,
   tool-using agent with compiler/test feedback, and a verifier-in-the-loop design
   where a static checker rejects candidate patches. Ablate every component.
5. **Contamination control.** Evaluate on repositories/commits postdating model
   cutoffs and on mutated variants, so you are measuring capability rather than
   memorization.

**Evidence needed.** A released, versioned, documented artifact. Error taxonomy
with counts. Multiple models, ≥5 seeds, confidence intervals. Comparison against
whatever commercial CBOM tooling you can access.

**What you need.** Workstation + API credits + CI compute. Cheapest Tier-A entry.

**Venue.** **IEEE TSE** or **ACM TOSEM** (SE framing), **IEEE TIFS** (security
framing). Pick framing by which reviewer pool you want.

**Risk.** Medium-high scoop risk — obvious idea, commercial incentive.
**Mitigation: differentiate on the correctness oracle and the hard-case taxonomy,
never on "we prompted an LLM."** Anyone can prompt; almost nobody will do the
ground-truth work. If scooped on the headline, your benchmark remains the
evaluation substrate others cite.

---

## T3 — [TIER A] Cross-dataset generalization of deep-learning side-channel attacks on ML-KEM / ML-DSA

**This replaces the lab-based SCA problem from the earlier draft.** You do not
need an oscilloscope. Public traces exist:

| Dataset | Content |
|---|---|
| DTDS | ~60,000 power traces of Dilithium signing, Cortex-M4 reference implementation, with intermediate values — <https://doi.org/10.57760/sciencedb.j00173.00001> |
| Kyber pair-pointwise set | Power traces of pair-pointwise multiplication in ML-KEM decapsulation, PQClean reference — <https://eprint.iacr.org/2025/811> |
| Unified ML-KEM/ML-DSA hardware set | Power traces from a unified FIPS 203/204 hardware implementation — <https://zenodo.org/records/18681117> |
| ELMO / MAPS | *Simulated* leakage emulators for ARM Cortex-M — generate your own traces in software |

**Gap.** Nearly every published DL-SCA result is trained and tested on traces from
one device, one implementation, one capture campaign. The known, unsolved,
practically decisive problem is **portability**: models collapse across devices,
compilers, and capture setups. Single-lab papers structurally cannot study this —
they have one rig. **You, with multiple public datasets, are better positioned
than a lab is.** That is the framing that turns your constraint into your angle.

**Claim.** *We show that deep-learning side-channel models for ML-KEM and ML-DSA
degrade by X% when transferred across implementations, devices, and capture
campaigns, identify the leakage-representation causes, and present a
domain-adaptation method recovering Y% of the loss with Z traces on the target —
evaluated across four public datasets plus emulated leakage.*

**Method.**
- Establish a **common evaluation protocol** across the public datasets
  (alignment, normalization, points-of-interest selection, guessing-entropy
  reporting). The absence of one is itself a documented problem in this subfield —
  producing it is a secondary contribution.
- Cross-dataset matrix: train on each, test on all. Report guessing entropy and
  traces-to-disclosure with confidence intervals over repeated key setups.
- Diagnose *why* transfer fails: is it misalignment, amplitude scaling, leakage
  model drift, or genuinely different leaking intermediates? Use the emulator
  (ELMO/MAPS) as a controlled ground truth where you can vary one factor at a time
  — something no physical rig can do cleanly.
- Remedy: domain adaptation, trace augmentation, or leakage-invariant
  representation learning. Report how many target-domain traces you need.
- Extend to **ML-DSA's rejection loop** specifically — rejected signing trials
  consume secret-dependent computation and constitute an attack surface with no
  classical analogue. DTDS gives you the traces to study it.

**Evidence needed.** Guessing entropy, not accuracy. Comparison against tuned
classical CPA/template baselines. Results on masked or protected targets where the
datasets permit — attacks on unprotected reference code alone no longer clear
review. Released code and evaluation protocol.

**What you need.** One GPU. Disk for trace datasets. **No lab hardware.**

**Venue.** **IEEE TIFS** (primary), IEEE Transactions on Computers, IEEE TETC.
*Note:* IACR TCHES is the field's top venue but is not an IEEE/ACM Transaction —
excluded under your constraint.

**Risk.** Medium. Dataset quality is outside your control; check each set's
documentation before committing. Failure mode is that transfer works fine and you
have no problem — unlikely given published evidence, and a rigorous negative
result across four datasets is still publishable.

---

## T4 — [TIER A] Timing and microarchitectural leakage in the *deployed* PQC stack, with LLM-assisted localization

**Gap.** KyberSlash showed that reference PQC implementations shipped with
secret-dependent timing. Tooling now exists (dudect, TIMECOP, MicroWalk,
Binsec/Rel2, DATA, CT-KAT) and systematic screening of NIST candidates has begun.
Two gaps remain: (a) work targets *reference* implementations, not the
compiled, optimized, platform-specific builds that actually ship in liboqs,
OpenSSL providers, BoringSSL, and language bindings — where compiler
optimization can *reintroduce* violations that source-level analysis clears;
(b) the tools report violations but localization and repair remain manual.

**Claim.** *We show that N constant-time violations in production PQC builds are
introduced by the toolchain rather than the source, invisible to source-level
verification, and dependent on compiler, optimization level, and target
architecture. We further show that LLM-assisted localization and repair resolves
R% of them, validated against ground truth from [DATA/MicroWalk/Binsec].*

**Method.**
- Build a matrix: {ML-KEM, ML-DSA, SLH-DSA, HQC} × {GCC, Clang, MSVC} ×
  {-O0..-O3, LTO} × {x86-64, ARM64} × {liboqs, OpenSSL provider, language
  bindings}. Run the analysis toolchain over every cell.
- Attribute each violation: source-level, toolchain-introduced, or binding-layer.
  The toolchain-introduced class is your headline.
- Where a violation is found, build the actual timing distinguisher and measure
  it, so you report exploitability rather than a policy violation.
- **LLM layer:** given a tool-reported violation, can a model localize the
  offending construct and produce a patch that (i) preserves known-answer test
  vectors and (ii) makes the tool report clean? Ground truth comes free from the
  tools. This gives you a rigorous LLM evaluation with an *automatic* oracle —
  rare and valuable.

**Evidence needed.** The full matrix, not cherry-picked cells. Measured timing
distinguishers for claimed exploitable cases. Responsible disclosure to
maintainers before submission, documented. LLM results with contamination control
and multiple seeds.

**What you need.** Workstation only. This is the lowest-cost Tier-A problem here.

**Venue.** **IEEE TSE** or **IEEE TDSC** (the toolchain/SE framing), **IEEE
TIFS** (the attack framing).

**Risk.** Medium. The subfield is active (CT-KAT, PQDSS screening, DATA-vs-
MicroWalk comparisons all landed 2025-2026), so **your novelty must be the
toolchain-introduced-violation axis and the LLM repair oracle, not "we ran
existing tools."** Verify early that toolchain-introduced violations actually
exist in meaningful numbers — a two-week pilot on one algorithm tells you
whether the paper is there.

---

## T5 — [TIER B] Post-quantum provenance and delegation for agentic systems

**Gap.** Agent frameworks (MCP, A2A-style protocols, tool-calling stacks) have no
verifiable delegation chain: when agent A asks B which asks C to act, C cannot
cryptographically verify origin, scope, or freshness of authority. Proposals use
classical signatures. PQ signature sizes (ML-DSA ~3.3KB, SLH-DSA up to ~50KB)
collide with high-frequency agent messaging in a way nobody has measured or
designed around.

**Claim.** *We define a capability-based post-quantum delegation credential
binding each tool invocation to an unforgeable, scoped, attenuable chain of
authority. Naive per-message ML-DSA signing costs X ms and Y bytes at realistic
agent message rates; our batched-commitment construction reduces this to Z with a
proved security property.*

**Method.** Formalize delegation with attenuation (macaroon- or biscuit-style)
over a PQ signature scheme — a sub-agent must only be able to *narrow* authority.
Instantiate with ML-DSA, SLH-DSA, and a hybrid mode. **The research content is
amortization:** Merkle-batched attestation over an agent's action log, few-time PQ
signatures on the hot path anchored to a long-term ML-DSA key, or transcript
commitments signed only at checkpoints — with an explicit statement of what an
attacker can do *between* checkpoints. Evaluate on a real agent workload
(AgentDojo-class harness), not a synthetic loop. Give a game-based security
definition; mechanize the protocol layer in Tamarin or ProVerif if you can.

**What you need.** Workstation. Substantial engineering time.

**Venue.** **IEEE TDSC** (primary), ACM TOPS, IEEE Transactions on Services
Computing.

**Risk.** Medium. Failure mode is producing integration engineering with no
research claim. **The amortization result is the paper** — if you cannot find a
non-obvious construction, downgrade to a measurement study and fold it into T6.

---

## T6 — [TIER B] Cryptographic agility as a measurable property of ML systems

**Gap.** "Agility" is invoked constantly and defined loosely. Application-level
assessment frameworks exist, but ML systems have an unstudied profile: enormous
signed binary artifacts, derivative lineage (base → fine-tune → merge → quantize),
millisecond latency budgets, and datasets outliving several algorithm generations.

**Claim.** *We define a computable agility metric for ML systems — the cost, in
changed call-sites and invalidated stored artifacts, of replacing primitive p —
apply it to N widely-used ML platforms, and show agility failures cluster in
stored artifact formats that hard-encode algorithm identifiers.*

**Method.** Make the metric **computable from source** — build the analyzer, run
it, report numbers. Target model hubs, serving stacks, feature stores, federated
learning frameworks. The interesting failures live in safetensors metadata,
checkpoint headers, and model-card signatures. Propose an intent-based crypto API
shim and demonstrate measured migration-cost reduction.

**A high-value sub-finding to chase:** TEE attestation chains for confidential
inference (SEV-SNP, TDX, GPU confidential computing) are rooted in classical
ECDSA in hardware that is **not field-upgradeable**. If that holds up under
examination, it is alarming, underexamined, and possibly a paper of its own.

**What you need.** Workstation.

**Venue.** **IEEE TDSC**, IEEE TETC, IEEE TSE.

**Risk.** Medium — risk is that it reads as a survey. The computable metric and
the released tool are what prevent that.

---

## T7 — [TIER B] Prefix-cache and KV-cache side channels in multi-tenant LLM serving

**Gap.** Prefix caching, paged attention, and speculative decoding create timing
differences dependent on other tenants' data. Some prompt-cache timing attacks
exist; missing is systematic treatment across the modern serving stack, leakage
quantified in bits, and a mitigation with measured throughput cost.

**Claim.** *Prefix-cache sharing in production LLM serving leaks O(b) bits about
co-tenant prompts per query; we systematize the leakage across
[cache policy × batching × speculative decoding] and give a partitioning /
constant-admission mitigation costing X% throughput.*

**Method.** Standard side-channel methodology transplanted: build the oracle,
quantify with mutual information rather than anecdotal success rates, sweep
configurations, then defend and measure the cost precisely — throughput is the
entire reason vendors enable sharing.

**What you need.** One GPU running vLLM or SGLang with a small model. The
cache-hit timing oracle is measurable with 7B-class or smaller models; you do not
need frontier-scale serving.

**Venue.** **IEEE TIFS**, IEEE TDSC, IEEE Transactions on Cloud Computing, IEEE
TPDS.

**Risk.** Medium-high scoop risk; systems-heavy. Note this problem carries **no
PQC content** — include it only if your thesis spine is confidentiality of ML
systems broadly.

---

## T8 — [TIER C] Post-quantum secure aggregation for federated learning under realistic dropout

**Gap.** Classical secure aggregation rests on pairwise Diffie-Hellman masking.
PQ replacements change the cost profile substantially, and dropout-recovery
machinery interacts with PQ key sizes in ways that are asserted rather than
measured. Most published work simulates rather than measures.

**Claim.** *We give a PQ secure-aggregation protocol scaling as X in client count
and evaluate it on real constrained devices under measured dropout traces,
establishing feasibility bounds that current simulated work overstates.*

**What you need.** Workstation, plus optionally 5-10 Raspberry Pi / ESP32-class
boards (cheap, classical, ~₹15k total) — the *real device* measurement is
precisely your differentiator against simulation-based work.

**Venue.** **IEEE TIFS**, IEEE TDSC, IEEE Transactions on Mobile Computing.

**Risk.** Medium; somewhat crowded.

---

## T9 — [TIER C] Formal capability bounds for tool-using agents

**Gap.** Everyone builds prompt-injection detectors; almost nobody states a
theorem. Since instruction/data separation is architecturally impossible, the
publishable framing is **containment**, not detection.

**Claim.** *Assuming the model is fully adversarially controlled, an agent
architecture enforcing [capability restriction / information-flow labels /
plan-then-execute with a non-LLM validator] admits no execution trace violating
policy P. We implement it and measure the utility cost, retaining X% task
completion under an adaptive attacker.*

**Method.** Adopt "assume the model is compromised" — intellectually correct, and
it sidesteps the impossibility entirely. Prove non-interference for the
*architecture*, not the model. Then pay the bill honestly: measure how much task
capability you lose, because that trade is why such designs are not deployed.

**What you need.** Workstation + API credits.

**Venue.** **IEEE TDSC**, ACM TOPS, IEEE TIFS.

**Risk.** High competition — strong groups and frontier labs work here, design-
pattern papers exist. Enter only with a formal layer (mechanized proof or real IFC
implementation). **The utility-cost measurement is the underserved half** — that
is your opening.

---

## T10 — [TIER C] Quantum cryptanalytic resource estimation for ML asset lifetimes

**This is your quantum chapter, and it runs entirely on your laptop.** Resource
estimation is *classical computation about quantum algorithms* — no quantum
hardware, ever.

**Gap.** PQC migration prioritization is driven by generic guidance. Nobody has
derived per-asset-class migration deadlines for ML infrastructure by combining
concrete quantum attack cost models with measured data-lifetime distributions.

**Claim.** *Combining logical-qubit and T-gate cost estimates for attacking the
key-exchange and signature configurations actually deployed in ML infrastructure
with measured confidentiality-lifetime distributions per asset class, we derive
migration deadlines showing that [embedding stores / training corpora / model
signing keys] require action N years earlier than current guidance implies.*

**Method.** Use existing estimation tooling — the lattice-estimator for PQ
parameter security, and Azure Quantum Resource Estimator or Qualtran-style
tooling for Shor/Grover cost models against the *classical* algorithms still
deployed. Pair with lifetime data gathered in T1 and T6. Present everything
parametrically over hardware assumptions; never state a Q-day prediction.

**What you need.** Laptop. Software only.

**Venue.** IEEE TETC, IEEE TDSC. **IEEE Transactions on Quantum Engineering is a
plausible home but its stated scope emphasizes quantum information and quantum
cryptography rather than classical PQC — email the editors with a one-paragraph
abstract before investing.** Realistically this is strongest as a *chapter and a
section of T1*, not a standalone paper.

**Risk.** Medium. Risk is that it reads as arithmetic over other people's models.
Mitigate by making the *lifetime measurement* the novel input.

---

## Removed from the earlier draft

| Was | Why removed |
|---|---|
| QRNG-backed entropy for DP guarantees | Requires quantum randomness infrastructure you do not have. The *classical* half — auditing DP-SGD implementations for non-cryptographic PRNG seeding — remains valid and could be folded into T1 as a side contribution, or run as a small standalone for IEEE TIFS. |
| Lab-based DL-SCA with ChipWhisperer | Replaced by T3, which uses public datasets and emulated leakage, and asks a better question (portability) as a result. |
| QML for LLM security | No mechanism, no advantage on classical data, and the literature is not credible. Barren plateaus and dequantization argue against it. Do not build on it. |

---

## Ranked shortlist

| Rank | Problem | Tier | Hardware needed | Transactions target | Scoop risk |
|---|---|---|---|---|---|
| 1 | **T1** HNDL vs. RAG/embeddings | A | 1 GPU | IEEE TIFS | Medium |
| 2 | **T4** Toolchain-introduced PQC timing leakage + LLM repair | A | None | IEEE TSE / TDSC | Medium |
| 3 | **T2** Crypto discovery & migration benchmark | A | None | IEEE TSE / TOSEM | High |
| 4 | **T3** Cross-dataset DL-SCA generalization | A | 1 GPU | IEEE TIFS / TC | Medium |
| 5 | **T5** PQ delegation for agents | B | None | IEEE TDSC | Low |
| 6 | **T6** Agility metrics for ML systems | B | None | IEEE TDSC / TETC | Low |
| 7 | **T7** KV-cache side channels | B | 1 GPU | IEEE TIFS / TCC | High |
| 8 | **T8** PQ secure aggregation | C | Optional Pis | IEEE TIFS / TMC | Medium |
| 9 | **T9** Formal agent containment | C | None | IEEE TDSC / TOPS | Very high |
| 10 | **T10** Quantum resource estimation for ML lifetimes | C | None | IEEE TETC (or a chapter) | Low |
