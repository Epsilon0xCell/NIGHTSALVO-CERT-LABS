# Lab: Linux permissions audit

- Track: GIAC GSEC
- Objective mapping: Linux security and hardening: file permissions,
  setuid and setgid controls, least privilege on sensitive files.

## Scenario

A small server was built by hand over two years and never audited.
`build_tree.py` recreates its file tree under `audit_tree/`: the same
relative paths and the same permission modes, with harmless stand-in
content. Two of the files in that tree are findings waiting for a
report, one directory is a hole, and one file hands you the lab flag
precisely because its permissions are wrong.

The tree is built and owned by your own lab user, not root. The modes
are the lesson; on a production box the same modes on root-owned
files are the incident.

## Setup

```
python3 build_tree.py
```

## Tasks

1. List every setuid file in the tree, with its mode.
2. List every world-writable file or directory in the tree.
3. List the files under `etc/` and `.ssh/` whose contents should
   never be world-readable, and check their actual modes.
4. Recover the lab flag from the file that proves the point.

## Answer format

There is no grader in this lab. The flag sits in the material, in
`SALVO{...}` form, and finding it with the audit commands is the
proof. Your findings list should name: both setuid files, the
world-writable directory, and both over-readable sensitive files.

## Hint ladder

1. Permissions are numbers. Ask find(1) numeric questions instead of
   reading listings by eye.
2. `find <dir> -perm -4000` finds setuid files; `-perm -0002` finds
   world-writable entries. World-readable is the default state of
   most files, which is why sensitive files have to opt out of it.
3. The find(1) manual page section on `-perm` explains the minus
   sign form, which means "all of these bits set."
