# 8. Execution Plan — the actual step-by-step

This supersedes the sequencing in `03-thesis-architecture.md`, which was written
before the prior-art check invalidated the proposal catalog. Everything learned
in this repository is folded in here as guardrails at the step where it applies.

**Read `06-novelty-assessment.md` first if you have not.** This plan assumes you
accept its finding: 10 of 10 generated proposals were occupied, so the method is
no longer "pick a problem and verify it" but "generate friction and let the
problem surface."

---

## The four rules this plan encodes

Everything below is downstream of these. If you remember nothing else:

1. **Ideas are not scarce; validated gaps are.** Any composition obvious enough
   to think up in an afternoon has been done. Stop generating, start reproducing.
2. **A stated limitation in someone's paper beats any idea you generate.**
   Authors tell you exactly what they could not do. That is a pre-validated gap
   with a citation attached.
3. **Every experiment needs a positive control before it runs.** The T1 scan
   would have returned 0% — the hypothesised answer — for three reasons unrelated
   to reality. If your apparatus cannot detect a known-present signal, its
   negative results mean nothing.
4. **"Nobody has done this" is fragile; "X assumed B, B fails in C" is robust.**
   Never build an abstract on the first shape.

---

## Phase 0 — Instrument yourself · Week 0–1

Cheap, boring, and everything later depends on it.

- [ ] **TLS stack.** OpenSSL **3.5+** (3.0.x cannot offer ML-KEM — this already
      cost one measurement). Verify: `openssl s_client -groups X25519MLKEM768 ...`
      must not error. Install `liboqs` + `oqs-provider` as a fallback path.
- [ ] **Identify a validated vantage point.** Run `tools/pq_scan.py --check` from
      every network you have access to — home, campus, phone tether, a cheap VPS.
      Record which pass all three gates. You need at least one, ideally two.
- [ ] **Repo hygiene from commit one.** Every experiment gets a config file, a
      fixed seed, and a `make reproduce` path. Retrofitting costs months and
      TSE/TOSEM/TDSC increasingly require artifacts.
- [ ] **Alerts.** arXiv `cs.CR` + `cs.SE` daily; IACR ePrint RSS; Google Scholar
      alerts on each of the five colliding papers in §8.1. This is how you avoid
      a repeat of the 10/10 result.
- [ ] **Accounts, now not later.** arXiv (**cs.CR requires endorsement for new
      authors — start this early, it can take weeks**), IACR ePrint, Zenodo,
      ORCID.
- [ ] **Create `limitations-ledger.md`** in this repo. Phase 1 fills it.

**Done when:** one network passes all three scan gates, and `--check` output is
committed as evidence.

---

## Phase 1 — Build the limitations ledger · Weeks 1–4

Not "read broadly." A specific extraction task.

**Seed set — the five papers that killed your proposals.** They are the closest
work to your interests, which makes them the highest-value reading in the field:

| Paper | Its own stated limit — your starting material |
|---|---|
| arXiv 2606.07341 (LLM crypto migration) | fails on "larger projects with complex dependencies" |
| CaMeL / [IFC for agents](https://arxiv.org/abs/2505.23643) | 7-point utility gap (77% vs 84%); policies hand-written |
| [CSA HNDL paper](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/ai-infrastructure-post-quantum-harvest-now-decrypt-later-v1-csa-styled.pdf) | position paper — no measurement at all |
| [Breaking Bad](https://arxiv.org/html/2410.13489) | classical libraries; PQC coverage incidental |
| [Kyber DL-SCA portability](https://dl.acm.org/doi/10.1007/978-981-97-9053-1_9) | Kyber only; ML-DSA barely touched |

**Procedure, per paper:**

1. Read it properly — method and evaluation, not just the abstract.
2. Extract **every** sentence from limitations, threats-to-validity, and
   future-work into the ledger. One row each.
3. **Forward citation walk.** Read everything citing it. This is where "someone
   already did your extension" lives, and it is the step most often skipped.
4. For each limitation, record: is it still open? who tried? why is it hard?

**Ledger columns:**
`limitation | source paper | still open? | who tried | why hard | what it'd take | my delta`

**Done when:** ≥40 rows from ≥25 papers, and you can name **ten specific things
published authors say they could not do.**

> **Guardrail.** If you find yourself writing new proposal ideas during this
> phase, stop. That is the failure mode this whole plan exists to prevent.
> Ideas go in a separate scratch file and are not acted on until Phase 3.

---

## Phase 2 — Three reproductions · Weeks 3–12 *(overlaps Phase 1)*

Reproduction is how you generate friction. Most of the colliding work is
2025–2026 preprints with self-reported numbers and no independent replication —
that is your edge as a careful student without a lab.

**Before each: write down what a positive control looks like and what result
would mean your apparatus is broken.** Rule 3. No exceptions.

### R1 — The PQ deployment scan · days
- Run `tools/pq_scan.py --check` from a validated vantage. All three gates PASS.
- Run against `tools/targets.txt`. Then **build a real sampling frame** — a
  census of a public directory beats a hand-picked list, and the frame is a
  reviewable choice.
- Record CDN attribution per host: PQ inherited from Cloudflare is a different
  finding from PQ chosen by the operator.
- **A crack looks like:** heavy variance across vantage points; a large
  can-but-does-not-prefer population; PQ adoption being almost entirely inherited.
- **Done when:** ≥100 hosts, ≥2 vantage points, ≥2 timepoints, preflight blocks archived.

### R2 — Reproduce CaMeL's 77% / 84% · 3–4 weeks
- Rebuild the evaluation on a current agent benchmark.
- **Positive control:** an undefended agent must be *successfully attacked* by
  your attack set. If it isn't, your attacks are too weak to measure a defense.
- Then the interesting move: re-run under an **adaptive** attacker that knows the
  architecture. Published defenses routinely under-evaluate here.
- **A crack looks like:** the utility gap widening materially under adaptation;
  the guarantee holding but policy authoring proving infeasible at scale.
- **Done when:** you reproduce both numbers within a stated tolerance, or can
  show precisely why they do not reproduce.

### R3 — Reproduce arXiv 2606.07341 on a dependency-complex repository · 3–4 weeks
- Their code, **their stated failure case** — the thing they said doesn't work.
- **Positive control:** reproduce their reported success on a simple module first.
  If you can't, the problem is your setup, not their method.
- Characterise the failure: which crypto constructs, which dependency shapes,
  which error classes.
- **A crack looks like:** a clean taxonomy of what breaks and why — that is
  publishable as an extension against a named paper.
- **Done when:** a failure taxonomy with counts, on ≥10 real repositories.

> **Guardrail.** A reproduction that simply confirms the paper is *not* wasted —
> it makes you competent in that subfield and gives you a validated baseline you
> will reuse for years. Confirmation is a legitimate outcome. Record it and move on.

---

## Phase 3 — Decision gate · Weeks 12–14

Stop experimenting. Decide.

- [ ] For each candidate that survived Phases 1–2, write a **two-page memo**:
      threat model · the exact claim · the experiment that would falsify it ·
      resources · the three most likely reasons it fails.
- [ ] Rank by: *does this attach to a named paper's stated limitation?* If no,
      it is not a candidate.
- [ ] **Kill everything but one.** Killing a direction at month 3 is a success;
      at month 20 it is a crisis.

**Decision criteria for your constraints (workstation, no lab, Transactions):**
- Needs no GPU → prefer it, GPU access will bottleneck you eventually.
- Attaches to a stated limitation → strongly prefer.
- Requires a benchmark/artifact you must build → good, that is labor not
  equipment, and labor is your comparative advantage.
- Competes head-on with a resourced lab on their main line → avoid.
- You actively enjoy the work → non-negotiable over four years.

**Done when:** one problem chosen, memo committed, others explicitly killed in writing.

---

## Phase 4 — Novelty verification · Weeks 14–16

Run `06-novelty-assessment.md` §6.4 in full on the *chosen* problem. Budget a
full week. Do not skip because Phase 1 felt thorough.

- [ ] Systematic search: Scholar, Semantic Scholar, **IACR ePrint** (crypto
      appears here a year before journals), arXiv full-text, DBLP author walks
      for the 3–5 most active groups, ACM DL, IEEE Xplore.
- [ ] Forward citation walk from the two closest papers.
- [ ] Fill the delta table: `closest prior work | what it established | its stated
      limits | which limit I break | why that matters`.
- [ ] **Write the related-work paragraph before running any experiment.** Two
      hours. If it is uncomfortable to write, the delta is too small — go back to
      Phase 2. This test would have killed eight of the ten original proposals.

**Hard gate:** if you cannot complete the last two delta-table columns against a
*named* paper, you do not have a contribution. Return to Phase 2.

---

## Phase 5 — Pilot, short paper, preprint · Weeks 16–28

- [ ] Run the smallest experiment that could produce the headline number.
- [ ] **Positive control first** (Rule 3), and state in writing what result would
      indicate a broken apparatus.
- [ ] Write it up short (4–6 pages).
- [ ] **Post to arXiv and IACR ePrint immediately.** Transactions cycles run
      10–16 months; the preprint is your only protection against being scooped
      mid-review, and it costs nothing.
- [ ] Email the authors of the papers you build on. They respond to people using
      their artifacts, and this is how collaborations start without a famous group.

**Done when:** preprint posted, one number you own that did not exist before.

---

## Phase 6 — Full Transactions paper · Months 7–14

Expand the pilot. Apply `04-venues-and-rigor.md` §4.4 in full before submitting:

- [ ] Threat model written **before** experiments; adversary capabilities enumerated
- [ ] Adaptive attacker evaluated, not just static corpora
- [ ] Tuned baseline included, reported honestly when close
- [ ] ≥5 seeds / key setups; mean and CI
- [ ] **Field-correct metrics** — guessing entropy for SCA, mutual information for
      leakage, behavioral equivalence for migration. Reporting accuracy for SCA
      marks the paper as an outsider's and draws harsh review.
- [ ] Ablation for every design component
- [ ] Contamination control for any LLM evaluation
- [ ] Artifact with Zenodo DOI
- [ ] Ethics + coordinated disclosure where you touch systems you don't own
- [ ] **Re-run the full novelty search the week before submitting** — the field
      moved while you worked

**Venue:** IEEE TIFS / TDSC for security framing; IEEE TSE / ACM TOSEM for
benchmark and tooling framing. Note what the Transactions-only constraint costs:
IACR TCHES and top conferences are excluded — mitigate by publishing the extended
version in a Transaction.

---

## Phase 7 — Steady state · Months 12+

- [ ] **Two papers in flight at all times.** With 10–16 month cycles this is the
      single most important scheduling habit. A plan that only works when nothing
      is rejected is not a plan.
- [ ] Weekly one-page written update to your supervisor, even if unread — it
      forces falsifiable statements.
- [ ] Monthly scoop check on your active line. If scooped: become the best
      extender of what landed rather than competing with it.
- [ ] Ledger stays live. Every paper you read contributes limitation rows.
- [ ] Reproductions continue in the background — they are cheap and they are how
      the next problem surfaces.

---

## Timeline at a glance

| Phase | When | Output |
|---|---|---|
| 0 Instrument | Wk 0–1 | Validated vantage point; alerts; accounts |
| 1 Ledger | Wk 1–4 | ≥40 limitations from ≥25 papers |
| 2 Reproductions | Wk 3–12 | 3 reproductions; ≥1 crack |
| 3 Decision gate | Wk 12–14 | One problem chosen; rest killed in writing |
| 4 Novelty check | Wk 14–16 | Delta table; related-work paragraph |
| 5 Pilot + preprint | Wk 16–28 | arXiv/ePrint preprint; one owned number |
| 6 Full paper | Mo 7–14 | Transactions submission |
| 7 Steady state | Mo 12+ | Two in flight, permanently |

---

## Three things that would sink this

1. **Skipping Phase 2 and picking from a list.** That is what produced 10/10
   occupied. The reproductions are the plan.
2. **Running an experiment without a positive control.** The scan would have
   returned a beautiful, false 0%. Assume every apparatus is broken until a
   known-present signal proves otherwise.
3. **Underestimating Transactions review time.** Start Phase 5's preprint early
   and keep two in flight from month 12.

---

## What is settled and needs no re-litigating

- **Quantum-as-compute (QML for security) is excluded**, with reasons: barren
  plateaus, the data-loading bottleneck, dequantization, and a literature of
  small simulated circuits on toy datasets without tuned baselines. Prepared
  committee answer in `03-thesis-architecture.md` §3.6.
- **PQC is classical cryptography** designed against a quantum adversary. No
  quantum hardware is needed for any of this.
- **Quantum enters as threat model only** — and parametrically, never as a Q-day
  prediction. That choice neutralises the commonest reviewer objection.
