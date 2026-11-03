# Writeup: Windows event log hunt

Fifty-three rows is a small haystack, but the method scales to
fifty thousand, so I used the real method: one event ID at a time,
in the order an investigator actually asks the questions.

## Failures first: who is being guessed?

```
$ awk -F, '$2==4625' events.csv | head -3
2026-10-12 11:41:00,4625,j.okafor,192.168.4.50,WS-104,An account failed to log on. Failure reason: unknown user name or bad password.
2026-10-12 11:41:23,4625,j.okafor,192.168.4.50,WS-104,An account failed to log on. Failure reason: unknown user name or bad password.
2026-10-12 11:41:46,4625,j.okafor,192.168.4.50,WS-104,An account failed to log on. Failure reason: unknown user name or bad password.

$ awk -F, '$2==4625 {print $4}' events.csv | sort | uniq -c
     14 192.168.4.50
```

Every failure in the export is the same story: account `j.okafor`,
source 192.168.4.50, fourteen attempts at 23 second intervals
starting 11:41:00. That spacing is a tool, not a person typing.

## The dead end: stopping at the failures

Fourteen failures with no success would be a non-event, and my first
pass nearly filed it that way. The failures are only the first act.
Sorting the same account's events by time shows what the failures
were buying: a 4624 success for j.okafor from 192.168.4.50 lands
right after the fourteenth failure, at 11:47 the account creates
another account, and at 11:50 that new account joins Domain Admins.

```
$ grep -E ",(4720|4732)," events.csv
2026-10-12 11:47:00,4720,temp.admin2,,WS-104,A user account was created. Creator account: j.okafor.
2026-10-12 11:50:00,4732,temp.admin2,,WS-104,A member was added to a security-enabled global group. Group: Domain Admins. Added by: j.okafor.
```

That is the whole incident in four event IDs: 4625 fourteen times,
4624 once, 4720 once, 4732 once. Guess, get in, make a friend, hand
the friend the keys. The created account, `temp.admin2`, is the
persistence: even if j.okafor's password is reset within the hour,
temp.admin2 stays.

## Grading

```
compromised_account=j.okafor
source_ip=192.168.4.50
created_account=temp.admin2
failure_count=14
```

```
$ python3 grade.py
All 4 answers correct.
SALVO{event_ids_tell_the_story}
```

Flag: `SALVO{event_ids_tell_the_story}`

The takeaway I drill from this: 4720 and 4732 are quiet events that
nobody pages on, and they are the two that turn a bad password into
a lasting problem. If I could alert on only two IDs from this lab,
it would be those, with 4625 bursts as the early warning in front
of them.
