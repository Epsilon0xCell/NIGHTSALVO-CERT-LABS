# Lab template

Every lab in this repo follows this shape. A lab folder lives at
`labs/<track>/<lab-name>/` and contains:

- `README.md`
  - Track and the public exam objective domain the lab maps to.
  - Scenario: what the material is and where it supposedly came from.
  - Setup: exact commands to prepare the lab, including running any
    generator that ships with it.
  - Tasks: numbered, each with a checkable outcome.
  - Answer format: the exact keys the grader expects, or where the
    flag sits to be recovered.
  - Hint ladder: three rungs, from a nudge to the concept to the
    documentation pointer. Hints never contain the answer.
- Materials: the files the lab works on (logs, captures, certificates,
  reports, message files), or a generator script (`gen_*.py`,
  `build_*.py`, `make_*.sh`) that produces them deterministically,
  plus the generated output itself so the lab works without running
  the generator.
- `grade.py` where the lab uses an answer set: reads `answers.txt`
  (key=value lines), compares each answer against a stored SHA-256
  of the expected value, and prints the lab flag on a full match.
  Labs whose flag is recovered from the material itself ship no
  grader; the writeup shows the recovery.
- `WRITEUP.md`
  - First person, my voice, the full working process: what I ran,
    what failed, the breakthrough, and the verified flag or answer
    set at the end.
  - Real commands with real output, trimmed only for repetition.
  - Any environment caveat stated openly in the writeup, never
    buried.

Naming: track folders are `security-plus`, `gsec`, `network-plus`,
`cysa-plus`. Lab names are short, lowercase, hyphenated, and describe
the task rather than the answer.
