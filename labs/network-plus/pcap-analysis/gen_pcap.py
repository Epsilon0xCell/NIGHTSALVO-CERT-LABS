#!/usr/bin/env python3
"""Generate capture.pcap for the packet analysis lab, stdlib only.

Three flows go in the capture:
1. A DNS lookup for updates.example.net and its reply (routine).
2. A DNS lookup for cdn-sync.example.org and its reply (routine).
3. An HTTP exchange where the response body arrives split across two
   TCP segments. The flag is in the body, so it only appears whole
   once the stream is reassembled in order.
Plus a short TLS-looking flow of random bytes on port 443 (noise).
"""
import random
import struct

random.seed(11)

def csum(data):
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    return (~total) & 0xFFFF

def ip_packet(src, dst, proto, payload, ident):
    src_b = bytes(int(x) for x in src.split("."))
    dst_b = bytes(int(x) for x in dst.split("."))
    total = 20 + len(payload)
    hdr = struct.pack("!BBHHHBBH", 0x45, 0, total, ident, 0x4000, 64, proto, 0)
    hdr = hdr[:10] + struct.pack("!H", csum(hdr + src_b + dst_b)) + hdr[12:]
    return hdr + src_b + dst_b + payload

def eth(payload, etype=0x0800):
    return bytes.fromhex("aabbccddeeff") + bytes.fromhex("112233445566") + struct.pack("!H", etype) + payload

def udp(src, dst, sport, dport, payload):
    seg = struct.pack("!HHHH", sport, dport, 8 + len(payload), 0) + payload
    return eth(ip_packet(src, dst, 17, seg, random.randint(1, 60000)))

def tcp(src, dst, sport, dport, seq, ack, flags, payload=b""):
    seg = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 0x50, flags, 65535, 0, 0) + payload
    return eth(ip_packet(src, dst, 6, seg, random.randint(1, 60000)))

def dns_query(name, ident, answer_ip=None):
    labels = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
    q = struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0) + labels + struct.pack("!HH", 1, 1)
    if answer_ip is None:
        return q
    ans = struct.pack("!HHHHHH", ident, 0x8180, 1, 1, 0, 0) + labels + struct.pack("!HH", 1, 1)
    ans += b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 300, 4) + bytes(int(x) for x in answer_ip.split("."))
    return ans

packets = []

# DNS noise flow 1
packets.append(udp("10.0.5.14", "10.0.5.1", 53100, 53, dns_query("updates.example.net", 0x1001)))
packets.append(udp("10.0.5.1", "10.0.5.14", 53, 53100, dns_query("updates.example.net", 0x1001, "203.0.113.10")))

# DNS noise flow 2
packets.append(udp("10.0.5.14", "10.0.5.1", 53101, 53, dns_query("cdn-sync.example.org", 0x1002)))
packets.append(udp("10.0.5.1", "10.0.5.14", 53, 53101, dns_query("cdn-sync.example.org", 0x1002, "198.51.100.44")))

# HTTP flow: handshake, request, two-segment response, teardown.
C, S, CP, SP = "10.0.5.14", "93.184.216.34", 52344, 80
body = (b"<html><body><h1>Quarterly report</h1>"
        b"<p>Reference code: SALVO{pcap_stream_reassembly_finds_the_flag}</p>"
        b"</body></html>")
resp = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body
cut = len(resp) // 2
packets.append(tcp(C, S, CP, SP, 1000, 0, 0x02))                      # SYN
packets.append(tcp(S, C, SP, CP, 5000, 1001, 0x12))                   # SYN-ACK
packets.append(tcp(C, S, CP, SP, 1001, 5001, 0x10))                   # ACK
req = b"GET /report HTTP/1.1\r\nHost: files.example.net\r\n\r\n"
packets.append(tcp(C, S, CP, SP, 1001, 5001, 0x18, req))              # PSH-ACK request
packets.append(tcp(S, C, SP, CP, 5001, 1001 + len(req), 0x10))        # ACK
packets.append(tcp(S, C, SP, CP, 5001 + cut, 1001 + len(req), 0x18, resp[cut:]))   # segment 2 arrives first
packets.append(tcp(S, C, SP, CP, 5001, 1001 + len(req), 0x18, resp[:cut]))   # segment 1 (retransmit order in file)
packets.append(tcp(C, S, CP, SP, 1001 + len(req), 5001 + len(resp), 0x11))   # FIN-ACK

# TLS-looking noise flow.
for i in range(4):
    packets.append(tcp(C, "142.250.72.14", 49800, 443, 2000 + i * 100, 9000, 0x18, bytes(random.getrandbits(8) for _ in range(120))))

with open("capture.pcap", "wb") as fh:
    fh.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    ts = 1762000000
    for i, pkt in enumerate(packets):
        fh.write(struct.pack("<IIII", ts + i, i * 1000, len(pkt), len(pkt)))
        fh.write(pkt)

print(f"wrote capture.pcap: {len(packets)} packets")
