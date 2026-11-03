#!/bin/sh
# How the three candidate certificates in certs/ were made.
# They were issued by a throwaway lab CA with openssl ca, because
# openssl ca is the subcommand that accepts explicit start and end
# dates. The lab CA certificate ships as certs/lab-ca.pem so the
# chains can be verified. The CA key and the leaf keys were not kept.
#
#   alpha.pem    CN and SAN portal.nightsalvo.local,
#                2025-01-01 to 2025-02-01  (expired)
#   bravo.pem    CN and SAN status.nightsalvo.local,
#                2026-01-01 to 2027-01-01  (valid dates, wrong name)
#   charlie.pem  CN and SAN portal.nightsalvo.local,
#                2026-01-01 to 2027-06-01  (valid, correct name)
#
# Sketch of the commands (run in a scratch CA directory):
#
#   openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.pem \
#     -nodes -days 3650 -subj "/CN=NightSalvo Lab CA"
#   openssl req -newkey rsa:2048 -keyout leaf.key -out leaf.csr -nodes \
#     -subj "/CN=portal.nightsalvo.local" \
#     -addext "subjectAltName=DNS:portal.nightsalvo.local"
#   openssl ca -batch -config ca.cnf -in leaf.csr -out leaf.pem \
#     -startdate 20250101000000Z -enddate 20250201000000Z
#
# with unique_subject = no in index.txt.attr, because alpha and
# charlie share a subject name on purpose.
echo "Reference only: see the comments in this file."
