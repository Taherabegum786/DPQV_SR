# 1. The Landscape: What Industry Actually Cannot Do Yet

*Last updated: September 2026*

Before choosing problems, be precise about what the three fields are, because
"LLM security + quantum + PQC" is a phrase that hides three very different
maturity levels. Conflating them is the single most common reason papers in
this space get desk-rejected from serious venues.

---

## 1.0 Disambiguation: three different things get called "quantum"

You must decide, explicitly and in writing, which of these your thesis uses.
Reviewers at Q1 security venues will assume the worst reading unless you say.

| Sense | What it means | Maturity (2026) | Honest verdict for a security PhD |
|---|---|---|---|
| **Q-as-threat** | A future cryptographically-relevant quantum computer (CRQC) breaks RSA/ECC via Shor; Grover halves symmetric margins. Motivates PQC. | Threat is speculative in *timing* but certain in *kind*. Standards shipped. | **Load-bearing.** Rigorous, fundable, publishable. This is where your thesis should sit. |
| **Q-as-compute** | Quantum/variational circuits used *as* an ML substrate — "quantum neural network for intrusion detection", "quantum-enhanced LLM". | NISQ. No demonstrated advantage on any real security dataset. | **Dangerous.** High volume of weak literature. Do not make this your spine. |
| **Q-as-infrastructure** | QKD, QRNG, quantum networks — physical-layer key agreement and certified randomness. | QRNG is a real, buyable product. QKD is real but restricted (NSA/NCSC do not recommend it for general-purpose use). | **Narrow but honest.** QRNG-for-entropy is a legitimate, small contribution. QKD is largely a policy dead end for your purposes. |

**Recommendation:** build on *Q-as-threat*, allow at most one bounded
contribution from *Q-as-infrastructure*, and avoid *Q-as-compute* as a thesis
pillar. You can still cite and critique it — a well-argued negative or
systematization result about Q-as-compute in security is more publishable than
another positive claim.

---

## 1.1 LLM security: what is genuinely unsolved

### H1. Instructions and data are not separable
An LLM consumes one token stream. There is no architectural boundary between
"the system's instruction" and "content the system was asked to read". Every
deployed defense — delimiters, spotlighting, instruction hierarchies,
classifier guards, dual-LLM patterns — is a *probabilistic* mitigation over a
semantic channel. OWASP still ranks prompt injection #1; frontier labs
describe it as unsolved rather than mitigated.

Consequence for research: any paper claiming to "solve" prompt injection with a
detector will be rejected. Papers that *bound* the problem — capability
restriction, provable non-interference, information-flow control, or a rigorous
impossibility argument — are the publishable direction.

### H2. Evaluation is broken, and everyone knows it
Defenses are measured against fixed, public attack corpora. Attackers adapt;
benchmarks do not. A defense reporting "98% attack success reduction" against a
static set tells you almost nothing about its security. The field lacks:
- adaptive-attacker evaluation as a *default* requirement,
- attack-cost metrics (queries, compute, adversary knowledge) rather than pass/fail,
- benchmarks that resist contamination as models retrain on them.

This is a gap you can convert directly into a contribution.

### H3. Agentic blast radius
Tool-calling agents, MCP servers, and agent-to-agent delegation turn a text
vulnerability into an *action* vulnerability. Concrete unsolved pieces:
- authorization is coarse (an agent holds the user's full token, not a
  task-scoped capability),
- delegation chains have no verifiable provenance — B cannot prove to C that
  A actually asked for this,
- no accepted revocation or audit model for autonomous action sequences,
- Five Eyes issued joint agentic-AI guidance in 2026, which signals regulatory
  attention but not a technical solution.

### H4. Non-determinism defeats classical assurance
Security engineering rests on "we patched it; it is now fixed." A model
mitigation is a distribution shift, not a patch. There is no accepted notion of
a *fixed* LLM vulnerability, no regression semantics, and no conformance test a
vendor can pass. This blocks certification under the EU AI Act and similar
regimes.

### H5. The model supply chain is largely unauthenticated
Weights, LoRA adapters, tokenizers, datasets, and quantized derivatives are
distributed as large binary blobs. Practice is improving (model signing,
MBOM/AIBOM proposals, sigstore-style transparency), but:
- signatures, where present, are classical (Ed25519/ECDSA/RSA),
- there is no standard for signing *derivatives* (a merged/quantized/fine-tuned
  model's relationship to its parent),
- verification gates before deployment are rare in practice,
- deserialization formats remain an execution vector.

### H6. Multi-tenant inference leaks
Shared KV caches, prefix caching, speculative decoding, and batching create
timing and memory side channels across tenants. Cache-hit timing can reveal
whether another tenant submitted a given prefix. This is a classical systems
security problem that the ML serving stack reinvented, and it is
under-studied relative to its deployment scale.

---

## 1.2 PQC: what industry is stuck on

### H7. Deployment is roughly 5% against a 2030/2035 deadline
NIST finalized FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) in
August 2024, and selected HQC as a backup KEM in March 2025. NIST calls for
RSA-2048/ECC-256 deprecation by 2030 and disallowance after 2035. Enterprise
uptake remains a small single-digit percentage. Large estates starting in 2026
do not expect completion before the early 2030s.

### H8. Nobody knows where their crypto is
The binding constraint is **inventory**, not algorithms. Organizations cannot
produce a cryptographic bill of materials (CBOM) across heterogeneous code,
binaries, containers, firmware, and third-party dependencies. Crypto is
hard-coded, wrapped in in-house abstractions, invoked through configuration, and
buried in dependencies of dependencies.

