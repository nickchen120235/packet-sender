class _IPv4:
  def __init__(self, ip: str) -> None:
    self.ip = ip

  def toBytes(self) -> bytes:
    return bytes([int(n) for n in self.ip.split('.')])

class _MAC:
  def __init__(self, mac: str) -> None:
    self.mac = mac

  def toBytes(self) -> bytes:
    return bytes.fromhex(self.mac.replace(':', ''))

ETH_P_IP = 0x0800
ETH_P_ARP = 0x0806
ETH_P_ALL = 0x0003

class Unpacker:
  def __init__(self, packet: bytes) -> None:
    self._ether = packet[0:14]
    self._ipv4 = packet[14:34]
    self._tcp = packet[34:]
    self._udp = packet[34:]
    self._icmp = packet[34:]
    self._arp = packet[14:]

  def ether(self) -> dict:
    return {
      'dest': self._ether[0:6].hex(':'),
      'src': self._ether[6:12].hex(':'),
      'proto': '0x'+self._ether[12:14].hex()
    }

  def ipv4(self) -> dict:
    return {
      'ver': int(self._ipv4[0]) >> 4,
      'IHL': int(self._ipv4[0]) - ((int(self._ipv4[0]) >> 4) << 4),
      'length': (int(self._ipv4[2] << 8)) + int(self._ipv4[3]),
      'ID': hex((int(self._ipv4[4] << 8)) + int(self._ipv4[5])),
      'ttl': int(self._ipv4[8]),
      'protocol': hex(int(self._ipv4[9])),
      'checksum': hex((int(self._ipv4[10] << 8)) + int(self._ipv4[11])),
      'src': f'{int(self._ipv4[12])}.{int(self._ipv4[13])}.{int(self._ipv4[14])}.{int(self._ipv4[15])}',
      'dest': f'{int(self._ipv4[16])}.{int(self._ipv4[17])}.{int(self._ipv4[18])}.{int(self._ipv4[19])}'
    }

  def tcp(self) -> dict:
    flags = bin((int(self._tcp[12]) << 8) + int(self._tcp[13]))[2:].zfill(16)
    return {
      'srcPort': (int(self._tcp[0]) << 8) + int(self._tcp[1]),
      'destPort': (int(self._tcp[2]) << 8) + int(self._tcp[3]),
      'seq_num': (int(self._tcp[4]) << 24) + (int(self._tcp[5]) << 16) + (int(self._tcp[6]) << 8) + int(self._tcp[7]),
      'ack_num': (int(self._tcp[8]) << 24) + (int(self._tcp[9]) << 16) + (int(self._tcp[10]) << 8) + int(self._tcp[11]),
      'offset': int(flags[0:4], 2),
      'ack': True if flags[11] == '1' else False,
      'rst': True if flags[13] == '1' else False,
      'syn': True if flags[14] == '1' else False,
      'fin': True if flags[15] == '1' else False,
      'window': (int(self._tcp[14]) << 8) + int(self._tcp[15]),
      'checksum': hex((int(self._tcp[16]) << 8) + int(self._tcp[17]))
    }
    
  def udp(self) -> dict:
    return {
      'srcPort': (int(self._udp[0] << 8) + int(self._udp[1]),
      'destPort': (int(self._udp[2] << 8) + int(self._udp[3]),
      'length': (int(self._udp[4] << 8) + int(self._udp[5]),
      'checksum': (int(self._udp[6] << 8) + int(self._udp[7])
    }

  def arp(self) -> dict:
    return {
      'HTYPE': int(self._arp[0]) << 8 + int(self._arp[1]),
      'PTYPE': '0x'+self._arp[2:4].hex(),
      'HLEN': int(self._arp[4]),
      'PLEN': int(self._arp[5]),
      'OP': int(self._arp[6]) << 8 + int(self._arp[7]),
      'SHA': self._arp[8:14].hex(':'),
      'SPA': f'{int(self._arp[14])}.{int(self._arp[15])}.{int(self._arp[16])}.{int(self._arp[17])}',
      'THA': self._arp[18:24].hex(':'),
      'TPA': f'{int(self._arp[24])}.{int(self._arp[25])}.{int(self._arp[26])}.{int(self._arp[27])}'
    }

  def icmp(self) -> dict:
    return {
      'TYPE': int(self._icmp[0]),
      'CODE': int(self._icmp[1]),
      'checksum': '0x'+self._icmp[2:4].hex(),
      'DATA': '0x'+self._icmp[4:].hex()
    }
