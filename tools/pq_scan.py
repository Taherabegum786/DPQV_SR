#!/usr/bin/env python3
"""
pq_scan.py — measure post-quantum hybrid key-exchange adoption across
embedding APIs and vector-database endpoints (proposal T1).

WHAT IT MEASURES
  For each target host, two independent probes:

    preference : offer PQ-hybrid AND classical groups, in the order a modern
                 browser would. Records what the server actually SELECTS.
                 This is the deployment-adoption number.

    capability : offer ONLY PQ-hybrid groups. A successful handshake proves the
                 server CAN do PQ; a failure proves it cannot. This separates
                 "supports but prefers classical" from "does not support",
                 which the preference probe alone cannot distinguish.

WHY THE PREFLIGHT GATES EXIST
  This measurement has a silent failure mode that produces exactly the result
  the hypothesis predicts. If the scan runs from behind a TLS-terminating
  middlebox (corporate egress, cloud sandbox, university proxy, some CDNs), or
  with a TLS client too old to offer ML-KEM groups, every host reports
  "classical only" -- not because the servers are classical, but because the
  client never offered PQ or never spoke to the server at all.
  A 0% result would look like confirmation. It would be an artifact.

  So the scan REFUSES TO RUN unless all three gates pass, and it embeds the
  gate evidence in its own output. Never report numbers from this tool without
  the accompanying preflight block.

REQUIREMENTS
  OpenSSL 3.5+ (April 2025) for native ML-KEM hybrid groups, or OpenSSL 3.x
  with oqs-provider configured. Verified by gate 1.

ETHICS
  Passive TLS handshake observation only -- exactly what any client does when
  it opens a connection. No authentication, no requests, no data access, no
  attempt to reach any tenant's content. One handshake per probe per host.
  See docs/04-venues-and-rigor.md section 4.5 before publishing results.

USAGE
  ./pq_scan.py --targets targets.txt --out results
  ./pq_scan.py --check          # run preflight gates only
"""

import argparse, csv, json, re, shutil, socket, subprocess, sys, time
from datetime import datetime, timezone

# Hybrid groups standardised / widely deployed as of 2026.
PQ_GROUPS = ["X25519MLKEM768", "SecP256r1MLKEM768", "X25519Kyber768Draft00"]
CLASSICAL_GROUPS = ["X25519", "P-256", "P-384"]

# Hosts known to negotiate PQ hybrid. If these come back classical, the
# apparatus is broken, not the internet. Positive controls are mandatory.
POSITIVE_CONTROLS = ["cloudflare.com", "www.google.com"]

# Public CAs we expect to sign the controls. An issuer outside this set means
# the connection is being terminated by something in the path.
EXPECTED_ISSUER_HINTS = ["google", "cloudflare", "digicert", "let's encrypt",
                         "lets encrypt", "isrg", "sectigo", "globalsign",
                         "baltimore", "amazon", "ssl.com", "entrust"]

RE_NEG_GROUP = re.compile(r"Negotiated TLS1\.3 group:\s*(\S+)")
RE_TEMP_KEY = re.compile(r"Server Temp Key:\s*([^\n,]+)")
RE_PROTOCOL = re.compile(r"Protocol\s*:\s*(\S+)")
RE_ISSUER = re.compile(r"^issuer=(.*)$", re.M)


