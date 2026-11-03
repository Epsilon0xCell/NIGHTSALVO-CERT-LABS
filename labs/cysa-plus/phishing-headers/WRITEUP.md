# Writeup: Phishing email header analysis

I did not read the message bodies first. Bodies are written to be
believed; headers are written by machines, and machines are worse
liars. One grep pulled the verdict line out of all four messages:

```
$ grep -h "Authentication-Results" mail/*.eml
Authentication-Results: mx.nightsalvo.com; spf=pass smtp.mailfrom=nightsalvo.com; dkim=pass header.d=nightsalvo.com; dmarc=pass header.from=nightsalvo.com
Authentication-Results: mx.nightsalvo.com; spf=fail smtp.mailfrom=paypa1-secure.example; dkim=none; dmarc=fail header.from=paypa1-secure.example
Authentication-Results: mx.nightsalvo.com; spf=fail smtp.mailfrom=nightsalvo.com (sender IP 198.51.100.77 is not authorized); dkim=none; dmarc=fail header.from=nightsalvo.com
Authentication-Results: mx.nightsalvo.com; spf=pass smtp.mailfrom=nightsalvo.com; dkim=pass header.d=nightsalvo.com; dmarc=pass header.from=nightsalvo.com
```

```
$ grep -l "spf=fail" mail/*.eml
mail/msg2.eml
mail/msg3.eml
```

Two messages pass everything (msg1, the invoice notice, and msg4,
the newsletter, both with aligned From, Return-Path, and Reply-To).
Two fail, and they fail in instructively different ways.

## msg2: the lookalike

From is `support@paypa1-secure.example`, digit 1 standing in for the
letter l in the brand name, on a domain that is not the brand's.
SPF fails, DKIM is absent, DMARC fails, and the Reply-To moves the
conversation to a third domain entirely, `quickreply.example`. Any
one of those is a tell; together they are a confession. This is the
external lookalike.

## msg3: the one wearing our own name

From is `helpdesk@nightsalvo.com`, our real domain, and the
Reply-To matches it, which is exactly what makes this message the
dangerous one in a busy inbox. The headers undo the costume:
Return-Path is a bulk sender's domain, the Received line shows the
mail arriving from that sender's relay at 198.51.100.77, and the
SPF result says it in plain language: that address is not
authorized to send for nightsalvo.com. A message can borrow a
display name in one line of text. It cannot borrow the DNS records
that SPF checks. This is the internal spoof.

## The dead end worth naming

My first pass flagged msg1 as suspicious because invoice emails are
a classic phish shape, and its body asks the user to sign in to a
portal. The headers say otherwise on every check, and the body
itself, read second, never includes a link at all. Suspicion aimed
by genre is how analysts burn their morning; the authentication
results are the evidence, and they outrank the vibe.

## Grading

```
phish_messages=msg2,msg3
internal_spoof=msg3
lookalike_domain=msg2
```

```
$ python3 grade.py
All 3 answers correct.
SALVO{headers_never_lie}
```

Flag: `SALVO{headers_never_lie}`

The durable lesson: judge a message by the checks it cannot fake.
Display names, logos, and urgency are free to forge. SPF, DKIM, and
DMARC alignment cost the sender control of real infrastructure,
which is why the fakes keep failing them.
