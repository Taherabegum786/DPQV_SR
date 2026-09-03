# DPQV_SR — PhD Research Program

**Post-Quantum Security for Machine-Learning Systems**

Planning repository for doctoral research across LLM/AI security, post-quantum
cryptography, and the quantum threat model.

## Start here

**→ [`docs/08-execution-plan.md`](docs/08-execution-plan.md)** — the step-by-step
process to actually follow, Phase 0 through Phase 7.

**→ [`docs/06-novelty-assessment.md`](docs/06-novelty-assessment.md)** — read this
before trusting any proposal in this repo.

## Status, honestly

A catalog of ten research proposals was generated, then prior-art checked.
**All ten were already occupied.** Four are dead outright (T5, T7, T8, T9), one
is reduced to a background section (T10), and five survive only as narrow deltas
against named papers.

That result was predictable rather than unlucky: compositions obvious enough to
generate in one pass are obvious enough that someone with domain immersion did
them two years ago. Real open problems are open because they are hard or
unglamorous, not unthought-of.

**Consequence:** the method changed from *generate proposals and verify them* to
*reproduce published work and let problems surface from friction*. Every collision
in the register arrived with a **stated limitation** attached — and those
limitations are worth more than the ten proposals were.

An attempt to run the one surviving measurement (the PQ deployment scan)
independently confirmed the point: it could not run here, and the way it failed —
silently returning exactly the hypothesised answer for three unrelated reasons —
became a genuine methodological finding for the study.

## Operating constraints

- One classical workstation, optionally one consumer GPU. **No quantum hardware.
  No side-channel lab.**
- Publication target: **IEEE / ACM Transactions only.**
- PQC is classical cryptography designed against a quantum adversary. None of
  this needs a quantum computer.

## Contents

| Document | Purpose |
|---|---|
| [`docs/08-execution-plan.md`](docs/08-execution-plan.md) | **The plan.** Phases 0–7, with every lesson encoded as a guardrail |
| [`limitations-ledger.md`](limitations-ledger.md) | The live problem source. Phase 1 fills it |
| [`docs/06-novelty-assessment.md`](docs/06-novelty-assessment.md) | Prior-art register (10/10 occupied), and the novelty verification protocol |
| [`docs/07-t1-scan-methodology.md`](docs/07-t1-scan-methodology.md) | The scan instrument, and the vantage-point hazard it exposed |
| [`docs/04-venues-and-rigor.md`](docs/04-venues-and-rigor.md) | Transactions targets, rejection reasons, rigor checklist, ethics |
| [`docs/01-landscape-and-hurdles.md`](docs/01-landscape-and-hurdles.md) | Industry hurdles H1–H13; the three senses of "quantum" |
| [`docs/03-thesis-architecture.md`](docs/03-thesis-architecture.md) | Thesis framing and the committee answer on quantum. *Sequencing superseded by 08* |
| [`docs/02-open-problems.md`](docs/02-open-problems.md) | Original proposal catalog. **Historical** — see 06 for what survived |
| [`docs/00-proposal-index.md`](docs/00-proposal-index.md) | Proposal index with current status flags |
| [`docs/05-first-90-days.md`](docs/05-first-90-days.md) | Tooling and datasets. *Sequencing superseded by 08* |
| [`tools/pq_scan.py`](tools/pq_scan.py) | Gated PQ deployment scanner — refuses to run from an invalid vantage point |

## The four rules

1. **Ideas are not scarce; validated gaps are.** Stop generating, start reproducing.
2. **A stated limitation in someone's paper beats any idea you generate.**
3. **Every experiment needs a positive control before it runs.** If your apparatus
   cannot detect a known-present signal, its negative results mean nothing.
4. **"Nobody has done this" is fragile. "X assumed B, B fails in C" is robust.**

## Next action

Phase 0, `docs/08-execution-plan.md`: install OpenSSL 3.5+, then run
`python3 tools/pq_scan.py --check` from every network you have access to until
one passes all three gates. Commit the passing output as evidence.
