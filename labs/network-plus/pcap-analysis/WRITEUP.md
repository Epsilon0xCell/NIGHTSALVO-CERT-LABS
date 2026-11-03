# Writeup: Packet capture analysis

Sixteen frames. I listed them before I read any of them, because in
a capture the summary is the map and the payloads are the territory.

## The map

```
$ python3 pcap_lite.py capture.pcap
tcp 10.0.5.14:49800 -> 142.250.72.14:443  packets=4
tcp 10.0.5.14:52344 -> 93.184.216.34:80  packets=4
tcp 93.184.216.34:80 -> 10.0.5.14:52344  packets=4
udp 10.0.5.1:53 -> 10.0.5.14:53100  packets=1
udp 10.0.5.1:53 -> 10.0.5.14:53101  packets=1
udp 10.0.5.14:53100 -> 10.0.5.1:53  packets=1
udp 10.0.5.14:53101 -> 10.0.5.1:53  packets=1
total frames: 16
```

Four conversations: two DNS round trips between the workstation
(10.0.5.14) and its resolver, a four-packet flow to port 443 whose
payloads are opaque (TLS, and irrelevant here), and a full HTTP
exchange with 93.184.216.34 on port 80. The HTTP flow is the one
with something to read.

## The dead end: capture order is not stream order

My first look at the server-to-client payload joined the two data
segments in the order they sit in the file. That gives:

```
report</h1><p>Reference code: SALVO{...}</p></body></html>HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 118

<html><body><h1>Quarterly
```

The second half of the page, then the headers, then the first half.
The later bytes were captured first, which happens on real networks
whenever a segment is retransmitted or paths differ. TCP's answer to
this is the sequence number: every byte in the stream has an
address, and reassembly means placing payloads at their addresses,
not stacking them in arrival order.

## Reassembly by sequence number

`pcap_lite.py --streams` sorts each direction's segments by
sequence number and writes each payload at its offset:

```
$ python3 pcap_lite.py capture.pcap --streams
...
<html><body><h1>Quarterly report</h1><p>Reference code: SALVO{pcap_stream_reassembly_finds_the_flag}</p></body></html>
```

The page reads clean end to end, headers first, and the reference
code support asked for is sitting in the body.

Flag: `SALVO{pcap_stream_reassembly_finds_the_flag}`

What this lab is really about: a packet capture is not a recording
of the conversation, it is a bag of addressed pieces of several
conversations. Every follow-the-stream button in every tool is doing
exactly what the parser does here, demultiplex by the four-tuple,
then sort by sequence. Once I saw the generator and the parser side
by side, the tool stopped being magic, which is the point of
building it from the standard library instead of only clicking it.
