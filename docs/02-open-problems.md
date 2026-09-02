# 2. Open Problem Catalog

Ten problems, ranked by *expected Q1 yield per unit of risk* for a PhD student
with modest GPU access, ~₹50k of embedded hardware budget, and a 4-year horizon.

Each entry uses a fixed schema so you can compare them honestly:

- **Gap** — what nobody has established
- **Claim** — the sentence your paper's abstract would contain
- **Method** — how you would actually get there
- **Evidence needed** — what a Q1 reviewer will demand before believing you
- **Resources** — what it costs you
- **Venue** — realistic targets
- **Risk** — scoop risk, failure modes, and what you salvage if it dies

Tiering: **A** = do this; **B** = strong second paper; **C** = viable but only
with a specific enabling condition; **D** = avoid as a primary contribution.

---

## P1 — [TIER A] Harvest-Now-Decrypt-Later against RAG and embedding stores

**Gap.** HNDL is always argued about *generic* long-lived secrets. Nobody has
established that vector databases and embedding traffic are a *distinctively
severe* HNDL target, nor quantified it. Two known results have never been
composed: (a) embeddings are invertible — text can be substantially reconstructed
from dense vectors (Song & Raghunathan's inversion work, and the vec2text line
of work showing near-verbatim recovery); (b) TLS sessions recorded today under
ECDHE are decryptable by a future CRQC.

**Claim.** *Enterprise RAG deployments constitute a worst-case harvest-now-
decrypt-later target: they transmit and store dense representations of documents
whose confidentiality lifetime exceeds the projected CRQC horizon, those
representations are invertible to near-verbatim text, and the overwhelming
majority of deployed embedding APIs and vector stores still negotiate classical
key exchange. We quantify the resulting exposure and give a hybrid-PQ +
representation-hardening mitigation with a measured utility bound.*

**Method.**
1. **Measurement.** Scan the reachable surface of embedding APIs, managed vector
   DBs (Pinecone, Weaviate, Qdrant, Milvus, pgvector deployments), and popular
   self-hosted stacks for negotiated key-exchange groups. Determine what fraction
   offer/negotiate X25519MLKEM768 or equivalent vs. pure classical. This is a
   clean, citable measurement nobody has published for this stack specifically.
2. **Inversion fidelity.** Reproduce embedding inversion across current embedding
   models and dimensions. Report recovery as a function of model family,
   dimensionality, and whether the attacker knows the embedding model. Include
   domain corpora with genuinely long confidentiality lifetimes (de-identified
   clinical notes, legal filings, patents-in-prep).
3. **Exposure model.** Formalize risk as a function of
   `P(CRQC by year t) x data_confidentiality_lifetime x inversion_fidelity x
   interception_feasibility` — and be explicit that the CRQC term is a *policy
   input*, not your prediction. Present results parametrically over it. This is
   how you avoid the "you're guessing about quantum timelines" reviewer objection.
4. **Mitigation.** Hybrid PQ key exchange for the transport leg *plus*
   representation hardening at rest (e.g. bounded random rotation/noise with a
   retrieval-quality guarantee, or storing only reduced representations). Measure
   the retrieval-quality/inversion-resistance Pareto frontier on standard IR
   benchmarks (BEIR/MTEB subsets).

**Evidence needed.** Real measurement numbers, not a survey. An inversion
reproduction with a strong baseline. A mitigation with a *measured* utility cost,
not an assertion that the cost is small. Threat model stated with the adversary's
capabilities and the exact assumption about CRQC arrival.

**Resources.** Modest. One GPU for inversion training. No quantum hardware. No
embedded hardware. This is the cheapest Tier-A problem here.

**Venue.** IEEE TIFS; ACM TOPS; Computers & Security; PoPETs (if you lean
privacy). A short version could go to a security conference first.

**Risk.** Low-to-medium. Scoop risk is real because the ingredients are public —
move fast on the measurement, which is the part that ages. If inversion fidelity
turns out low for modern models, that is *still a paper* (a negative result that
bounds the threat), which is why this is Tier A: it cannot fully fail.

---

## P2 — [TIER A] Deep-learning side-channel analysis of ML-DSA's rejection loop

