#!/usr/bin/env python3
"""Grader for this lab. Reads answers.txt (key=value lines), checks each
value against a stored SHA-256 of the expected answer, and prints the
lab flag when every key matches. Expected answers are hashed so the
ground truth is not sitting in plain text."""
import hashlib
import sys

EXPECTED = {'ws07': '48bf9b4f142ab45cac6f33cf99415bca6ca8e07608a031237aa76560fec2204b', 'prn02': '4ea5ee68fea05586106890ded5733820bb77d919cda27bc4b8139b7cd33b8889', 'r2': '8a84e406c08ac9594f47222406598f7598e15c55f8044b04813e28c9dee70976', 'new_cabinet': 'fe55bd22d9475bdebec3c49d274b87f5a264b12865f4c45b03120992e726f659'}
FLAG = 'SALVO{subnet_math_beats_guessing}'

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
