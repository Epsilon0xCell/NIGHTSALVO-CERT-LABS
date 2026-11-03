# NIGHTSALVO-CERT-LABS

Hands-on certification labs, built the slow way: every lab is original,
keyed to a published certification exam objective domain, and shipped
only after its solution has been executed and verified in session.

## Why this repo exists

Certifications test whether you can recognize and work a problem, not
whether you can recite one. These labs drill the working half. Each lab
hands you realistic material (logs, captures, certificates, scan output,
a file tree), a set of tasks, and a hint ladder for when you get stuck.
The writeup in every folder is my own full solution, with the dead ends
left in, because the dead ends are where the learning is.

## Rules the repo runs on

- Labs map to public exam objective domains only. No actual exam
  questions, no braindump material, ever. All content is original.
- No lab ships unverified. The solution in each WRITEUP.md was run
  against the shipped materials before the lab was published, and the
  flag or answer set was recovered from that run.
- Where an environment limit blocks part of a solution chain, the
  writeup says so openly instead of papering over it.

## Status board

- Labs completed: 8
- Cert tracks: 4 (CompTIA Security+, GIAC GSEC, CompTIA Network+, CompTIA CySA+)
- Current tier: INITIATE (see TIERS.md; the batch that crossed the tier
  is named there)

## Layout

- `labs/INDEX.md` lists every lab with its track and objective mapping.
- `labs/<track>/<lab-name>/` holds one lab: README (objectives, setup,
  tasks, hint ladder), the materials or the generator that builds them,
  and WRITEUP.md with the verified solution.
- `LAB-TEMPLATE.md` is the shape every lab follows.
- `TIERS.md` is the ladder the repo is graded against.

Built by Gavin Blacklock (Epsilon0xCell).
