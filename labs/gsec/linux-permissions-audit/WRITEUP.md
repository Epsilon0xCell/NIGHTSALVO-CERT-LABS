# Writeup: Linux permissions audit

I built the tree and then audited it the way I would audit a box I
had never seen: numeric questions first, opinions after.

```
$ python3 build_tree.py
audit_tree built
```

## Setuid first, it is the shortest list with the longest shadow

```
$ find audit_tree -perm -4000 -type f -ls
    53896      4 -rwsr-xr-x   1 root     root           49 Nov  3 04:27 audit_tree/bin/testshell
    53895      4 -rwsr-xr-x   1 root     root           30 Nov  3 04:27 audit_tree/bin/backup_tool
```

(In my sandbox the files carry the lab user's ownership; the listing
above is from the build run. The modes are what matter.)

Two setuid files. `backup_tool` is at least a plausible shape for
the bit, a backup helper that needs privilege. `testshell` is the
finding: its own contents say it is a leftover test shell, and it
still runs with its owner's privileges for anyone who executes it.
Setuid is a short list on any healthy system, and every entry on it
should be able to explain itself. This one explains itself as a
mistake.

## World-writable

```
$ find audit_tree -perm -0002 -ls
    53910      0 drwxrwxrwx   2 root     root           40 Nov  3 04:27 audit_tree/var/www/upload
```

One hit: the web upload directory is writable by everyone. Upload
directories are where untrusted content lands by design, so this one
wants a hard look at what the web server will execute out of it. In
this tree there is nothing to execute yet, which makes it a hole
waiting for a tenant rather than a live compromise.

## The dead end: world-readable is invisible until you aim at it

My first pass at the sensitive files was a plain `ls -l` over the
tree, and it taught me nothing: almost everything is 644, so the
dangerous 644s hide among the harmless ones. The fix was to stop
scanning everything and name the files that should never be
world-readable, then check only them:

- `etc/shadow.bak` at 644: a shadow backup anyone can read.
- `home/user/.ssh/id_rsa.bak` at 644: a private key backup anyone
  can read.
- `etc/passwd.bak` at 600: the one that was done right, and the
  contrast proves the other two are oversights, not policy.

## The flag

```
$ grep -r "SALVO" audit_tree 2>/dev/null
audit_tree/etc/shadow.bak:flag: SALVO{suid_audit_shadow_bak_world_readable}
```

Flag: `SALVO{suid_audit_shadow_bak_world_readable}`

Findings list, as the lab asks for it:

- Setuid: `bin/backup_tool` (4755), `bin/testshell` (4755, the
  finding that matters).
- World-writable: `var/www/upload` (777).
- Over-readable sensitive files: `etc/shadow.bak` (644),
  `home/user/.ssh/id_rsa.bak` (644).

The habit I want from this lab: on any new box, the setuid list and
the world-writable list are two commands and thirty seconds, and
they catch the class of mistake that survives every careful design
review, because nobody designed it. It accumulated.
