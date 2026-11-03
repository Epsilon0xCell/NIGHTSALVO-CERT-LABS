# Writeup: Subnet and route diagnosis

Four tickets, four different flavors of the same sin: a device
believing something false about addresses. I checked each one with
`ipaddress` instead of trusting my head arithmetic, because subnet
math done in my head is how these faults got typed in the first
place.

## WS-07: the mask that exiles the gateway

WS-07 is 192.168.10.130 with mask 255.255.255.128, a /25, on a LAN
designed as a /24. From the host's own arithmetic:

```
$ python3 -c "
import ipaddress
host = ipaddress.ip_interface('192.168.10.130/25')
print('WS-07 network:', host.network)
print('gateway 192.168.10.1 in it:', ipaddress.ip_address('192.168.10.1') in host.network)"
WS-07 network: 192.168.10.128/25
gateway 192.168.10.1 in it: False
```

The host believes it lives in 192.168.10.128/25, and its gateway,
192.168.10.1, is not in that network. A host sends off-subnet
traffic to the gateway, and reaches the gateway because the gateway
is on-subnet. Here it is not, from the one perspective that matters,
the host's. Local traffic works, everything remote fails, and the
ticket writes itself. Fault code: `mask`.

## PRN-02: the gateway that does not exist

The printer is 192.168.20.45/24 with gateway 192.168.20.254. The
design says the branch gateway is R2 at 192.168.20.1, and the ticket
notes nothing answers at .254. Local printing works because local
delivery never consults a gateway; remote traffic goes to .254 and
dies quietly. No computation needed, just comparing the typed
gateway against the design. Fault code: `gateway`.

## R2: the route to a broadcast address

R2 holds a static route to 10.30.0.0/24 via 10.0.0.3, across a WAN
link addressed as a /30:

```
WAN /30 hosts: [IPv4Address('10.0.0.1'), IPv4Address('10.0.0.2')]
10.0.0.3 is broadcast: True
```

A /30 has two usable addresses: .1 is R1, .2 is R2 itself. The next
hop .3 is the link's broadcast address, which is not a router and
never forwards anything. The route should point at 10.0.0.1. This
was my slowest ticket, because a next hop one digit off a valid
address looks right at reading speed. Fault code: `route`.

## NEW-CABINET: the plan inside the plan

The planned training-room subnet, 192.168.10.128/25, against the HQ
LAN, 192.168.10.0/24:

```
NEW-CABINET inside HQ LAN: True
```

It is not adjacent to the HQ LAN, it is inside it: every address in
the /25 is already an HQ address. Two networks cannot own the same
addresses in one design. Fault code: `overlap`.

## Grading

```
ws07=mask
prn02=gateway
r2=route
new_cabinet=overlap
```

```
$ python3 grade.py
All 4 answers correct.
SALVO{subnet_math_beats_guessing}
```

Flag: `SALVO{subnet_math_beats_guessing}`

Four tickets, and not one of them was a broken device. Every fault
was a belief: a mask, a gateway, a next hop, a plan. That is most of
network troubleshooting in one exercise, and it is why I now compute
instead of eyeballing: eyeballing is what produced the .3.
