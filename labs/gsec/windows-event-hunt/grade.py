#!/usr/bin/env python3
"""Grader for this lab. Reads answers.txt (key=value lines), checks each
value against a stored SHA-256 of the expected answer, and prints the
lab flag when every key matches. Expected answers are hashed so the
ground truth is not sitting in plain text."""
import hashlib
import sys

EXPECTED = {'compromised_account': 'a10787635794ca5401750623382e1b6437599c60ef82ade9402f9ed34e19e793', 'source_ip': '9a6d44e97c38bcfe88cca3d4d1184a74f9d5a165ccd68abc0e0b5bb912369f76', 'created_account': '59f062f3fb511043d6d92837bf95661a905940cad040f809be006edf9c051801', 'failure_count': '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61'}
FLAG = 'SALVO{event_ids_tell_the_story}'

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
