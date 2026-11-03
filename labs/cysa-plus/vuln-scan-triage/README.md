# Lab: Vulnerability scan triage

- Track: CompTIA CySA+
- Objective mapping: Domain 2, Vulnerability Management: vulnerability
  analysis, prioritization, and risk scoring in context.

## Scenario

`scan_report.csv` is this week's vulnerability scan: twelve findings.
`asset_context.csv` says what the scanner cannot know: which assets
face the internet and how much each one matters. The patch window
fits five fixes. Pick the right five, in the right order.

Raw CVSS order is the obvious answer and the wrong one. The team's
published prioritization rule is:

```
risk score = CVSS
           + 2.0 if the asset is internet-facing
           + 2.0 if a known exploit is available
           + 1.0 if asset criticality is high (0.5 if medium)
```

Rank by risk score, highest first. Break ties by higher CVSS, then
by CVE ID in ascending order.

## Setup

Nothing to build. The grader reapplies the published rule to the
shipped CSVs and compares its top five with yours, so the ground
truth cannot drift from the rule.

## Tasks

1. Compute the risk score for all twelve findings.
2. Write the top five CVE IDs to `top5.txt`, one per line, in
   priority order.
3. Be able to explain, in one sentence each, why the highest raw
   CVSS finding did or did not make the cut.

## Answer format

`top5.txt` in this folder, then run `python3 grade.py`.

## Hint ladder

1. The scanner's sort order is a trap. Re-sort by the rule, not by
   the number in the CVSS column.
2. Work the trap case by hand: a 10.0 on an internal workstation
   with no exploit scores exactly 10.0 under the rule. Compare that
   with a 7.5 on an internet-facing, high-criticality asset with an
   exploit.
3. The CySA+ vulnerability management materials cover contextual
   scoring: exposure and exploitability move real priority more
   than base severity does.
