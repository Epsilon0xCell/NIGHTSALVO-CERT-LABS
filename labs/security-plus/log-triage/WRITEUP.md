# Writeup: Log triage, find the spray

The ticket said "someone was knocking." I started by sizing the log
and counting failures before reading a single line closely.

## Count first

```
$ wc -l auth.log
219 auth.log

$ grep -c "Failed password" auth.log
79
```

Seventy-nine failures in a morning is worth understanding. The
question is who owns them:

```
$ grep "Failed password" auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | head -5
     47 203.0.113.77
     11 10.20.7.9
      9 10.20.4.15
      6 172.16.0.31
      3 198.51.100.23
```

One external address owns 47 of the 79 failures. The internal
addresses in the list are ordinary users mistyping passwords. The
other external, 198.51.100.23, failed three times and stopped: that
is the decoy, and the count alone nearly let me report it.

## The dead end, and the question that fixed it

Counting failures ranks the knockers, but knocking is not the
incident. The incident is a success. So I asked the log the second
question, which addresses ever got in:

```
$ grep "203.0.113.77" auth.log | grep -c "Failed"
47

$ grep "203.0.113.77" auth.log | head -1
Oct 14 04:05:20 bastion-01 sshd[4679]: Failed password for root from 203.0.113.77 port 40000 ssh2

$ grep "Accepted" auth.log | grep "203.0.113.77"
Oct 14 04:11:48 bastion-01 sshd[5623]: Accepted password for svc_backup from 203.0.113.77 port 40047 ssh2
```

There it is. Forty-seven failures starting 04:05:20, walking a list
of account names, and at 04:11:48 an Accepted line for `svc_backup`.
A service account, reached by spraying, is exactly the kind of quiet
win an attacker wants: nobody watches a backup account the way they
watch their own. The decoy address never has an Accepted line, which
is what separates a nuisance from a compromise.

## Grading

```
attacker_ip=203.0.113.77
compromised_account=svc_backup
failed_attempts=47
first_seen=Oct 14 04:05:20
```

```
$ python3 grade.py
All 4 answers correct.
SALVO{spray_found_in_the_noise}
```

Flag: `SALVO{spray_found_in_the_noise}`

What I take from this one: the report that matters is four facts
(address, count, account, first seen), and every one of them came
from grouping and counting rather than reading. The single most
important line in the file, the Accepted line, is one line out of
219, and it only stands out once you already know whose lines to
pull.
