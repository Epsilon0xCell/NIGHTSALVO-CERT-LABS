# Lab: Subnet and route diagnosis

- Track: CompTIA Network+
- Objective mapping: Domain 3, Network Operations: IP addressing,
  subnetting, default gateways, and static routing.

## Scenario

`topology.txt` describes a two-site office network the way it was
found on Monday morning: the design, the configurations as actually
typed into each device, and four open trouble tickets. All four
tickets trace to addressing or routing faults in the as-configured
column. The design column is correct; trust it over the devices.

## Setup

Nothing to build. A subnet calculator or Python's `ipaddress`
module will check your arithmetic, and checking is encouraged:
the skill is knowing which computation answers which ticket.

## Tasks

For each ticket, name the fault with exactly one of these codes:
`mask`, `gateway`, `route`, `overlap`.

1. WS-07 cannot reach anything off its own subnet.
2. PRN-02 is unreachable from anywhere remote.
3. R2's static route to the server net delivers nothing.
4. The planned training-room subnet conflicts with something.

## Answer format

Create `answers.txt` in this folder:

```
ws07=<code>
prn02=<code>
r2=<code>
new_cabinet=<code>
```

Then run `python3 grade.py`.

## Hint ladder

1. Work one ticket at a time, and for each one write down what the
   device believes its own network is. Faults live in the gap
   between belief and design.
2. A host decides local versus remote by ANDing its address with
   its mask. If the gateway does not land inside the result, the
   host cannot even ARP for it. A /30 link has exactly two usable
   addresses; count them before judging a next hop.
3. The Network+ addressing materials cover the mask arithmetic and
   the subnet-of test for overlapping plans.
