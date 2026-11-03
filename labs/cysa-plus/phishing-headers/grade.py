#!/usr/bin/env python3
"""Grader for this lab. Reads answers.txt (key=value lines), checks each
value against a stored SHA-256 of the expected answer, and prints the
lab flag when every key matches. Expected answers are hashed so the
ground truth is not sitting in plain text."""
import hashlib
import sys

EXPECTED = {'phish_messages': '3ea190416dba26653fcd65af393c0ea7e51f7e0348a927b8adeb27a346a4849f', 'internal_spoof': '89da2bd31a5d008c84323c9693f12f09e62a75a688a55f2a6fd24660afba5660', 'lookalike_domain': 'a78521e49048b6e0d368d3fba417fc20c7546272dafa78a8a173fcca6c81233b'}
FLAG = 'SALVO{headers_never_lie}'

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
