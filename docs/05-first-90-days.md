# 5. First 90 Days: Concrete Plan

The goal of the first 90 days is not a paper. It is to (a) eliminate one
research direction, (b) reproduce two existing results so your tooling is
trusted, and (c) produce one measurement nobody has published.

---

## Weeks 1-3 — Read to a decision, not to completeness

Read with a specific question: *which of P1, P2, P3 am I actually going to do?*

**Standards and policy (read the actual documents, not summaries)**
- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA)
- NIST IR 8547 (transition to PQC standards) and NIST/NCCoE migration project
- NSA CNSA 2.0; BSI/ANSSI hybrid guidance — read both, note where they disagree
- OWASP Top 10 for LLM Applications; NIST AI 100-2 (adversarial ML taxonomy)
- EU AI Act security-relevant articles, if you want the compliance angle

**Foundational technical**
- Embedding inversion: Song & Raghunathan (information leakage in embeddings);
  the vec2text line of work on near-verbatim text recovery from embeddings
- Prompt injection: the design-patterns paper (arXiv 2506.08837) and the agentic
  security survey (arXiv 2510.23883)
- SCA on PQC: the ML-and-side-channels survey (ePrint 2025/1754), Dubrova's
  ML-KEM/ML-DSA attack line, and the non-profiled DL-SCA work
- QML skepticism: barren plateau theory, dequantization results, and the QML-for-
  cybersecurity taxonomy (arXiv 2512.15286) — read these so you can defend the
  decision *not* to do QML

**How to read:** maintain a single table with columns
`paper | claim | evidence | what it does NOT show | what I would do next`.
The fourth column is where your problems come from. Aim for 60-80 rows by week 6.

---

## Weeks 2-6 — Get tooling working and reproduce two results

Reproduction is the fastest way to find out whether you can actually do the work.

**Software stack**
```
liboqs + oqs-provider          # PQ primitives, OpenSSL 3.x integration
pqm4                           # ARM Cortex-M4 PQC implementations + benchmarks
ChipWhisperer                  # trace capture (if doing P2)
sigstore / model-signing       # model artifact signing
CodeQL, Semgrep                # crypto discovery ground truth (P3)
AgentDojo, InjecAgent          # agent security benchmarks (P4/P9)
BEIR / MTEB subsets            # retrieval quality (P1)
vLLM or SGLang                 # serving stack (P6)
```

**Reproduction 1 (everyone does this):** stand up a hybrid PQ TLS connection with
oqs-provider (X25519MLKEM768), and measure handshake size and latency versus
classical on a constrained link. Trivial, but it makes the size problem concrete
and gives you numbers you will reuse in three papers.

**Reproduction 2 (choose by direction):**
- If P1: reproduce embedding inversion on one open embedding model. Target
  measurable recovery on a held-out corpus.
- If P2: reproduce a published CPA or DL attack on unprotected Kyber/ML-KEM in
  pqm4. If your rig cannot recover a key from a *known-broken* target, your rig
  is wrong — find out now, not in month 14.
- If P3: run 2-3 LLMs over 10 real repositories and hand-audit the crypto
  inventory. Measure how bad discovery recall actually is. This single number
  tells you whether P3 is a paper.

---

## Weeks 6-10 — Kill one direction, commit to one

Write a two-page internal memo for each of your top two candidates containing:
threat model, the exact claim, the experiment that would falsify it, resource
requirements, and the three most likely reasons it fails. Then kill one. Killing
a direction in month 2 is a success; killing it in month 20 is a crisis.

**Decision heuristics:**
- Do you have (or can you get) SCA hardware within 8 weeks? If no → not P2.
- Do you have >= 1 dedicated GPU? If no → P3 and P5 over P1's inversion work.
- Does your supervisor have industry contacts for real deployment data? If yes →
  P1 or P5 gain enormously.
- Do you enjoy lab measurement or software systems? Answer honestly; a 4-year
  project you dislike will fail regardless of its merit.

---

## Weeks 8-12 — Produce one novel measurement

By day 90 you should own one number that did not exist before. Candidates,
each achievable in ~4 weeks once tooling works:

- **For P1:** the fraction of N reachable embedding/vector-DB endpoints that
  negotiate a PQ-hybrid key exchange. (Almost certainly near zero — which is
  exactly the point, and it is a *fact* you established.)
- **For P3:** discovery recall of frontier LLMs on hand-audited real repositories,
  broken down by hard-case category.
- **For P2:** a TVLA leakage map across ML-DSA signing phases on your board,
  including the rejection loop.
- **For P5:** the count of stored-artifact formats in the top ML platforms that
  hard-encode an algorithm identifier.

Write it up as a 4-page workshop/short paper immediately. It gets you a
timestamp, feedback, and a citation, and it becomes Section 3 of the eventual
journal paper.

---

## Ongoing hygiene from day 1

- **One repository, versioned, with an artifact mindset.** Every experiment gets
  a seed, a config file, and a `make reproduce` path. Retrofitting this later
  costs months.
- **A running related-work file**, updated weekly. Set arXiv alerts for `cs.CR`
  with keyword filters (`post-quantum`, `ML-KEM`, `ML-DSA`, `prompt injection`,
  `agent security`, `side-channel`) and an ePrint feed.
- **Weekly 1-page written update** to your supervisor, even if unread. It forces
  you to state results in falsifiable terms.
- **Track scoop risk explicitly.** For P3 especially, check monthly whether
  someone published your benchmark. If they did: pivot to being the best user and
  extender of it rather than competing.

---

## The three things most likely to sink this PhD

1. **Spending year one on a survey with no thesis.** Covered in §3.4.
2. **Being talked into QML because it sounds impressive.** Covered in P10. If a
   committee member pushes for it, offer P7 (QRNG for DP) as the quantum chapter —
   it is honest, cheap, and defensible.
3. **Doing all three fields shallowly.** The framing in §3.1 exists precisely to
   let you go deep in one place while legitimately claiming all three.
