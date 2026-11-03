# Writeup: Vulnerability scan triage

Twelve findings, five slots, and one column begging to be sorted.
My first pass made the mistake this lab exists to catch, so I will
record it plainly: I sorted by CVSS, took the top five, and had
CVE-2026-1005, the 10.0, at the head of the list.

## Why the 10.0 is a trap

CVE-2026-1005 sits on ws-114: not internet-facing, low criticality,
no known exploit. Under the published rule it scores its raw 10.0
and nothing more. Now compare the shape of CVE-2026-1004: a 7.5 on
web-01, internet-facing, high criticality, exploit available. That
is 7.5 + 2.0 + 2.0 + 1.0 = 12.5. The 7.5 outranks the 10.0 by two
and a half points, because the 7.5 is reachable by everyone on
earth and the 10.0 is reachable by whoever already owns the office.

## Applying the rule to all twelve

I computed every score rather than sampling, since triage errors
live in the middle of the table:

| CVE | CVSS | Asset | Score |
| --- | --- | --- | --- |
| CVE-2026-1001 | 9.8 | vpn-01 (internet, high, exploit) | 14.8 |
| CVE-2026-1002 | 9.1 | web-01 (internet, high, exploit) | 14.1 |
| CVE-2026-1006 | 8.1 | mail-01 (internet, medium, exploit) | 12.6 |
| CVE-2026-1004 | 7.5 | web-01 (internet, high, exploit) | 12.5 |
| CVE-2026-1003 | 8.8 | db-01 (internal, high, exploit) | 11.8 |
| CVE-2026-1005 | 10.0 | ws-114 (internal, low, no exploit) | 10.0 |
| CVE-2026-1010 | 9.4 | app-02 (internal, medium, no exploit) | 9.9 |
| CVE-2026-1008 | 6.5 | web-01 (internet, high, no exploit) | 9.5 |
| CVE-2026-1011 | 4.3 | mail-01 (internet, medium, exploit) | 8.8 |
| CVE-2026-1009 | 5.4 | db-01 (internal, high, exploit) | 8.4 |
| CVE-2026-1007 | 7.0 | app-02 (internal, medium, no exploit) | 7.5 |
| CVE-2026-1012 | 3.7 | vpn-01 (internet, high, no exploit) | 6.7 |

The cut falls after CVE-2026-1003 at 11.8, and the 10.0 watches from
sixth place. Note the second quiet lesson in the table: CVE-2026-1003
makes the cut from inside the network because an available exploit
on a high-criticality database is still a fire, just a smaller one
than the internet-facing set.

## Grading

`top5.txt`:

```
CVE-2026-1001
CVE-2026-1002
CVE-2026-1006
CVE-2026-1004
CVE-2026-1003
```

```
$ python3 grade.py
Rule ranking, top 5:
  CVE-2026-1001  cvss=9.8  risk score=14.8
  CVE-2026-1002  cvss=9.1  risk score=14.1
  CVE-2026-1006  cvss=8.1  risk score=12.6
  CVE-2026-1004  cvss=7.5  risk score=12.5
  CVE-2026-1003  cvss=8.8  risk score=11.8
Your top 5 matches the rule exactly.
SALVO{triage_by_risk_not_by_number}
```

Flag: `SALVO{triage_by_risk_not_by_number}`

The grader here recomputes the ranking from the CSVs rather than
comparing against a stored key, which is the honest way to grade a
rule-based lab: if the data changes, the truth changes with it.
And the habit the lab drills is the one that matters on the job: a
severity score describes a vulnerability, but priority describes a
vulnerability in a place, and the place is half the answer.