**Gap.** ML-KEM decapsulation is heavily studied. ML-DSA signing is studied less,
and the *rejection-sampling* structure is a leakage surface with no classical
analogue: a signature attempt that gets rejected still consumes secret-dependent
computation and still leaks. Existing work has begun exploiting rejected trials;
what is missing is (a) a systematic leakage characterization across the whole
rejection loop, (b) non-profiled and portability-robust attacks, and (c) a
countermeasure with a measured cost.

**Claim.** *We characterize secret-dependent leakage across ML-DSA's rejection
loop on an embedded target, demonstrate a non-profiled deep-learning attack that
recovers signing-key material from N traces without a cloned device, show it
transfers across devices and compilation settings, and evaluate a targeted
countermeasure costing X% signing throughput.*

**Method.**
- Target: `pqm4` (the standard ARM Cortex-M4 PQC benchmarking suite) on an
  STM32F4 discovery board, captured with ChipWhisperer (Husky or Lite) or a
  Picoscope + EM probe.
- Build a leakage map: instrument each phase (`ExpandMask`, NTT/INTT, `HighBits`/
  `LowBits` decomposition, hint computation, the rejection checks) and localize
  leakage with TVLA plus a learned leakage detector.
- Attack: non-profiled deep learning (a small network replacing CPA's correlation
  as the distinguisher — this is the current frontier because it works against
  countermeasures where a fixed leakage model fails). Then push to masked
  implementations.
- **Portability** is where papers get accepted or rejected: train on device A,
  attack device B, different compiler flags, different clock. Report the drop
  honestly and address it (domain adaptation, trace augmentation).
- Countermeasure: shuffling within the rejection loop, or masking the specific
  leaking intermediate you identified. Measure cycles, RAM, code size on the
  same board.

**Evidence needed.** Traces-to-key-recovery with confidence intervals over
repeated key setups. Comparison to a properly tuned classical CPA/template
baseline. A masked-implementation result, not just unprotected. Public trace
dataset + code release. **Do not** publish an attack on an unprotected reference
implementation only — reviewers now treat that as insufficient.

**Resources.** ChipWhisperer-Husky or Lite + STM32 target: roughly ₹40k-₹1.5L
depending on kit. One GPU. Time: expect 4-6 months before the first clean result.
This is the highest-credibility leg of your thesis and the one that will most
impress a viva committee, because it is *measurement on real hardware*.

**Venue.** IACR TCHES (the gold standard for this; it is a journal-style venue
with rolling submissions); IEEE TIFS; IEEE Transactions on Computers; IEEE TVLSI
if you go hardware-heavy. Note TCHES is the reputational win even where your
university's rules care about JCR quartiles — pair it with a TIFS extension.

**Risk.** Medium. Crowded field, fast-moving, and you must get the measurement
setup right (bad traces waste months). Mitigation: start with a *reproduction* of
a published ML-KEM attack to validate your rig before attempting novel ML-DSA
work. That reproduction is also a useful artifact.

---

## P3 — [TIER A] A benchmark and agent for cryptographic discovery and migration correctness

**Gap.** Everyone agrees LLMs should help with PQC migration (H8/H9). Empirical
work so far shows LLMs detect crypto *misuse* reasonably but do not reliably
perform end-to-end migrations, and the existing evaluations use small synthetic
paired-fragment datasets. There is no benchmark with (a) real-world code, (b)
ground-truth crypto inventory, (c) executable behavioral equivalence checking,
and (d) an adversarial split that resists memorization.

**Claim.** *We present CryptoMig-Bench, the first benchmark for cryptographic
discovery and PQC migration on real repositories with verified ground truth and
differential-execution correctness checking, and show that state-of-the-art LLM
agents achieve D% discovery recall and only M% behaviorally-correct migration,
with failures concentrated in [specific categories]. We give an agent design that
improves correctness to M' by [mechanism].*

**Method.**
1. **Ground truth is the contribution.** Build it semi-automatically: select N
   real OSS repositories across languages; derive crypto inventory by combining
   static analysis (CodeQL/Semgrep crypto queries), dynamic tracing of calls into
   libcrypto/JCA/`cryptography`, and expert adjudication of disagreements. Publish
   inter-annotator agreement. This is the part that makes it a benchmark rather
   than a demo.
