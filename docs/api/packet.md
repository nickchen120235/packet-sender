# API Reference: `./lib/packet.py`
## `Ether`: Ethernet Layer Packet Generator
- `Ether(src: str, dest: str) -> None`: Class constructor
  - `src`: Source MAC address in the form of `XX:XX:XX:XX:XX:XX`
  - `dest`: Destination MAC address in the form of `XX:XX:XX:XX:XX:XX`
- `packet(protocol: int) -> bytes`: Returns the packet in bytes
  - `protocol`: Protocol type of the next (internet) layer (use `ETH_P_IP` or `ETH_P_ARP` from `./lib/helper.py`)

## `IPv4`: Internet Protocol Version 4 Packet Generator
- `IPv4(src_ip: str, dest_ip: str) -> None`: Class constructor
  - `src_ip`: Source IP address in the form of `XXX.XXX.XXX.XXX`
  - `dest_ip`: Destination IP address in the form of `XXX.XXX.XXX.XXX`
- `packet(protocol: int, ttl: int, nextHeaders: bytes) -> bytes`: Returns the packet in bytes
  - `protocol`: Protocol type of the next layer (use `socket.IPPROTO_*` from built-in `socket` library)
  - `ttl`: Time To Live
  - `nextHeader`: Header of the next (transport) layer for checksum calculation

## `ARP`: Address Resolution Protocol Packet Generator
- `ARP(src_ip: str, src_mac: str) -> None`: Class constructor
  - `src_ip`: Source IP address in the form of `XXX.XXX.XXX.XXX`
  - `src`: Source MAC address in the form of `XX:XX:XX:XX:XX:XX`
- `packet(protocol: int, dest_ip: str) -> bytes`: Returns the packet in bytes
  - `protocol`: Protocol type of the internetwork (use `ETH_P_IP` from `./lib/helper.py`)

## `TCP`: Transmission Control Protocol Packet Generator
- `TCP(source_ip: str, source_port: int, dest_ip: str, dest_port: int) -> None`: Class constructor
  - `source_ip`: Source IP address in the form of `XXX.XXX.XXX.XXX`
  - `source_port`: Source port (0 - 65535)
  - `dest_ip`: Destination IP address in the form of `XXX.XXX.XXX.XXX`
  - `dest_port`: Destination port (0 - 65535)
- `packet(seq_num: int, ack_num: int, ack: bool=False, rst: bool=False, syn: bool=False, fin: bool=False) -> bytes`: Returns the packet in bytes
  - `seq_num`: Sequence number
  - `ack_num`: Acknowledgement number
  - `ack`, `rst`, `syn`, `fin`: Flags of a TCP packet

## `UDP`: User Datagram Protocol Packet Generator
- `UDP(source_ip: str, source_port: int, dest_ip: str, dest_port: int) -> None`: Class constructor
  - `source_ip`: Source IP address in the form of `XXX.XXX.XXX.XXX`
  - `source_port`: Source port (0 - 65535)
  - `dest_ip`: Destination IP address in the form of `XXX.XXX.XXX.XXX`
  - `dest_port`: Destination port (0 - 65535)
- `packet()`: Returns the packet in bytes

## `ICMP`: Internet Control Message Protocol Packet Generator
- `ICMP() -> None`: Class constructor
- `packet(type: int, code: int) -> bytes`: Returns the packet in bytes
  - `type`: Type of control message
  - `code`: Operation code of the control message