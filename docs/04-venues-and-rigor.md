# 4. Venues and What Q1 Reviewers Actually Demand

## 4.1 Target venues

"Q1" usually means JCR/Scopus first-quartile, which is what most Indian
university PhD regulations and UGC guidance key on. Below, the quartile is
indicative — **verify the current JCR/Scopus quartile yourself before
submitting**, because they shift annually and your committee will check.

### Tier 1 — aim here
| Venue | Type | Fit |
|---|---|---|
| **IEEE Trans. Information Forensics & Security (TIFS)** | Journal, Q1 | Best all-round fit for P1, P2, P3, P6 |
| **IEEE Trans. Dependable & Secure Computing (TDSC)** | Journal, Q1 | Systems security, P4, P9 |
| **ACM Trans. Privacy & Security (TOPS)** | Journal, Q1 | Rigorous, slower |
| **IACR TCHES** | Journal-style, rolling | *The* venue for P2. Not JCR-indexed — pair with a TIFS version |
| **Computers & Security (Elsevier)** | Journal, Q1 | Fast, practical, receptive to measurement papers |
| **IEEE Trans. Software Engineering / TOSEM** | Journal, Q1 | P3 if you frame it as SE |

### Tier 1 conferences (if your program credits them)
IEEE S&P, USENIX Security, ACM CCS, NDSS. In India many programs weight journals
over conferences; internationally these outrank most journals. Know your
regulations, but publish at least one conference paper for visibility.

### Solid, realistic
IEEE Internet of Things Journal (Q1), Future Generation Computer Systems (Q1),
Journal of Systems and Software, Journal of Information Security and
Applications, IEEE Transactions on Emerging Topics in Computing, Empirical
Software Engineering, PoPETs.

### Handle with care
- **IEEE Access** — Q1/Q2 borderline by JCR, but increasingly discounted by
  hiring and evaluation committees. Fine as a fallback, poor as a strategy.
- **MDPI titles** (Sensors, Electronics, Applied Sciences, Systems, Information,
  Entropy) — several are JCR Q1/Q2 and technically satisfy most regulations, but
  reputational weight varies sharply by field and by committee. If your
  university accepts them, one is a reasonable pressure valve; a CV built on them
  will limit postdoc options. Ask your supervisor directly and early.
- Anything soliciting you by email, promising fast review, or charging fees
  without a recognizable editorial board. Check DOAJ, Scopus source list, and
  your institution's approved list.

**Strategy:** one strong TIFS/TDSC paper outweighs four mid-tier ones for
everything except a literal publication count. If your regulations demand a
count, satisfy it with the survey and one applied paper, and spend your real
effort on two top papers.

---

## 4.2 The rejection reasons you must design against

From how reviewing actually goes in this area:

1. **No adaptive attacker.** You evaluated a defense against fixed, published
   attacks. *Required:* an attacker who knows your defense and optimizes against
   it. State the attacker's knowledge and budget explicitly.
2. **Missing or weak baseline.** Especially fatal in ML-flavored security work.
   A properly tuned classical/simple baseline must appear, and sometimes it must
   *win* on some axis for your paper to be believable.
3. **Single seed, no variance.** Report mean ± CI over ≥5 seeds. Side-channel
   work: over multiple key setups and multiple devices.
4. **Threat model stated after the fact.** Write it first. Name the adversary's
   capabilities, knowledge, and goal. If your threat model needs the adversary
   to be weak in an unnatural way, reviewers will find it.
5. **Unfalsifiable quantum claims.** Any sentence implying a quantum computer
   improves your result without measured evidence is a rejection trigger. Keep
   CRQC timing as a *parameter*, never an assumption.
6. **No artifact.** Increasingly, code+data release is expected. Plan for it from
   day one — it is much harder to retrofit.
7. **Contamination.** For LLM evaluations: show your test data postdates model
   cutoffs, or is mutated, or is private. Otherwise your numbers measure
   memorization.
8. **Overclaiming in the abstract.** "We solve X" where you mitigated X in a
   configuration. Reviewers punish this disproportionately.

---

## 4.3 A rigor checklist to apply before every submission

```
[ ] Threat model written before the experiments, adversary capabilities enumerated
[ ] Adaptive attacker evaluated, not just static corpora
[ ] Strong, tuned baseline included (and honestly reported when it is close)
[ ] >= 5 seeds / >= 5 key setups; mean and CI reported
[ ] Ablation for every design component; anything with no ablation gets cut
[ ] Negative and failure cases reported in the paper, not the appendix only
[ ] Costs measured (latency, bytes, throughput, energy) not asserted
[ ] Data-contamination control documented for any LLM evaluation
[ ] Artifact: code, data, exact versions, seeds, and a working README
[ ] Every "quantum" sentence checked: is this Q-as-threat, -compute, or -infra?
[ ] Limitations section that names the real weakness, not a decorative one
[ ] Ethics/disclosure section if you attack deployed systems (see 4.4)
```

---

## 4.4 Ethics and disclosure

P1 (scanning deployed vector DB endpoints) and P6 (side channels in hosted
serving) touch live systems. Before you run anything against infrastructure you
do not own:

- Restrict to *passive* observation of what a normal client negotiates; do not
  attempt access to other tenants' data.
- Get institutional ethics/IRB clearance, and keep the approval documented — Q1
  security journals ask.
- Follow coordinated disclosure with a defined embargo (90 days is customary) for
  anything you find. Document it in the paper; it strengthens the submission.
- For P2, work only on hardware you own. Never on production devices.

An ethics section is not overhead — for measurement papers it is often what makes
the paper acceptable.

---

## 4.5 Building visibility as an unknown group

- Release artifacts on GitHub with a DOI (Zenodo). Benchmarks get cited even when
  the paper is not read.
- Preprint on arXiv **and** on IACR ePrint for anything crypto-flavored. ePrint is
  where the PQC community actually reads.
- Present at NIST PQC forums / IETF mailing lists where relevant; PQC standards
  work is unusually open to outside input, and being a known name there helps
  reviewing outcomes.
- Reproduce and publicly release a reproduction of an existing result early. It
  costs little and builds credibility fast.