2. **Include hard cases deliberately:** indirect/config-driven algorithm
   selection, in-house crypto wrappers, crypto in dependencies, crypto in
   compiled artifacts, dead-but-present crypto, and *stored* artifacts whose
   format encodes the algorithm (the real agility killer).
3. **Correctness oracle.** Migration is only correct if behavior is preserved
   where it must be and changed where it must be. Use differential testing:
   original vs. migrated under the project's own test suite plus generated
   property tests (round-trip, interop against liboqs/OQS-OpenSSL vectors,
   negative tests for downgrade).
4. **Agent design.** Compare: single-shot LLM, RAG over standards + library docs,
   tool-using agent with compiler/test feedback, and a verifier-in-the-loop design
   where a static checker rejects candidate patches. Ablate.
5. **Contamination control.** Report results on repositories/commits after model
   cutoffs, and on mutated variants, to show you are not measuring memorization.

**Evidence needed.** A released, documented, versioned benchmark artifact. Error
taxonomy with counts. Multiple models and multiple seeds with confidence
intervals. Comparison against commercial CBOM tooling where accessible.

**Resources.** Cheap — API credits and CI compute. No hardware.

**Venue.** IEEE TIFS; IEEE Transactions on Software Engineering; Empirical
Software Engineering; Computers & Security; ACM TOSEM. A benchmark paper with a
real artifact is highly citable and gives you a platform for follow-ups.

**Risk.** Medium-high scoop risk — this is an obvious idea whose time has come,
and industry has commercial incentive. **Mitigation: differentiate on the
correctness oracle and the hard-case taxonomy, not on "we prompted an LLM".**
Anyone can prompt; almost nobody will do the ground-truth work. If scooped on the
headline, your benchmark still stands as the evaluation substrate others use.

---

## P4 — [TIER B] Post-quantum provenance and delegation for agentic systems

**Gap.** Agent frameworks (MCP, A2A-style protocols, tool-calling stacks) have no
verifiable delegation chain: when agent A asks B which asks C to spend money, C
cannot cryptographically verify the origin, scope, or freshness of the authority.
Existing work proposes classical signing; PQ signature sizes (ML-DSA ~3.3KB,
SLH-DSA up to ~50KB) collide with high-frequency agent messaging in a way nobody
has measured or designed around.

**Claim.** *We define a capability-based, post-quantum delegation credential for
multi-agent systems that binds each tool invocation to an unforgeable, scoped,
attenuable chain of authority; we show naive per-message ML-DSA signing costs
X ms and Y bytes of overhead at realistic agent message rates, and present a
batching/aggregation construction reducing this to Z with a formal security
argument.*

**Method.**
- Formalize the delegation model (macaroon-style attenuation, or biscuit-style
  with a PQ signature scheme underneath). Attenuation is the key property: a
  sub-agent should only be able to *narrow* authority, never widen it.
- Instantiate with ML-DSA and with SLH-DSA; hybrid mode with Ed25519.
- The real research content: **amortization**. Per-message PQ signatures are too
  expensive; explore Merkle-batched attestation over an agent's action log, PQ
  one-time/few-time signatures for the hot path anchored by a long-term ML-DSA
  key, or a transcript-commitment design where only checkpoint boundaries are
  signed. Prove what you get and what you give up (what an attacker can do
  *between* checkpoints).
- Evaluate on a real agent workload — not a synthetic loop. Use an existing agent
  benchmark harness so numbers are comparable.
- Security argument: at minimum a careful game-based definition and proof sketch;
  ideally mechanized (Tamarin/ProVerif) for the protocol layer.

**Evidence needed.** A working implementation integrated with a real agent
framework. Latency/bandwidth measurements at multiple message rates. A stated,
proved security property. An attack you *prevent*, demonstrated end-to-end.

**Resources.** Software only. Substantial engineering.

**Venue.** IEEE TDSC; IEEE TIFS; ACM TOPS; IEEE Internet of Things Journal (if
you frame edge/IoT agents); Computer Networks.

**Risk.** Medium. Failure mode is producing "integration engineering" with no
research claim. **The batching/amortization result is what makes it a paper** —
if you cannot find a non-obvious construction there, downgrade this to a
measurement study and fold it into P1 or P5.

---

## P5 — [TIER B] Cryptographic agility as a measurable property of ML systems

