# 7. T1 Deployment Scan — instrument, and why it did not run here

## 7.1 Attempted, aborted

The scan was attempted from this session's container on 2026-09-03. It cannot
produce a valid measurement from this vantage point. **Three independent gates
failed**, any one of which is disqualifying.

### Gate 1 — the client cannot offer PQ at all

```
OpenSSL 3.0.13 (30 Jan 2024)
$ openssl s_client -groups X25519MLKEM768 -connect cloudflare.com:443
error:0A080106:SSL routines:gid_cb:passed invalid argument:
  group 'X25519MLKEM768' cannot be set
```

Native ML-KEM hybrid groups arrived in **OpenSSL 3.5 (April 2025)**. A 3.0.x
client cannot put the group in its ClientHello, so no server can ever select it.
Python's `ssl` module fails identically (`unknown elliptic curve name`), because
it links the same library.

### Gate 2 — TLS is terminated before it reaches the origin

```
$ openssl s_client -connect cloudflare.com:443     # no proxy env, direct TCP
issuer = O = Anthropic, CN = Egress Gateway SDS Issuing CA (production)
Server Temp Key: X25519, 253 bits
```

The certificate is issued by the sandbox's egress gateway, not by Cloudflare's
CA. Same for `www.google.com`. The TCP connection succeeds and the handshake
completes — **but the peer is the gateway.** `Server Temp Key: X25519` is the
gateway's choice; the origin's preference is unobservable. Explicit-proxy
`CONNECT` to arbitrary hosts is separately refused with 403.

### Gate 3 — positive controls do not negotiate PQ

Cloudflare and Google both deploy `X25519MLKEM768` in production. From here,
neither negotiates it. When hosts *known* to support the thing you are measuring
report that they do not, the apparatus is broken, not the internet.

## 7.2 Why this matters more than a failed run

**The failure mode produces exactly the result the hypothesis predicts.**

T1's expected finding is "almost no embedding or vector-DB endpoint negotiates
PQ hybrid key exchange." Run naively from this container — or from any corporate
network, university proxy, cloud egress, or inspecting middlebox — the scan
returns **0% PQ adoption across every host**. That number would look like clean,
strong confirmation. It would be an artifact of the measurement apparatus, and
nothing about the output would reveal it.

This is a genuine methodological hazard for the study, not an artefact of one
sandbox:

- TLS-inspecting middleboxes are common on exactly the networks a student is
  likely to scan from (campus, corporate VPN, cloud VM with egress filtering).
- The default TLS client on most current Linux distributions is still OpenSSL
  3.0.x, which silently cannot offer ML-KEM.
- Neither condition raises an error. Both quietly yield the expected answer.

**Consequence for the paper:** vantage-point validation is not hygiene, it is a
reportable part of the method. The paper must state where the scan ran, what TLS
client version, and the positive-control results — and reviewers should ask for
them. This belongs in the methodology section, and it is a small independent
contribution: prior deployment scans in this space rarely report it.

## 7.3 The instrument

`tools/pq_scan.py` is written, complete, and refuses to run until the gates pass.

**Two probes per host**, which is the design point that makes the number
meaningful:

| Probe | Groups offered | Answers |
|---|---|---|
| `preference` | PQ hybrid **and** classical, browser-realistic order | What the server actually **selects** — the adoption number |
| `capability` | PQ hybrid **only** | Whether the server **can** do PQ at all |

The pair separates *"supports PQ but prefers classical"* from *"cannot do PQ"*.
A single probe conflates them, and the distinction is the interesting part of the
result: a server that can but does not is a configuration story, a server that
cannot is a software-lifecycle story.

**Gates, all mandatory, all embedded in the output JSON:**

1. `gate1_client_can_offer_pq` — client actually offers ML-KEM hybrids
2. `gate2_path_not_intercepted` — control-host issuers match public CAs
3. `gate3_positive_control` — known-PQ hosts do negotiate PQ from this vantage

`--force` exists only for harness debugging and stamps the output as invalid.
The tool prints a reminder that no number should be reported without its
preflight block.

## 7.4 To actually run it

```bash
# needs OpenSSL 3.5+ and an unfiltered network path
openssl version                       # must be >= 3.5
python3 tools/pq_scan.py --check      # all three gates must PASS
python3 tools/pq_scan.py --targets tools/targets.txt --out results
```

If OpenSSL 3.5+ is unavailable, build OpenSSL 3.5 from source, or use
OpenSSL 3.x with `oqs-provider` configured — gate 1 accepts either.

**Before publishing anything from it:**

- **Define the sampling frame.** `tools/targets.txt` is a seed list, not a frame.
  How hosts were chosen is a reviewable methodological decision. Consider a
  census of a public directory rather than hand-picking.
- **Repeat over time and from multiple vantage points.** Adoption is moving;
  a single-day, single-network snapshot is weak. Multiple vantages also
  cross-check gate 2.
- **Record CDN attribution.** Many of these endpoints sit behind Cloudflare or
  similar. If a host negotiates PQ, you may be measuring the CDN's configuration
  rather than the operator's decision. Say so — and it is arguably a finding in
  itself that PQ adoption in this space is inherited rather than chosen.
- **Ethics.** Passive handshake observation only, one connection per probe. See
  `04-venues-and-rigor.md` §4.5 and obtain institutional clearance before a
  large-scale run.

## 7.5 Status

| Item | State |
|---|---|
| Instrument | Written, gated, ready (`tools/pq_scan.py`) |
| Target seed list | Written (`tools/targets.txt`), needs a real sampling frame |
| Measurement | **Not run.** Requires OpenSSL 3.5+ on an unfiltered network |
| Finding so far | The vantage-point hazard itself, documented in §7.2 |
