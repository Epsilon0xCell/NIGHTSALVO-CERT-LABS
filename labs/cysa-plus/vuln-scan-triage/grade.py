#!/usr/bin/env python3
"""Grader for the scan triage lab. It does not hold a hidden answer
key: it reapplies the prioritization rule published in the lab README
to scan_report.csv and asset_context.csv, then compares the result
with the CVE list in top5.txt (one CVE per line, in order)."""
import csv
import sys

FLAG = "SALVO{triage_by_risk_not_by_number}"
CRIT = {"high": 1.0, "medium": 0.5, "low": 0.0}

def ranked():
    ctx = {r["asset"]: r for r in csv.DictReader(open("asset_context.csv"))}
    scored = []
    for r in csv.DictReader(open("scan_report.csv")):
        a = ctx[r["asset"]]
        score = float(r["cvss"])
        if a["internet_facing"] == "yes":
            score += 2.0
        if r["exploit_available"] == "yes":
            score += 2.0
        score += CRIT[a["criticality"]]
        scored.append((r["cve"], float(r["cvss"]), score))
    scored.sort(key=lambda x: (-x[2], -x[1], x[0]))
    return scored

def main():
    top = ranked()
    print("Rule ranking, top 5:")
    for cve, cvss, score in top[:5]:
        print(f"  {cve}  cvss={cvss}  risk score={score:.1f}")
    try:
        mine = [ln.strip() for ln in open("top5.txt") if ln.strip()]
    except FileNotFoundError:
        print("top5.txt not found. Write the five CVEs, one per line, in priority order.")
        return 1
    expected = [cve for cve, _, _ in top[:5]]
    if mine == expected:
        print("Your top 5 matches the rule exactly.")
        print(FLAG)
        return 0
    print("Your list: " + ", ".join(mine))
    print("Expected:  " + ", ".join(expected))
    return 1

if __name__ == "__main__":
    sys.exit(main())