**Gap.** "Cryptographic agility" is invoked constantly and defined loosely.
Recent work proposes assessment frameworks at the application level, but ML
systems have a distinctive and unstudied profile: enormous signed binary
artifacts, derivative lineage (base → fine-tune → merge → quantize), latency
budgets measured in milliseconds, and datasets that outlive several algorithm
generations.

**Claim.** *We define an agility metric for ML systems, apply it to N widely-used
ML platforms (model hubs, serving stacks, feature stores, federated learning
frameworks), and show that agility failures cluster in [artifact formats /
derivative lineage / config-driven negotiation], with a proposed
interface-level remedy.*

**Method.** Define agility operationally — e.g. *the cost, in changed
call-sites and broken stored artifacts, of replacing primitive p* — then measure
it across real systems. Formats that embed algorithm identifiers in stored
artifacts (safetensors metadata, checkpoint headers, model-card signatures) are
where you will find the interesting failures. Propose an intent-based crypto API
shim and demonstrate migration cost reduction.

**Venue.** Computers & Security; IEEE TDSC; Journal of Systems and Software;
IEEE Software (for a practitioner-facing version).

**Risk.** Medium. Risk is that it reads as a survey. Fix by making the metric
*computable from source* — build a tool, run it, report numbers.

---

## P6 — [TIER B] KV-cache and prompt-cache side channels in multi-tenant serving

**Gap.** Prefix caching, paged attention, and speculative decoding all create
observable timing differences that depend on other tenants' data. Some
prompt-cache timing attacks exist; what is missing is a systematic treatment
across the modern serving stack (vLLM/SGLang-class systems), a leakage
quantification in bits, and a mitigation with a measured throughput cost.

**Claim.** *We show that prefix-cache-sharing policies in production LLM serving
leak O(b) bits about co-tenant prompts per query, systematize the leakage across
[cache policy x batching x speculative decoding], and give a partitioning/
constant-time-admission mitigation costing X% throughput.*

**Method.** Classic side-channel methodology transplanted: build the oracle,
quantify with mutual information rather than anecdotal success rates, evaluate
across configurations, then defend (per-tenant cache partitioning, randomized
admission, cache-hit response padding) and measure the cost precisely — the
throughput cost is the whole reason vendors enable sharing.

**Venue.** IEEE TIFS; IEEE TDSC; ACM TOPS.

**Risk.** Medium-high scoop risk; systems-heavy. Strong fit if you enjoy systems
measurement. Note this problem has *no PQC content* — it belongs in your thesis
only if your spine is "confidentiality of AI systems" broadly.

---

## P7 — [TIER C] Certified/quantum randomness for cryptographic and DP guarantees in ML pipelines

**Enabling condition:** you can access a QRNG (cloud QRNG API, a university
physics-department device, or a randomness beacon) — no quantum computer needed.

**Gap.** Differential privacy guarantees and key generation both assume a good
entropy source; in practice ML pipelines seed noise from framework PRNGs
(`numpy`, `torch`) that are non-cryptographic, sometimes deterministically
seeded for reproducibility, and occasionally shared across workers. The gap
between the *proved* DP guarantee and the *delivered* guarantee under a real RNG
is not well characterized.

**Claim.** *We show that common DP-SGD implementations seed noise from
non-cryptographic PRNGs in ways that materially weaken the delivered privacy
guarantee under a realistic adversary, quantify the gap, and demonstrate a
QRNG/CSPRNG-backed noise pipeline that closes it at X% training overhead.*

**Method.** Audit real DP libraries (Opacus, TF-Privacy, JAX pipelines) for
seeding and worker-sharing behavior. Construct a concrete distinguishing or
reconstruction attack that exploits predictable noise. Then measure the fix.

**Venue.** Computers & Security; IEEE TIFS; PoPETs; Quantum Information
Processing (for a quantum-framed version).

**Risk.** Medium. **This is your honest "quantum" contribution** if you want the
word in the thesis without QML hand-waving. Downside: the quantum part is thin —
the paper's strength is the *DP-implementation audit*, and the QRNG is the
remedy. Frame it that way and it is solid; frame it as "quantum-enhanced privacy"
and it is not.

---

## P8 — [TIER C] Post-quantum secure aggregation for federated learning under realistic dropout

