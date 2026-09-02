# 4. Transactions Venues and What Their Reviewers Demand

**Constraint: IEEE/ACM Transactions only.** This section is scoped accordingly —
non-Transactions venues that would otherwise be natural homes for this work are
listed in §4.2 so you know what you are giving up.

## 4.1 Target Transactions, mapped to problems

### Primary
| Venue | Publisher | Fit | Problems |
|---|---|---|---|
| **IEEE Trans. Information Forensics & Security (TIFS)** | IEEE | The flagship security Transaction. Receptive to measurement and attack papers. | T1, T3, T7, T8 |
| **IEEE Trans. Dependable & Secure Computing (TDSC)** | IEEE | Systems security, protocols, design-and-prove work. | T4, T5, T6, T9 |
| **ACM Trans. Privacy & Security (TOPS)** | ACM | Rigorous, formal-friendly, slower. | T5, T9 |
| **IEEE Trans. Software Engineering (TSE)** | IEEE | Benchmarks, empirical studies, tooling. | T2, T4 |
| **ACM Trans. Software Engineering & Methodology (TOSEM)** | ACM | As TSE; strong on artifacts. | T2 |

### Secondary
| Venue | Fit | Problems |
|---|---|---|
| IEEE Trans. Computers (TC) | Implementation and architecture-level security | T3 |
| IEEE Trans. Emerging Topics in Computing (TETC) | Cross-cutting, receptive to systematizations | T6, T10, survey |
| IEEE Trans. Cloud Computing (TCC) | Multi-tenant isolation | T7 |
| IEEE Trans. Parallel & Distributed Systems (TPDS) | Serving-system measurement | T7 |
| IEEE Trans. Mobile Computing (TMC) | On-device / federated | T8 |
| IEEE Trans. Services Computing (TSC) | Agent/service protocols | T5 |
| IEEE Trans. Quantum Engineering (TQE) | **Fit uncertain** — stated scope emphasizes quantum information and quantum cryptography, not classical PQC. Email the editors with a paragraph abstract before investing. | T10 |

### Strategy
One strong TIFS or TDSC paper outweighs four mid-tier ones for everything except
a literal publication count. If your regulations demand a count, satisfy it with
the systematization plus one applied paper, and spend your real effort on two top
Transactions.

**Verify current JCR/Scopus quartiles yourself before submitting** — they shift
annually and your committee will check.

---

## 4.2 What the Transactions-only constraint costs you

Be aware of these so the decision is deliberate:

- **IACR TCHES** — the top venue in the world for side-channel and implementation
  security. Journal-style with rolling submissions, but *not* an IEEE/ACM
  Transaction and not JCR-indexed. T3 and T4 would land best there. **Workaround:
  publish an extended version in IEEE TIFS or TC**, which is standard practice and
  accepted by both communities.
- **IEEE S&P / USENIX Security / ACM CCS / NDSS** — internationally these outrank
  most journals, and turnaround is faster. Many Indian programs do not credit
  conferences toward the publication requirement. **Check your regulations
  explicitly**, because if conferences count even partially, they are the faster
  path to visibility.
- **PoPETs, Computers & Security, Journal of Information Security & Applications**
  — fast and receptive to exactly your kind of measurement work. Excluded here.
- **IACR ePrint** is not a venue but you should post there anyway for anything
  crypto-flavored. It is where the PQC community actually reads, it costs nothing,
  and it establishes priority against scoop risk.

**Practical recommendation:** post every paper to arXiv and ePrint at submission
time. It protects priority during the long Transactions review cycle, which is
your single biggest structural risk.

---

## 4.3 The rejection reasons to design against

1. **No adaptive attacker.** You evaluated a defense against fixed published
   attacks. Required: an attacker who knows your defense and optimizes against it.
   State the attacker's knowledge and budget.
2. **Missing or weak baseline.** Fatal in ML-flavored security work. A properly
   tuned classical baseline must appear, and sometimes must *win* on some axis for
   your paper to be believable.
3. **Single seed, no variance.** Mean ± CI over ≥5 seeds. For T3, over multiple
   key setups *and* multiple datasets.
4. **Accuracy instead of the field's metric.** For side-channel work report
   **guessing entropy and traces-to-disclosure**, never classification accuracy.
   This single error marks a paper as an outsider's and draws harsh review.
5. **Threat model written after the experiments.** Write it first, enumerate
   adversary capabilities. If your threat model needs the adversary weak in an
   unnatural way, reviewers will find it.
6. **Unfalsifiable quantum claims.** Any sentence implying a quantum computer
   improves your result without measured evidence is a rejection trigger. Keep
   CRQC timing a *parameter*, never an assumption.
7. **No artifact.** Increasingly expected at TSE/TOSEM/TDSC, and retrofitting is
   expensive. Build for release from day one.
8. **Contamination.** For any LLM evaluation, show test data postdates model
   cutoffs, or is mutated, or is private. Otherwise you measured memorization.
9. **Overclaiming in the abstract.** "We solve X" where you mitigated X in one
   configuration. Punished disproportionately.

---

## 4.4 Pre-submission rigor checklist

```
[ ] Threat model written before experiments; adversary capabilities enumerated
[ ] Adaptive attacker evaluated, not just static corpora
[ ] Tuned baseline included, honestly reported when close
[ ] >= 5 seeds / key setups; mean and CI reported
[ ] Field-correct metrics (guessing entropy for SCA; mutual information for
    leakage; behavioral equivalence for migration; nDCG/recall for retrieval)
[ ] Ablation for every design component; no ablation means cut the component
[ ] Negative and failure cases in the body, not only the appendix
[ ] Costs measured (latency, bytes, throughput) not asserted
[ ] Contamination control documented for any LLM evaluation
[ ] Artifact: code, data, exact versions, seeds, working README, Zenodo DOI
[ ] Every "quantum" sentence classified: threat, infrastructure, or compute?
[ ] Limitations section naming the real weakness, not a decorative one
[ ] Ethics and disclosure section where you touch systems you do not own
```

---

## 4.5 Ethics and disclosure

T1 (probing deployed vector-DB endpoints) and T4 (finding real vulnerabilities in
shipped crypto libraries) both touch systems you do not own.

- **T1:** restrict to *passive* observation of what a normal client negotiates.
  Never attempt access to other tenants' data. Get institutional ethics clearance
  and keep the approval documented — TIFS and TDSC ask.
- **T4:** coordinated disclosure to maintainers (liboqs, OpenSSL, PQClean, binding
  authors) with a defined embargo, customarily 90 days, *before* submission.
  Document it in the paper. It strengthens the submission rather than delaying it,
  and a disclosed-and-fixed CVE is a strong CV line in its own right.
- **T3:** public datasets, no live systems, no ethics issue — but honor each
  dataset's licence and cite it as the authors request.

For measurement papers an ethics section is often what makes the paper
acceptable, not overhead.

---

## 4.6 Visibility without a famous group

- Release artifacts on GitHub with a **Zenodo DOI**. Benchmarks and datasets get
  cited even when the paper is not read.
- **Preprint on arXiv and IACR ePrint at submission time.** Non-negotiable given
  10-16 month Transactions cycles.
- Participate where PQC standards work happens — NIST PQC forum, IETF mailing
  lists. It is unusually open to outsiders and builds name recognition that shows
  up later in review outcomes.
- Publicly reproduce an existing result early. It costs little and buys
  credibility fast.
- Email authors of the datasets and tools you build on. Researchers respond to
  people using their artifacts, and this is how collaborations start when you are
  not at a well-known group.
