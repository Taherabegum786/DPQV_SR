# DPQV_SR — PhD Research Program

**Post-Quantum Security for Machine-Learning Systems**

Planning repository for doctoral research at the intersection of LLM/AI security,
post-quantum cryptography, and the quantum threat model.

## Operating constraints

- **Compute:** one classical workstation, optionally one consumer GPU, cloud API
  credits. **No quantum hardware. No side-channel lab equipment.**
- **Publication target:** IEEE / ACM **Transactions** only.

Every problem in this repository is executable under those constraints and maps
to a specific Transactions venue.

## Thesis claim

> Machine-learning systems are a distinct and worst-case class of cryptographic
> migration target. They combine long-lived confidential data held in invertible
> representations, large unauthenticated binary artifacts with derivative
> lineage, machine-speed autonomous delegation, and hard inference-time latency
> budgets. Post-quantum migration methodology — built for TLS, PKI, and firmware
> — does not address this class. This work characterizes the gap, quantifies the
> exposure, and provides mechanisms that close it.

Quantum computing enters as a **threat model**, and as **classical resource
estimation about quantum algorithms**. It is deliberately not used as a
machine-learning substrate — reasoning in `docs/02-open-problems.md` (T10 and the
removals table) and a prepared committee answer in `docs/03-thesis-architecture.md` §3.6.

PQC is classical cryptography designed against a quantum adversary. The entire
field runs on ordinary machines.

## Contents

| Document | Purpose |
|---|---|
| [`docs/00-proposal-index.md`](docs/00-proposal-index.md) | Every proposal at a glance: committed spine, reserve, and deliberate exclusions |
| [`docs/01-landscape-and-hurdles.md`](docs/01-landscape-and-hurdles.md) | What industry cannot currently do (H1-H13), and the three distinct senses of "quantum" |
| [`docs/02-open-problems.md`](docs/02-open-problems.md) | Ten ranked problems with claim, method, required evidence, hardware cost, Transactions venue, and risk |
| [`docs/03-thesis-architecture.md`](docs/03-thesis-architecture.md) | Unifying claim, four-paper sequence, time budget, failure modes |
| [`docs/04-venues-and-rigor.md`](docs/04-venues-and-rigor.md) | Transactions targets per problem, what the constraint costs, rejection reasons, rigor checklist, ethics |
| [`docs/06-novelty-assessment.md`](docs/06-novelty-assessment.md) | **Read first.** Prior-art register, the corrections it forced, and the per-problem novelty verification protocol |
| [`docs/05-first-90-days.md`](docs/05-first-90-days.md) | Reading plan, workstation-only tooling, public trace datasets, two reproductions, one novel measurement |

> **Novelty status:** the proposals below are *candidate framings, not verified
> novel contributions.* A targeted prior-art check found substantial existing
> work on all four proposals examined, and removed one outright. Read
> [`docs/06-novelty-assessment.md`](docs/06-novelty-assessment.md) before acting
> on any of them.

## Shortlist

| Rank | Problem | Hardware | Transactions target |
|---|---|---|---|
| 1 | Harvest-now-decrypt-later against RAG and embedding stores | 1 GPU | IEEE TIFS |
| 2 | Toolchain-introduced timing leakage in the PQC stack, with LLM-assisted repair | None | IEEE TSE / TDSC |
| 3 | Benchmark for cryptographic discovery and PQC migration correctness | None | IEEE TSE / ACM TOSEM |
| 4 | Cross-dataset generalization of DL side-channel attacks on ML-KEM / ML-DSA | 1 GPU | IEEE TIFS / TC |
| 5 | Post-quantum provenance and delegation for agentic systems | None | IEEE TDSC |

Full catalog including five lower-ranked problems, the removals, and the one to
avoid: `docs/02-open-problems.md`.

## Status

Planning stage. Next action: the two reproductions in `docs/05-first-90-days.md`,
weeks 2-6. The `-O0` vs `-O2` constant-time pilot is the highest-information
two weeks available — it decides whether problem T4 exists.
