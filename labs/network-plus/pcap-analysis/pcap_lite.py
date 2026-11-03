#!/usr/bin/env python3
"""Minimal pcap reader for the packet analysis lab, stdlib only.

Usage:
  python3 pcap_lite.py capture.pcap           flow summary
  python3 pcap_lite.py capture.pcap --streams reassembled TCP payloads
Reassembly is done properly: segments are sorted by sequence number
per direction before their payloads are joined, which is what makes
the out-of-order HTTP response readable.
"""
import struct
import sys
from collections import defaultdict

def parse(path):
    data = open(path, "rb").read()
    magic = struct.unpack("<I", data[:4])[0]
    if magic != 0xA1B2C3D4:
        raise SystemExit("not a little-endian pcap")
    off = 24
    frames = []
    while off + 16 <= len(data):
        _, _, caplen, _ = struct.unpack("<IIII", data[off:off + 16])
        frame = data[off + 16:off + 16 + caplen]
        frames.append(frame)
        off += 16 + caplen
    return frames

def dissect(frame):
    if len(frame) < 14:
        return None
    etype = struct.unpack("!H", frame[12:14])[0]
    if etype != 0x0800:
        return ("other",)
    ip = frame[14:]
    ihl = (ip[0] & 0x0F) * 4
    proto = ip[9]
    src = ".".join(str(b) for b in ip[12:16])
    dst = ".".join(str(b) for b in ip[16:20])
    l4 = ip[ihl:]
    if proto == 17:
        sport, dport = struct.unpack("!HH", l4[:4])
        return ("udp", src, dst, sport, dport, l4[8:])
    if proto == 6:
        sport, dport, seq = struct.unpack("!HHI", l4[:8])
        doff = (l4[12] >> 4) * 4
        return ("tcp", src, dst, sport, dport, seq, l4[doff:])
    return ("ip", src, dst, proto)

def main():
    frames = [dissect(f) for f in parse(sys.argv[1])]
    frames = [f for f in frames if f]
    if "--streams" not in sys.argv:
        counts = defaultdict(int)
        for f in frames:
            if f[0] in ("udp", "tcp"):
                counts[(f[0], f[1], f[3], f[2], f[4])] += 1
            else:
                counts[(f[0],)] += 1
        for key, n in sorted(counts.items()):
            if len(key) == 5:
                print(f"{key[0]} {key[1]}:{key[2]} -> {key[3]}:{key[4]}  packets={n}")
            else:
                print(f"{key[0]}  packets={n}")
        print(f"total frames: {len(frames)}")
        return
    streams = defaultdict(list)
    for f in frames:
        if f[0] == "tcp" and f[6]:
            streams[(f[1], f[3], f[2], f[4])].append((f[5], f[6]))
    for key, segs in sorted(streams.items()):
        segs.sort(key=lambda s: s[0])
        base = segs[0][0]
        buf = bytearray()
        for seq, payload in segs:
            start = seq - base
            if start > len(buf):
                buf.extend(b"\x00" * (start - len(buf)))
            buf[start:start + len(payload)] = payload
        print(f"== {key[0]}:{key[1]} -> {key[2]}:{key[3]} ({len(buf)} bytes)")
        print(bytes(buf).decode("utf-8", "replace"))

if __name__ == "__main__":
    main()