**Gap.** Classical secure aggregation (Bonawitz-style) rests on Diffie-Hellman
pairwise masking. PQ replacements change the cost profile substantially, and the
dropout-recovery machinery interacts with PQ key sizes in ways that are asserted
rather than measured. Some work exists; the gap is a rigorous cost model under
*realistic* mobile/edge dropout distributions plus constrained-device measurement.

**Claim.** *We give a PQ secure-aggregation protocol whose communication scales
as X in the number of clients, and evaluate it on real embedded hardware under
measured dropout traces, showing feasibility bounds current work overstates.*

**Venue.** IEEE IoT Journal; IEEE TDSC; Future Generation Computer Systems; IEEE
Transactions on Mobile Computing.

**Risk.** Medium. Somewhat crowded. Differentiate via *real device* measurement
(Cortex-M / Raspberry Pi class) rather than simulation — most published work
simulates, which is the weakness you exploit.

---

## P9 — [TIER C] Formal capability bounds for tool-using agents (the "provable" prompt-injection direction)

**Gap.** Everyone builds injection detectors; almost nobody states a theorem.
The publishable framing is not detection but *containment*: what can an adversary
who fully controls the model's output achieve, given a capability/IFC layer?

**Claim.** *Under the assumption that the model is fully adversarially
controlled, an agent architecture enforcing [capability restriction /
information-flow labels / plan-then-execute with a non-LLM validator] admits no
execution trace violating policy P; we implement it and measure the utility cost
on [agent benchmark], showing X% task completion retained.*

**Method.** Adopt the "assume the model is compromised" threat model — this is
the intellectually correct move and it dodges H1 entirely. Define policies over
tool invocations and data labels. Prove non-interference for the architecture,
not the model. Then pay the bill: measure how much task capability you lose,
because that is the honest trade and the reason such designs are not deployed.
Evaluate on established agent-security benchmarks with an *adaptive* attacker.

**Venue.** IEEE TDSC; ACM TOPS; IEEE TIFS. Top-tier conferences (S&P/USENIX/CCS)
are the natural home if you can get there.

**Risk.** High competition — several strong groups and frontier labs work here,
and design-pattern papers already exist. Enter only if you can bring the formal
layer (a mechanized proof, or a real IFC implementation), not another pattern
catalog. **The utility-cost measurement is the underserved half** — that is your
opening.

---

## P10 — [TIER D] "Quantum-enhanced" LLM security (QML classifiers, quantum embeddings, QNN intrusion detection)

**Do not build a thesis on this.** Stated plainly so you can point at this
section when someone suggests it:

- No mechanism connects variational circuits to any LLM security task better
  than a classical model of equal parameter count.
- Barren plateaus and dequantization results actively argue *against* advantage
  on classical data; recent theory ties trainability to classical simulability,
  meaning circuits you *can* train are circuits a classical machine can imitate.
- Data loading destroys claimed speedups for classical inputs.
- The existing literature is dominated by simulated small circuits on toy
  datasets without tuned classical baselines. Q1 security reviewers know this now.

**The one publishable move in this space is negative or systematizing:** a
rigorous reproduction study showing that published QML-for-security results do
not survive properly tuned classical baselines, hardware noise, or realistic
data — with a reproducibility checklist for the subfield. That is genuinely
useful, genuinely citable, and a good *fourth* paper, not a first one. It also
requires you to be socially careful about how you write it.

---

## Ranked shortlist

| Rank | Problem | Tier | Cost | Scoop risk | Q1 fit |
|---|---|---|---|---|---|
| 1 | **P1** HNDL vs. RAG/embeddings | A | Low | Medium | Very high |
| 2 | **P2** DL-SCA on ML-DSA rejection loop | A | Medium (hardware) | Medium | Very high |
| 3 | **P3** CryptoMig-Bench | A | Low | High | High |
| 4 | **P4** PQ delegation for agents | B | Medium | Low | High |
| 5 | **P5** Agility metrics for ML systems | B | Low | Low | Medium-high |
| 6 | **P6** KV-cache side channels | B | Medium | High | High |
| 7 | **P7** QRNG for DP/keying | C | Low | Low | Medium |
| 8 | **P8** PQ secure aggregation | C | Low-med | Medium | Medium |
| 9 | **P9** Formal agent containment | C | Medium | Very high | Very high if landed |
| 10 | **P10** QML for LLM security | D | — | — | Low |
