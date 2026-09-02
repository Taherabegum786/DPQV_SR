# DPQV_SR — PhD Research Program

**Post-Quantum Security for Machine-Learning Systems**

Planning repository for doctoral research at the intersection of LLM/AI security,
post-quantum cryptography, and quantum computing.

## Thesis claim

> Machine-learning systems are a distinct and worst-case class of cryptographic
> migration target. They combine long-lived confidential data held in invertible
> representations, large unauthenticated binary artifacts with derivative
> lineage, machine-speed autonomous delegation, and hard inference-time latency
> budgets. Post-quantum migration methodology — built for TLS, PKI, and firmware
> — does not address this class. This work characterizes the gap, quantifies the
> exposure, and provides mechanisms that close it.

Quantum computing enters this program as a **threat model** (motivating PQC) and,
optionally, as **certified randomness infrastructure**. It is deliberately *not*
used as a machine-learning substrate — see `docs/02-open-problems.md`, P10, for
the reasoning.

## Contents

| Document | Purpose |
|---|---|
| [`docs/01-landscape-and-hurdles.md`](docs/01-landscape-and-hurdles.md) | What industry cannot currently do, across all three fields (H1-H13) |
| [`docs/02-open-problems.md`](docs/02-open-problems.md) | Ten ranked, Q1-scoped open problems with method, evidence, cost, venue, and risk |
| [`docs/03-thesis-architecture.md`](docs/03-thesis-architecture.md) | Unifying claim, four-paper sequence, time budget, failure modes |
| [`docs/04-venues-and-rigor.md`](docs/04-venues-and-rigor.md) | Q1 venue targets, rejection reasons, rigor checklist, ethics and disclosure |
| [`docs/05-first-90-days.md`](docs/05-first-90-days.md) | Reading plan, tooling, reproductions, and the decision to make by day 90 |

## Shortlist

| Rank | Problem | Tier | Cost | Q1 fit |
|---|---|---|---|---|
| 1 | Harvest-now-decrypt-later against RAG and embedding stores | A | Low | Very high |
| 2 | Deep-learning side-channel analysis of ML-DSA's rejection loop | A | Medium (hardware) | Very high |
| 3 | A benchmark for cryptographic discovery and migration correctness | A | Low | High |
| 4 | Post-quantum provenance and delegation for agentic systems | B | Medium | High |
| 5 | Cryptographic agility as a measurable property of ML systems | B | Low | Medium-high |

Full catalog, including the five lower-ranked problems and the one to avoid, in
`docs/02-open-problems.md`.

## Status

Planning stage. Next action: the reproductions in `docs/05-first-90-days.md`,
weeks 2-6.
