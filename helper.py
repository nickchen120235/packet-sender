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

class Unpacker:
  def __init__(self, packet: bytes) -> None:
    self._ether = packet[0:14]
    self._ipv4 = packet[14:34]
    self._tcp = packet[34:]

  def ether(self) -> dict:
    return {
      'dest': self._ether[0:6].hex(':'),
      'src': self._ether[6:12].hex(':')
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
