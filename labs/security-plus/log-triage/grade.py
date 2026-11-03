#!/usr/bin/env python3
"""Grader for this lab. Reads answers.txt (key=value lines), checks each
value against a stored SHA-256 of the expected answer, and prints the
lab flag when every key matches. Expected answers are hashed so the
ground truth is not sitting in plain text."""
import hashlib
import sys

EXPECTED = {'attacker_ip': '0c25434b09c62046f88142b1412b949ea7e9bc61479d71b2b74ab8dbc3d2d946', 'compromised_account': 'bbd6bfb2f752164deab9871907106ce81a9cc953f9868dabd0a99c14b4ca1031', 'failed_attempts': '31489056e0916d59fe3add79e63f095af3ffb81604691f21cad442a85c7be617', 'first_seen': 'd4389ac73da07345a0768d47b6044404714681f200e89c9e37da2c77a13cf3ab'}
FLAG = 'SALVO{spray_found_in_the_noise}'

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
