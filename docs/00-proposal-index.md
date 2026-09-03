# 0. Proposal Index — the portfolio at a glance

> ⚠ **7 of 7 proposals checked came back occupied; T5 and T7 are dead.** A prior-art check found substantial existing work on
> all seven proposals examined so far. Read
> [`06-novelty-assessment.md`](06-novelty-assessment.md) first.

Eleven proposals. Five are committed thesis outputs; four are reserve; two are
excluded on principle. Full detail for each in `02-open-problems.md`; sequencing
in `03-thesis-architecture.md`.

**Constraints all of these satisfy:** one classical workstation (± one consumer
GPU), no quantum hardware, no side-channel lab, IEEE/ACM Transactions venue.

---

## Committed — the thesis spine (5 outputs)

### S — Systematization *(months 5-11)*
**"Cryptographic Assumptions in the Machine-Learning Stack: What Breaks When RSA
and ECC Are Disallowed"**
Enumerate every dependency the ML stack has on classical public-key cryptography
— model hub signing, package registries, container signing, TLS to inference
APIs, federated learning key agreement, TEE attestation chains, weight licensing
— score each on migration difficulty and data lifetime, derive a prioritization.
→ **IEEE TETC** · No hardware · Becomes Chapter 2.

### P1 = T1 — Paper 1 *(months 3-13)*
**"Harvest Now, Decrypt Later: Quantifying the Post-Quantum Exposure of
Retrieval-Augmented Generation Infrastructure"**
Embeddings are invertible; TLS recorded today is decryptable later. Nobody has
composed the two. Measure PQ-hybrid adoption across embedding APIs and vector
DBs, reproduce inversion fidelity, model exposure parametrically over CRQC
arrival, mitigate with hybrid PQ plus representation hardening.
→ **IEEE TIFS** · 1 GPU · Cannot fully fail — a low-inversion result still bounds
the threat.

### P2 = T4 — Paper 2 *(months 6-18)*
**"Constant-Time in Source, Leaky in Binary: Toolchain-Introduced Timing
Violations in Deployed Post-Quantum Cryptography"**
Existing screening targets reference implementations. Test whether compiler
optimization reintroduces violations in shipped builds (liboqs, OpenSSL
providers, language bindings) across an algorithm × compiler × opt-level ×
architecture matrix — then add LLM-assisted localization and repair, with the
verification tools as an automatic oracle.
→ **IEEE TSE / TDSC** · No hardware · Pilot decides it in two weeks.

### P3 = T2 — Paper 3 *(months 14-28)*
**"Finding and Fixing Cryptography at Scale: A Benchmark for LLM-Assisted
Post-Quantum Migration"**
Real repositories, adjudicated ground-truth crypto inventory, differential-
execution correctness oracle, hard-case taxonomy, contamination control. The
ground-truth work is the contribution, not the prompting.
→ **IEEE TSE / ACM TOSEM** · No hardware · Released artifact others will cite.

### P4 — Paper 4, choose at month 20 *(months 22-36)*
One of:
- ~~**T5** — "Post-Quantum Delegation"~~ **REMOVED** — AITH (PQ agent delegation,
  Tamarin-verified) and IBCT (attenuated capability chains over MCP/A2A) cover the
  framing; Merkle amortization is established prior art
- **T3** — *core claim false*: DL-SCA portability is an established subfield and
  is already done on Kyber. Only the ML-DSA rejection loop under domain shift may
  survive · IEEE TIFS / TC · 1 GPU
- **T6** — *metric machinery published* (assessment framework, CARS) and the
  proposed intent-based API remedy too. Only the ML-specific application may
  survive; thin · IEEE TDSC / TETC · No hardware

---

## Reserve — publishable, not on the critical path

| ID | Proposal | Hardware | Venue | Why reserve |
|---|---|---|---|---|
| ~~**T7**~~ | ~~Leaking Through the Cache~~ **REMOVED** | — | — | Attacks and defenses both published (PROMPTPEEK, EarlyBird, InputSnatch; SafeKV, PrefixWall) |
| **T8** | Post-Quantum Secure Aggregation for Federated Learning Under Realistic Dropout | Optional ₹15k of Pi/ESP32 boards | IEEE TIFS / TMC | Somewhat crowded; differentiator is real-device measurement vs. simulation |
| **T9** | Containment Instead of Detection: Provable Capability Bounds for Tool-Using LLM Agents | None | IEEE TDSC / ACM TOPS | Highest ceiling, highest competition — enter only with a formal layer |
| **T10** | How Long Is Your Model Safe? Quantum Cryptanalytic Resource Estimation for ML Asset Lifetimes | None (laptop) | IEEE TETC | Strongest as a chapter and a section of P1; standalone only if a committee demands visible quantum content |

---

## Excluded, deliberately

| Proposal | Reason |
|---|---|
| QRNG-backed entropy for differential privacy | Requires quantum randomness infrastructure not available. The classical half — auditing DP-SGD for non-cryptographic PRNG seeding — survives as a foldable contribution to P1. |
| Quantum machine learning for LLM security / intrusion detection | No mechanism, no demonstrated advantage on classical data. Barren plateaus, the data-loading bottleneck, and dequantization results argue against it; the existing literature is small simulated circuits on toy datasets without tuned classical baselines. Excluding it is a defensible scientific judgment — see `03-thesis-architecture.md` §3.6 for the prepared committee answer. |

---

## One-line summary of the whole portfolio

Four of five committed outputs need **no hardware beyond a workstation**; one
needs a single consumer GPU. Every one targets an IEEE or ACM Transaction. The
quantum content is threat modelling and classical resource estimation, never
quantum compute.
