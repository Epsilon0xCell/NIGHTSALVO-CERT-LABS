#!/usr/bin/env python3
"""Generate auth.log for the log triage lab. Deterministic (seed 42).

Scenario baked into the noise: one external address password-sprays the
host, fails against many accounts, then gets in as svc_backup. A second
external address fails three times and gives up (the decoy).
"""
import random
from datetime import datetime, timedelta

random.seed(42)

HOST = "bastion-01"
START = datetime(2026, 10, 14, 0, 3, 11)
USERS = ["amara", "j.okafor", "priya", "tom.h", "lena", "svc_deploy",
         "marcus", "ingrid", "d.reyes", "fatima", "oleg", "nina"]
GOOD_IPS = ["10.20.4.15", "10.20.4.22", "10.20.7.9", "172.16.0.31"]
ATTACKER = "203.0.113.77"
DECOY = "198.51.100.23"
TARGETS = ["root", "admin", "amara", "j.okafor", "priya", "tom.h",
           "lena", "marcus", "ingrid", "d.reyes", "fatima", "oleg",
           "nina", "svc_deploy", "svc_backup", "deploy", "ubuntu",
           "oracle", "postgres", "git", "jenkins", "backup", "test",
           "guest"]

lines = []
t = START
pid = 1100

def stamp(ts):
    return ts.strftime("%b %e %H:%M:%S")

def add(ts, msg):
    global pid
    pid += random.randint(1, 37)
    lines.append((ts, f"{stamp(ts)} {HOST} sshd[{pid}]: {msg}"))

# Background noise: six hours of ordinary traffic.
while t < START + timedelta(hours=6):
    t += timedelta(seconds=random.randint(20, 240))
    u = random.choice(USERS)
    ip = random.choice(GOOD_IPS)
    if random.random() < 0.82:
        add(t, f"Accepted password for {u} from {ip} port {random.randint(1024, 65000)} ssh2")
    else:
        add(t, f"Failed password for {u} from {ip} port {random.randint(1024, 65000)} ssh2")

# The decoy: three failures, then nothing.
dt = START + timedelta(hours=2, minutes=14)
for i in range(3):
    add(dt + timedelta(seconds=41 * i),
        f"Failed password for admin from {DECOY} port {51100 + i} ssh2")

# The spray: 47 failures, then a success as svc_backup.
at = START + timedelta(hours=4, minutes=2, seconds=9)
first_seen = at
fails = 0
for i, user in enumerate(TARGETS * 2):
    if fails >= 47:
        break
    add(at, f"Failed password for {user} from {ATTACKER} port {40000 + i} ssh2")
    fails += 1
    at += timedelta(seconds=random.randint(4, 11))
success_at = at + timedelta(seconds=9)
add(success_at, f"Accepted password for svc_backup from {ATTACKER} port 40047 ssh2")
add(success_at + timedelta(seconds=48),
    f"session opened for user svc_backup by (uid=0)")

lines.sort(key=lambda x: x[0])
with open("auth.log", "w") as fh:
    for _, line in lines:
        fh.write(line + "\n")

print(f"wrote auth.log: {len(lines)} lines")
print(f"ground truth: attacker_ip={ATTACKER} compromised_account=svc_backup "
      f"failed_attempts={fails} first_seen={stamp(first_seen)}")
