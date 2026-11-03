# Lab: Phishing email header analysis

- Track: CompTIA CySA+
- Objective mapping: Domain 1, Security Operations: threat intelligence
  and email analysis, phishing indicators, authentication results.

## Scenario

Four messages arrived for the same user on the same morning, in
`mail/`: msg1 through msg4. Two are legitimate. Two are phishing.
One of the phish wears a lookalike of a famous brand; the other
wears the company's own domain, which is the one that scares people
into complying. The bodies are short. The headers are the evidence,
and headers, unlike display names, are hard to dress up.

All four messages are synthetic, written for this lab. Every domain
in them is either the fictional company domain or a documentation
example domain.

## Setup

Nothing to build. Read the `.eml` files as text.

## Tasks

1. Name the two phishing messages.
2. Name the message that spoofs the company's own domain from
   outside it.
3. Name the message that uses a lookalike external brand domain.

## Answer format

Create `answers.txt` in this folder:

```
phish_messages=<msgN,msgN in ascending order>
internal_spoof=<msgN>
lookalike_domain=<msgN>
```

Then run `python3 grade.py`.

## Hint ladder

1. Ignore the body copy. Read Authentication-Results first, then
   compare From, Return-Path, and Reply-To domains message by
   message.
2. SPF fail on the company's own domain means the sending server
   was never authorized to use that name, no matter how good the
   display name looks. A Reply-To on a different domain from the
   From is a second, independent tell.
3. The CySA+ email analysis materials cover SPF, DKIM, and DMARC
   result reading, which is the whole toolkit this lab needs.
