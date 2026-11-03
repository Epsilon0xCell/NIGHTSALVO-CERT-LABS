# Lab: TLS certificate diagnosis

- Track: CompTIA Security+ (SY0-701)
- Objective mapping: Domain 1, General Security Concepts: cryptography
  concepts, public key infrastructure, and certificate management.

## Scenario

The internal portal at `portal.nightsalvo.local` needs a certificate
installed today. The previous admin left three candidate certificates
in a folder, all issued by the lab CA, and no note about which one is
the right one. Picking wrong means a browser error page for every user,
and each candidate fails or passes for a different reason.

The lab CA certificate is at `certs/lab-ca.pem` so you can verify
chains. `make_certs.sh` documents how the three candidates were made.

## Setup

Nothing to build. The materials are the three files in `certs/`:
`alpha.pem`, `bravo.pem`, `charlie.pem`. You need `openssl` only.

## Tasks

1. For each candidate, read its validity dates, subject, and subject
   alternative names.
2. Verify each candidate against the lab CA with hostname checking
   turned on for `portal.nightsalvo.local`.
3. Decide which single certificate gets deployed, and name the exact
   reason each of the other two must be rejected.

## Answer format

Create `answers.txt` in this folder:

```
deploy=<alpha|bravo|charlie>
alpha_reason=<one or two words>
bravo_reason=<one or two words>
```

Then run `python3 grade.py`.

## Hint ladder

1. A certificate can fail on time, on name, or on trust. Check all
   three for every candidate before deciding.
2. `openssl x509 -dates -subject -ext subjectAltName` reads the
   fields. `openssl verify -verify_hostname` tests the name the way
   a browser would.
3. Read the OpenSSL manual pages for `verify` and `x509`, in
   particular the sections on hostname verification and expiry
   checking.
