#!/usr/bin/env python3
"""Generate events.csv, a synthetic Windows-style security event log.

The data is invented for this lab and shipped as CSV on purpose: the
skill being drilled is reading event IDs and sequences, not parsing
the EVTX binary format. Scenario in the noise: one workstation takes
14 failed logons (4625) for j.okafor from a single internal address,
then a success (4624), then that account creates a new account
(4720) named temp.admin2 and adds it to a privileged group (4732).
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(7)

START = datetime(2026, 10, 12, 8, 0, 0)
ROWS = []

def add(ts, eid, account, ip, ws, msg):
    ROWS.append([ts.strftime("%Y-%m-%d %H:%M:%S"), eid, account, ip, ws, msg])

USERS = ["amara", "priya", "tom.h", "lena", "marcus", "ingrid"]
WORKSTATIONS = ["WS-101", "WS-104", "WS-107", "WS-112"]

t = START
while t < START + timedelta(hours=9):
    t += timedelta(minutes=random.randint(3, 25))
    u = random.choice(USERS)
    ws = random.choice(WORKSTATIONS)
    if random.random() < 0.75:
        add(t, 4624, u, "192.168.4." + str(random.randint(20, 60)), ws,
            "An account was successfully logged on.")
    else:
        add(t, 4634, u, "", ws, "An account was logged off.")

# The incident, late morning, against WS-104.
base = START + timedelta(hours=3, minutes=41)
for i in range(14):
    add(base + timedelta(seconds=23 * i), 4625, "j.okafor", "192.168.4.50",
        "WS-104", "An account failed to log on. Failure reason: unknown user name or bad password.")
add(base + timedelta(seconds=23 * 14), 4624, "j.okafor", "192.168.4.50",
    "WS-104", "An account was successfully logged on.")
add(base + timedelta(minutes=6), 4720, "temp.admin2", "", "WS-104",
    "A user account was created. Creator account: j.okafor.")
add(base + timedelta(minutes=9), 4732, "temp.admin2", "", "WS-104",
    "A member was added to a security-enabled global group. Group: Domain Admins. Added by: j.okafor.")

ROWS.sort(key=lambda r: r[0])
with open("events.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["TimeCreated", "EventID", "Account", "SourceIP", "Workstation", "Message"])
    w.writerows(ROWS)

print(f"wrote events.csv: {len(ROWS)} rows")
print("ground truth: compromised_account=j.okafor source_ip=192.168.4.50 created_account=temp.admin2 failure_count=14")
