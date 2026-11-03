# Writeup: TLS certificate diagnosis

Three certificates, one portal, and a folder with no notes. I worked
them in alphabetical order and wrote down everything before deciding
anything.

## Reading the candidates

For each file I pulled the dates, the subject, and the SAN list:

```
$ openssl x509 -in certs/alpha.pem -noout -dates -subject -ext subjectAltName
notBefore=Jan  1 00:00:00 2025 GMT
notAfter=Feb  1 00:00:00 2025 GMT
subject=CN = portal.nightsalvo.local
X509v3 Subject Alternative Name:
    DNS:portal.nightsalvo.local

$ openssl x509 -in certs/bravo.pem -noout -dates -subject -ext subjectAltName
notBefore=Jan  1 00:00:00 2026 GMT
notAfter=Jan  1 00:00:00 2027 GMT
subject=CN = status.nightsalvo.local
X509v3 Subject Alternative Name:
    DNS:status.nightsalvo.local

$ openssl x509 -in certs/charlie.pem -noout -dates -subject -ext subjectAltName
notBefore=Jan  1 00:00:00 2026 GMT
notAfter=Jun  1 00:00:00 2027 GMT
subject=CN = portal.nightsalvo.local
X509v3 Subject Alternative Name:
    DNS:portal.nightsalvo.local
```

The picture forms fast. Alpha carries the right name and died in
February 2025. Bravo is alive all through 2026 and named for the
status page, not the portal. Charlie has the right name and a window
that covers today.

## The dead end I almost walked into

My first instinct was to check the chains and stop there:

```
$ openssl verify -CAfile certs/lab-ca.pem certs/bravo.pem
certs/bravo.pem: OK
```

Bravo chains fine. So does charlie. Chain verification alone would
have let me deploy a certificate for the wrong hostname, because
`verify` without `-verify_hostname` never asks what name the
certificate is being presented for. The chain answers "was this
issued by someone I trust", not "is this the right certificate for
this service".

## Verifying the way a browser would

```
$ openssl verify -CAfile certs/lab-ca.pem -verify_hostname portal.nightsalvo.local certs/charlie.pem
certs/charlie.pem: OK

$ openssl verify -CAfile certs/lab-ca.pem -verify_hostname portal.nightsalvo.local certs/bravo.pem
CN = status.nightsalvo.local
error 62 at 0 depth lookup: hostname mismatch
error certs/bravo.pem: verification failed

$ openssl verify -CAfile certs/lab-ca.pem -verify_hostname portal.nightsalvo.local certs/alpha.pem
CN = portal.nightsalvo.local
error 10 at 0 depth lookup: certificate has expired
error certs/alpha.pem: verification failed

$ openssl x509 -in certs/alpha.pem -noout -checkend 0
Certificate will expire
(exit code 1: already expired)
```

Every candidate now has a verdict with evidence behind it:

- alpha: right name, expired. Reject, reason: expired.
- bravo: valid dates, issued for status.nightsalvo.local. Reject,
  reason: name mismatch.
- charlie: right name, valid dates, chain verifies. Deploy this one.

## Grading

```
deploy=charlie
alpha_reason=expired
bravo_reason=name mismatch
```

```
$ python3 grade.py
All 3 answers correct.
SALVO{tls_triage_deploy_charlie}
```

Flag: `SALVO{tls_triage_deploy_charlie}`

The lesson that stays with me: a certificate check has three separate
questions (time, name, trust), and passing one says nothing about the
other two. Most real-world certificate outages I have read about are
the alpha case, a good certificate nobody renewed.