def handshake(host, port, groups, timeout=15):
    """One TLS handshake offering exactly `groups`. Returns a result dict."""
    cmd = ["openssl", "s_client", "-connect", f"{host}:{port}",
           "-servername", host, "-groups", ":".join(groups),
           "-tls1_3", "-brief" if False else "-no_ign_eof"]
    try:
        p = subprocess.run(cmd, input=b"", capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except FileNotFoundError:
        return {"ok": False, "error": "openssl-missing"}

    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    if "no protocols available" in out or "handshake failure" in out.lower():
        return {"ok": False, "error": "handshake-failure", "raw": out[:400]}
    if "cannot be set" in out:
        return {"ok": False, "error": "group-unsupported-by-client", "raw": out[:400]}

    g = RE_NEG_GROUP.search(out)
    tk = RE_TEMP_KEY.search(out)
    group = (g.group(1) if g else (tk.group(1).strip() if tk else None))
    if group is None:
        return {"ok": False, "error": "no-handshake", "raw": out[:400]}

    proto = RE_PROTOCOL.search(out)
    iss = RE_ISSUER.search(out)
    return {"ok": True, "group": group,
            "tls": proto.group(1) if proto else None,
            "issuer": iss.group(1).strip() if iss else None}


def is_pq(group):
    if not group:
        return False
    g = group.lower()
    return "mlkem" in g or "kyber" in g or "ml-kem" in g


# ---------------------------------------------------------------- preflight

def gate_client_capability():
    """Gate 1: can this client even OFFER a PQ hybrid group?"""
    if not shutil.which("openssl"):
        return False, "openssl not found"
    ver = subprocess.run(["openssl", "version"], capture_output=True).stdout.decode().strip()
    probe = subprocess.run(
        ["openssl", "s_client", "-groups", PQ_GROUPS[0], "-connect", "127.0.0.1:1"],
        input=b"", capture_output=True, timeout=10)
    blob = (probe.stdout + probe.stderr).decode("utf-8", "replace")
    if "cannot be set" in blob or "invalid argument" in blob:
        return False, (f"{ver} cannot offer {PQ_GROUPS[0]}. Native ML-KEM hybrids "
                       f"need OpenSSL 3.5+ (Apr 2025), or oqs-provider. Every host "
                       f"would falsely report classical-only.")
    return True, ver


def gate_path_integrity():
    """Gate 2: is TLS terminated by something between us and the origin?"""
    findings = []
    for host in POSITIVE_CONTROLS:
        r = handshake(host, 443, CLASSICAL_GROUPS)
        if not r["ok"]:
            findings.append((host, False, f"no handshake: {r.get('error')}"))
            continue
        iss = (r.get("issuer") or "").lower()
        trusted = any(h in iss for h in EXPECTED_ISSUER_HINTS)
        findings.append((host, trusted, r.get("issuer")))
    ok = all(f[1] for f in findings)
    return ok, findings


def gate_positive_control():
    """Gate 3: do hosts known to support PQ actually negotiate it from here?"""
    findings = []
    for host in POSITIVE_CONTROLS:
        r = handshake(host, 443, PQ_GROUPS + CLASSICAL_GROUPS)
        got = r.get("group") if r["ok"] else None
        findings.append((host, is_pq(got), got or r.get("error")))
    ok = any(f[1] for f in findings)
    return ok, findings


def preflight(verbose=True):
    report = {"utc": datetime.now(timezone.utc).isoformat()}
    ok1, d1 = gate_client_capability()
    report["gate1_client_can_offer_pq"] = {"pass": ok1, "detail": d1}
    if verbose:
        print(f"[gate 1] client PQ capability : {'PASS' if ok1 else 'FAIL'}  {d1}")
    if not ok1:
        return False, report

    ok2, d2 = gate_path_integrity()
    report["gate2_path_not_intercepted"] = {"pass": ok2, "detail": d2}
    if verbose:
        print(f"[gate 2] path integrity       : {'PASS' if ok2 else 'FAIL'}")
        for h, t, i in d2:
            print(f"          {h:24} issuer={'OK ' if t else 'FOREIGN '}{i}")
    if not ok2:
        return False, report

    ok3, d3 = gate_positive_control()
    report["gate3_positive_control"] = {"pass": ok3, "detail": d3}
    if verbose:
        print(f"[gate 3] positive control     : {'PASS' if ok3 else 'FAIL'}")
        for h, t, g in d3:
            print(f"          {h:24} negotiated={g} pq={t}")
    return ok3, report


# ------------------------------------------------------------------- scan

def scan(targets, pause=0.4):
    rows = []
    for host in targets:
        host = host.strip()
        if not host or host.startswith("#"):
            continue
        port = 443
        if ":" in host:
            host, port = host.rsplit(":", 1); port = int(port)

        pref = handshake(host, port, PQ_GROUPS + CLASSICAL_GROUPS)
        time.sleep(pause)
        cap = handshake(host, port, PQ_GROUPS)
        time.sleep(pause)

        rows.append({
            "host": host, "port": port,
            "reachable": pref["ok"],
            "selected_group": pref.get("group"),
            "selected_is_pq": is_pq(pref.get("group")),
            "pq_only_handshake_ok": cap["ok"],
            "pq_capable": cap["ok"] or is_pq(pref.get("group")),
            "tls_version": pref.get("tls"),
            "issuer": pref.get("issuer"),
            "error": pref.get("error") or "",
        })
        print(f"  {host:38} sel={rows[-1]['selected_group'] or '-':22} "
              f"pq_sel={rows[-1]['selected_is_pq']!s:5} pq_cap={rows[-1]['pq_capable']!s}")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets"); ap.add_argument("--out", default="results")
    ap.add_argument("--check", action="store_true", help="preflight gates only")
    ap.add_argument("--force", action="store_true",
                    help="run despite failed gates. Results are INVALID; use only "
                         "to debug the harness, never to produce numbers.")
    a = ap.parse_args()

    print("preflight\n" + "-" * 68)
    ok, report = preflight()
    print("-" * 68)

    if a.check:
        print(json.dumps(report, indent=2, default=str)); return 0 if ok else 2

    if not ok and not a.force:
        print("\nABORT: preflight failed. This vantage point cannot produce a valid\n"
              "measurement. Any numbers it emitted would be an artifact of the\n"
              "client or the network path, not of the servers being measured.\n"
              "Move to an unfiltered network with OpenSSL 3.5+ and re-run.")
        return 2
    if not ok:
        print("\n!! --force: preflight FAILED. Output below is INVALID as a measurement.\n")

    if not a.targets:
        print("no --targets given"); return 1
    targets = open(a.targets).read().splitlines()
    print(f"\nscanning {len([t for t in targets if t.strip() and not t.startswith('#')])} hosts\n" + "-" * 68)
    rows = scan(targets)

    with open(f"{a.out}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(f"{a.out}.json", "w") as f:
        json.dump({"preflight": report, "preflight_passed": ok, "results": rows},
                  f, indent=2, default=str)

    reach = [r for r in rows if r["reachable"]]
    pq_sel = [r for r in reach if r["selected_is_pq"]]
    pq_cap = [r for r in reach if r["pq_capable"]]
    print("-" * 68)
    print(f"reachable            : {len(reach)}/{len(rows)}")
    if reach:
        print(f"selected PQ hybrid   : {len(pq_sel)}/{len(reach)}  ({100*len(pq_sel)/len(reach):.1f}%)")
        print(f"PQ-capable at all    : {len(pq_cap)}/{len(reach)}  ({100*len(pq_cap)/len(reach):.1f}%)")
    print(f"\nwrote {a.out}.csv and {a.out}.json")
    print("Report the preflight block alongside any number from this scan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
