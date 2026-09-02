# 3. Thesis Architecture

**Operating constraints:** one classical workstation (+ one GPU where noted), no
quantum hardware, no side-channel lab. Publication target: IEEE/ACM Transactions.

## 3.1 The unifying claim

Three fields do not make a thesis. One claim does.

> Machine-learning systems are a distinct and worst-case class of cryptographic
> migration target. They combine long-lived confidential data held in *invertible*
> representations, large unauthenticated binary artifacts with derivative lineage,
> machine-speed autonomous delegation, and hard inference-time latency budgets.
> Post-quantum migration methodology — built for TLS, PKI, and firmware — does not
> address this class. This thesis characterizes the gap, quantifies the exposure,
> and provides mechanisms that close it.

Why it holds up:

- **Falsifiable and specific**, not a topic list.
- **Quantum enters as threat model**, never as compute. Nothing in the thesis
  requires a quantum computer to exist, only to be *possible* — and the exposure
  analysis is parametric over that assumption, so the thesis survives any Q-day
  slippage.
- **The intersection is vacant.** PQC migration literature addresses enterprise
  IT; AI security literature ignores cryptography almost entirely.
- **Every chapter runs on a workstation.**

**Alternative spine** if you find you prefer implementation security to systems
work: *"Implementation security of post-quantum cryptography under machine-
learning adversaries"* — T3 + T4 + a third SCA paper. Narrower, more crowded,
easier to defend in a viva because the methodology is unambiguous. Also entirely
hardware-free under the public-dataset approach.

Pick one spine by month 6. Do not attempt both.

---

## 3.2 Paper sequence

Four Transactions papers plus one systematization. Ordered so each de-risks the
next and none blocks on another.

### Paper 1 (months 3-13) — T1: HNDL exposure of embedding and RAG infrastructure
→ **IEEE TIFS**

Entry paper. Cheap, self-contained, cannot fully fail, and it establishes your
thesis premise empirically so every later paper cites your own motivation. The
network measurement should run in month 3-4 — it is the component that ages.

### Paper 2 (months 6-18) — T4: toolchain-introduced timing leakage in the PQC stack
→ **IEEE TSE** or **IEEE TDSC**

Runs in parallel with Paper 1 because it is CPU-bound and needs no GPU
contention. Zero hardware. Contains your first LLM contribution with an
*automatic* correctness oracle, which is a genuinely strong methodological
position. Run the two-week pilot early (see `05-first-90-days.md`) to confirm the
toolchain-introduced violation class is real before committing.

### Paper 3 (months 14-28) — T2: cryptographic discovery and migration benchmark
→ **IEEE TSE** or **ACM TOSEM**

Produces a released artifact others will use — the highest-leverage citation move
available to a student without a famous advisor. Also the paper you show industry
collaborators. Deliberately placed after Paper 2 so the constant-time work feeds
its correctness oracle.

### Paper 4 (months 22-36) — choose one:
- **T5** (PQ delegation for agents) → IEEE TDSC — if you want the constructive,
  design-and-prove chapter.
- **T3** (cross-dataset DL-SCA generalization) → IEEE TIFS — if you want technical
  depth and enjoy empirical ML work.
- **T6** (agility metrics) → IEEE TDSC / TETC — the low-risk closer.

Decide at month 20 based on which of Papers 1-3 went smoothest.

### Systematization (months 5-11) — the survey you *should* write
→ **IEEE TETC** or a Transactions survey track

*"Cryptographic assumptions in the machine-learning stack: what breaks when RSA
and ECC are disallowed."* Enumerate every dependency on classical public-key
crypto — model hub signing, package registries, container signing, TLS to
inference APIs, federated learning key agreement, TEE attestation chains, weight
licensing — and score each on migration difficulty and data lifetime, then derive
a prioritization. That is a real contribution and it becomes Chapter 2 of the
thesis.

