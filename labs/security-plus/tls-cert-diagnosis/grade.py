#!/usr/bin/env python3
"""Grader for this lab. Reads answers.txt (key=value lines), checks each
value against a stored SHA-256 of the expected answer, and prints the
lab flag when every key matches. Expected answers are hashed so the
ground truth is not sitting in plain text."""
import hashlib
import sys

EXPECTED = {'deploy': 'b9dd960c1753459a78115d3cb845a57d924b6877e805b08bd01086ccdf34433c', 'alpha_reason': 'fa64ea1e82e1206f828ab2a02917c7e92accb98e3b95881a1b4ad52b914b66e3', 'bravo_reason': '64a3513950c6feb234fface75e3a7be5ff880ebef9bd3301e5fdbd61b62d599d'}
FLAG = 'SALVO{tls_triage_deploy_charlie}'

def norm(v):
    return " ".join(v.strip().lower().split())

def main():
    try:
        pairs = {}
        for line in open("answers.txt"):
            if "=" in line:
                k, v = line.split("=", 1)
                pairs[k.strip().lower()] = norm(v)
    except FileNotFoundError:
        print("answers.txt not found. Create it with one key=value per line.")
        return 1
    wrong = []
    for key, digest in EXPECTED.items():
        got = pairs.get(key, "")
        if hashlib.sha256(got.encode()).hexdigest() != digest:
            wrong.append(key)
    total = len(EXPECTED)
    if wrong:
        print(str(total - len(wrong)) + "/" + str(total) + " keys correct. Still wrong or missing: " + ", ".join(sorted(wrong)))
        return 1
    print("All " + str(total) + " answers correct.")
    print(FLAG)
    return 0

if __name__ == "__main__":
    sys.exit(main())
