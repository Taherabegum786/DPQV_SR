# 3. Thesis Architecture

## 3.1 The framing problem

"LLM security + quantum enhancements + PQC" is three fields. A thesis needs one
*claim*. Without a unifying claim you will produce three unrelated papers and an
examiner will ask, correctly, what the thesis is.

**Recommended unifying claim:**

> Machine-learning systems are a distinct and worst-case class of cryptographic
> migration target. They combine long-lived confidential data in recoverable
> representations, large unauthenticated binary artifacts with derivative
> lineage, machine-speed autonomous delegation, and hard inference-time latency
> budgets. Existing post-quantum migration methodology — designed for TLS, PKI,
> and firmware — does not address this class. This thesis characterizes the gap,
> quantifies the exposure, and provides mechanisms that close it.

Why this framing works:

- It is **falsifiable** and specific, not a topic list.
- Quantum enters as the *threat driver* (defensible) rather than as compute
  (indefensible in 2026).
- It contains natural subproblems that are individually publishable.
- Nobody owns it yet. PQC migration literature is about enterprise IT; AI
  security literature ignores cryptography almost entirely. The intersection is
  genuinely vacant, which is exactly what you want for a thesis.
- It survives contact with reality: even if CRQC timelines slip, the artifact
  provenance, agility, and inversion results stand on their own.

**Alternative framing** if you prefer hardware and want the strongest
technical credibility: *"Implementation security of post-quantum cryptography
under machine-learning adversaries"* — spine = P2 plus two more SCA papers.
Narrower, more crowded, but far more defensible in a viva and with a clearer
methodology. Choose this if you have hardware access and enjoy lab work.

Do not attempt both spines.

---

## 3.2 Paper sequence (primary framing)

Four papers, ordered so that each de-risks the next and none blocks on another.

### Paper 1 (months 4-14) — P1: HNDL exposure of embedding and RAG infrastructure
The entry paper. Cheap, self-contained, cannot fully fail (a low-inversion
result is still a bounding result), and it establishes your thesis premise
empirically. Publishing this first means every later paper can cite your own
motivation instead of borrowing someone else's.

*Target:* IEEE TIFS or Computers & Security.

### Paper 2 (months 10-24) — P3: CryptoMig-Bench
Runs partly in parallel with Paper 1 because it is engineering-heavy but
compute-light. Produces a released artifact that other people will use, which is
the highest-leverage citation move available to a PhD student. Also gives you
something concrete to demo to industry collaborators.

*Target:* IEEE TSE / IEEE TIFS / Empirical Software Engineering.

### Paper 3 (months 18-32) — P4: post-quantum delegation and provenance for agents
The constructive contribution. By now you know the cost profile (Paper 1) and
the migration landscape (Paper 2), so you are designing with data rather than
intuition. Contains the amortization result that makes it real research.

*Target:* IEEE TDSC or ACM TOPS.

### Paper 4 (months 28-40) — one of:
- **P2** (DL-SCA on ML-DSA) if you got hardware and want technical depth; or
- **P5** (agility metrics) if you want a tight, low-risk closer; or
- **P7** (QRNG/DP audit) if your committee insists on a visibly "quantum" chapter.

*Target:* TCHES/TIFS, Computers & Security, or QIP respectively.

Plus one **survey/SoK** (months 6-12) — see §3.4.

---

## 3.3 Time budget, honestly

| Phase | Months | Output |
|---|---|---|
| Orientation, replication, rig setup | 0-4 | Reproduced 2 published results; tooling working |
| Survey/SoK | 4-10 | 1 review paper submitted |
| Paper 1 | 4-14 | Submitted month ~12, accepted ~month 18 |
| Paper 2 | 10-24 | Submitted ~22 |
| Paper 3 | 18-32 | Submitted ~30 |
| Paper 4 | 28-40 | Submitted ~38 |
| Thesis writing | 38-48 | Defense |

Assume **8-14 months** from first submission to acceptance at a Q1 journal,
including one major revision. Assume at least one rejection. Budget for it: if
your plan only works when nothing is rejected, the plan is wrong. Keep two
papers in flight at all times so a rejection costs you queue position, not
calendar time.

---

## 3.4 The survey you should write (and the one you should not)

**Write:** a systematization with a defensible thesis — e.g. *"Cryptographic
assumptions in the machine-learning stack: a systematization of what breaks when
RSA and ECC are disallowed."* Enumerate every place the ML stack depends on
classical public-key crypto (model hub signing, package registries, container
signing, TLS to inference APIs, federated learning key agreement, TEE attestation
chains, licensing/DRM for weights), give each a migration difficulty and a data-
lifetime score, and derive a prioritization. That is a real contribution and it
doubles as your thesis' Chapter 2.

**Do not write:** "A Survey of Quantum Machine Learning for Cybersecurity" or
"A Review of LLM Security Threats." Both exist in quantity, neither will be
cited much, and neither demonstrates research capability. Surveys without a
thesis are the most common way PhD students waste year one.

Note that TEE attestation deserves special attention — attestation chains for
confidential inference (SEV-SNP, TDX, H100/H200 confidential computing) are
rooted in classical ECDSA in hardware that is *not field-upgradeable*. That is a
genuinely alarming, underexamined finding and it may be worth a paper of its own.

---

## 3.5 Guarding against the three failure modes

**Failure mode 1: the hype sandwich.** A paper that uses an LLM, mentions
quantum, and applies PQC, where removing any one component would not change the
result. Reviewers detect this instantly. *Test:* for each component, write one
sentence explaining what breaks without it. If you cannot, cut the component.

**Failure mode 2: the toy evaluation.** Simulated adversary, synthetic dataset,
no baseline, single seed. *Test:* would a practitioner change a deployment
decision based on your numbers? If not, the evaluation is too small.

**Failure mode 3: scope collapse into engineering.** Building a working system
is not a contribution; the *claim you can prove about it* is. *Test:* state your
result as a theorem, a measurement with error bars, or a bound. If you cannot
state it in any of those forms, you have a product, not a paper.

---

## 3.6 What to tell your supervisor and committee

A short pitch you can reuse verbatim:

> The post-quantum migration is a decade-long, government-mandated transition
> that is currently about 5% complete. Simultaneously, machine-learning systems
> have become the fastest-growing class of infrastructure handling long-lived
> confidential data. These two facts have not been studied together. My thesis
> establishes that ML systems are a distinctively hard PQC migration target —
> because embeddings are invertible and their source data stays sensitive for
> decades, because model artifacts and agent actions are unauthenticated at
> machine speed, and because inference latency budgets do not tolerate naive
> post-quantum signatures — and it delivers measured exposure, a migration
> benchmark, and a delegation mechanism that closes the gap.

Note what that pitch does *not* contain: any claim about quantum computers
improving machine learning. Keep it that way.