**Do not** write "A Survey of Quantum Machine Learning for Cybersecurity" or "A
Review of LLM Security Threats." Both exist in quantity, neither gets cited, and
neither demonstrates research capability. Surveys without a thesis are the most
common way year one is wasted.

---

## 3.3 Time budget

| Phase | Months | Output |
|---|---|---|
| Orientation, reproductions, tooling | 0-3 | 2 reproduced results; stack working |
| Novel measurement (T1 network scan) | 3-4 | One number nobody has published |
| Paper 1 (T1) | 3-13 | Submitted ~m11 |
| Paper 2 (T4) | 6-18 | Submitted ~m16 |
| Systematization | 5-11 | Submitted ~m11 |
| Paper 3 (T2) | 14-28 | Submitted ~m26 |
| Paper 4 | 22-36 | Submitted ~m34 |
| Thesis writing + defense | 36-48 | — |

**Transactions timelines are slow.** Budget 10-16 months from submission to
acceptance including one major revision — IEEE TIFS and TDSC routinely run
6-10 months to first decision. Assume at least one rejection. **Keep two papers
in flight at all times** so a rejection costs queue position, not calendar time.
A plan that only works when nothing is rejected is not a plan.

This is the main practical cost of the Transactions-only constraint, and you
should plan around it explicitly rather than discovering it in year three.

---

## 3.4 Guarding against three failure modes

**The hype sandwich.** A paper using an LLM, mentioning quantum, and applying PQC,
where removing any component would not change the result. Reviewers detect this
instantly. *Test:* for each component, write one sentence saying what breaks
without it. If you cannot, cut it.

**The toy evaluation.** Simulated adversary, synthetic data, no baseline, single
seed. *Test:* would a practitioner change a deployment decision based on your
numbers? If not, the evaluation is too small.

**Scope collapse into engineering.** A working system is not a contribution; the
claim you can prove about it is. *Test:* state your result as a theorem, a
measurement with error bars, or a bound. If it fits none of those forms, you have
a product, not a paper.

---

## 3.5 The pitch, for your supervisor and committee

> The post-quantum migration is a decade-long, government-mandated transition
> that is roughly 5% complete against a 2030 deprecation and 2035 disallowance
> deadline. Simultaneously, machine-learning systems have become the
> fastest-growing class of infrastructure handling long-lived confidential data.
> These two facts have not been studied together. My thesis establishes that ML
> systems are a distinctively hard PQC migration target — because embeddings are
> invertible and their source data stays sensitive for decades, because model
> artifacts and agent actions are unauthenticated at machine speed, and because
> inference latency budgets do not tolerate naive post-quantum signatures — and
> it delivers measured exposure, a migration benchmark, and a delegation
> mechanism that closes the gap. All of it is executable on standard hardware;
> none of it requires quantum infrastructure.

That last sentence matters when a committee asks how you can do quantum research
without a quantum computer. The answer is that PQC is *classical* cryptography
designed against a quantum adversary — the entire field runs on ordinary
machines.

---

## 3.6 Handling the "where is the quantum?" question

You will be asked. Prepare this answer:

1. **Quantum-as-threat** is what standardized PQC exists for; FIPS 203/204/205
   are classical algorithms. This is the thesis' foundation and requires no
   quantum hardware.
2. **Quantum cryptanalytic resource estimation** (T10) is classical computation
   *about* quantum algorithms — it runs on a laptop and produces the migration
   deadlines that drive Chapter 3.
3. **Quantum-as-compute** (QML for security) is excluded deliberately and with
   reasons: barren plateaus, the data-loading bottleneck, dequantization results,
   and a literature dominated by small simulated circuits on toy datasets without
   tuned classical baselines. Excluding it is a defensible scientific judgment,
   and saying so demonstrates more maturity than including it would.

If a committee member insists on visible quantum content, T10 as a full chapter
is the concession to make. It is honest, cheap, and requires nothing you lack.