### H9. No cryptographic agility
Most applications cannot swap a primitive without a rewrite. Algorithm choice is
baked into APIs, wire formats, database columns, and stored artifacts.
Agility is now recognized as the real deliverable — migrate once, then be able
to migrate again cheaply (HQC exists precisely because lattice assumptions might
fall).

### H10. Size and performance are real, not theoretical
ML-KEM-768 public keys/ciphertexts are ~1.2KB each; ML-DSA-65 signatures ~3.3KB;
SLH-DSA signatures range from ~7.8KB to ~50KB. Effects: TLS ClientHello
fragmentation, larger certificate chains, DNSSEC over UDP problems, firmware
images that no longer fit in flash, and constrained IoT/OT devices with 15-30
year lifecycles and non-upgradeable firmware.

### H11. Hybrid vs. pure is a live policy split
NSA's CNSA 2.0 direction is essentially pure-PQ for national security systems;
BSI/ANSSI and much of the EU favor hybrid (classical + PQ) constructions.
Vendors must ship both. Formal analysis of hybrid combiners, downgrade
resistance, and negotiation logic is still an active area.

### H12. The implementation-security layer is immature
Twenty-five years of hardening went into RSA/ECC. Lattice schemes are new and
leaky in ways that keep being discovered:
- decapsulation in ML-KEM and signing in ML-DSA are the hot targets,
- leakage points cluster around NTT/INTT, message encoding/decoding, coefficient
  multiplication, and PRF evaluation,
- first-order masked Kyber-768 has been broken with a small number of traces in
  published work; deep-learning profiled and non-profiled attacks keep improving,
- ML-DSA's rejection-sampling loop leaks through *rejected* trials, an attack
  surface with no classical analogue,
- masking is expensive, and higher-order masking costs grow badly on embedded targets.

HSM and FIPS 140-3 validation for PQC also lags the standards.

### H13. Harvest-now-decrypt-later is already happening
Any data with a multi-decade confidentiality requirement that crosses a network
today under ECDHE is, under the threat model, already compromised. This
reframes the deadline: it is not 2035, it is *the confidentiality lifetime of
the data you are moving right now*.

---

## 1.3 Quantum computing: the honest state

- **No CRQC.** Logical-qubit counts remain orders of magnitude below what
  Shor needs for RSA-2048. Error correction is progressing but not close.
- **QML has structural obstacles.** Barren plateaus (exponentially vanishing
  gradients with system size), the data-loading/state-preparation bottleneck
  that erases most claimed speedups for classical data, and dequantization
  results showing classical algorithms matching quantum ones on the same
  problems. Recent theory reframes barren plateaus as *evidence of*
  classical simulability rather than a mere training nuisance.
- **The QML-for-security literature has a rigor problem.** Predominant pattern:
  4-16 qubit simulated circuits, KDD99/NSL-KDD/CIC-IDS toy datasets, no properly
  tuned classical baseline, no hardware run, no noise model, accuracy reported
  on data a logistic regression solves. Surveys now say this explicitly.
- **QRNG is the exception.** Certified quantum randomness is commercially
  available and has a defensible security story (entropy source quality),
  independent of any quantum-advantage claim.

**Implication:** "quantum enhancement" of LLM security, in the *Q-as-compute*
sense, currently has no credible mechanism. If you want quantum in your thesis,
it belongs in the threat model and in entropy — not in the classifier.

---

## 1.4 Where the three fields actually touch

The intersections that are *load-bearing* rather than decorative:

1. **LLMs applied to the PQC migration problem** (H8, H9) — the migration
   bottleneck is code comprehension at scale, which is what LLMs are for.
2. **ML applied against PQC implementations** (H12) — deep-learning side-channel
   analysis is now the state of the art in attacking lattice implementations.
3. **PQC applied to protect AI systems** (H5, H3, H13) — model provenance, agent
   delegation, and long-lived AI data are cryptographic problems with
   AI-specific constraints (artifact size, latency budget, message rate).
4. **HNDL applied to AI data** (H13 + H6) — embeddings, RAG corpora, and prompt
   traffic have long confidentiality lifetimes and are recoverable via inversion
   attacks once decrypted.

Everything in `02-open-problems.md` sits in one of those four.

---

## Sources

- NIST PQC standards and timelines: <https://csrc.nist.gov/projects/post-quantum-cryptography>
- PQC migration timelines (2026): <https://thequantuminsider.com/2026/08/07/post-quantum-cryptography-timelines/>
- CSA enterprise PQC migration research: <https://labs.cloudsecurityalliance.org/research/strategic-post-quantum-cryptography-migration-enterprise-roa/>
- Survey of PQC support in cryptographic libraries: <https://arxiv.org/pdf/2508.16078>
- Agentic AI security — threats, defenses, open challenges: <https://arxiv.org/pdf/2510.23883>
- Design patterns for securing LLM agents against prompt injection: <https://arxiv.org/pdf/2506.08837>
- Layered attack-surface survey for LLM agents: <https://arxiv.org/pdf/2604.23338>
- QML for cybersecurity — taxonomy and future directions: <https://arxiv.org/pdf/2512.15286>
- Barren plateaus, unified theory: <https://www.pnnl.gov/publications/unified-mathematical-theory-barren-plateaus>
- ML and side-channel attacks on PQC: <https://eprint.iacr.org/2025/1754.pdf>
- Side-channel and fault attacks on ML-KEM and ML-DSA (Dubrova): <https://proact-school.cs.ru.nl/assets/uploads/slides/PROACT2025.pdf>
- AI supply chain security with MBOM-PQC provenance: <https://www.mdpi.com/2079-8954/14/5/593>
