from helper import _IPv4, _MAC

class IPv4:
  def __init__(self, src_ip: str, dest_ip: str) -> None:
    self._src = _IPv4(src_ip).toBytes()
    self._dest = _IPv4(dest_ip).toBytes()

  def checksum(self) -> bytes:
    arr = [n for n in (self._header+self._src+self._dest)]
    sum = 0
    for i in range(0, len(arr), 2):
      sum += (arr[i] << 8) + arr[i+1]
    carry = int(hex(sum)[:-4], 16) if len(hex(sum)[2:]) > 4 else 0
    check = 0xffff - (int(hex(sum)[-4:] if len(hex(sum)[2:]) > 4 else hex(sum), 16) + carry)
    return check.to_bytes(2, 'big')

  def packet(self, protocol: int, ttl: int, nextHeader: bytes) -> bytes:
    ver_IHL_TOS = b'\x45\x00'
    length = (20+len(nextHeader)).to_bytes(2, 'big')
    ID = b'\xde\xad'
    flags = b'\x00\x00'
    TTL = ttl.to_bytes(1, 'big')
    proto = protocol.to_bytes(1, 'big')
    self._header = ver_IHL_TOS+length+ID+flags+TTL+proto
    checksum = self.checksum()
    return self._header+checksum+self._src+self._dest


class TCP:
  def __init__(self, source_ip: str, source_port: int, dest_ip: str, dest_port: int) -> None:
    self._srcIP = _IPv4(source_ip).toBytes()
    self._srcPort = source_port.to_bytes(2, 'big')
    self._destIP = _IPv4(dest_ip).toBytes()
    self._destPort = dest_port.to_bytes(2, 'big')

  def checksum(self) -> bytes:
    arr = [n for n in (self._header+self._srcIP+self._destIP)]
    sum = 26 # protocol (6) + length (20)
    for i in range(0, len(arr), 2):
      sum += (arr[i] << 8) + arr[i+1]
    carry = int(hex(sum)[:-4], 16) if len(hex(sum)[2:]) > 4 else 0
    check = 0xffff - (int(hex(sum)[-4:] if len(hex(sum)[2:]) else hex(sum), 16) + carry)
    return check.to_bytes(2, 'big')

  def packet(self, seq_num: int, ack_num: int, ack: bool=False, rst: bool=False, syn: bool=False, fin: bool=False) -> bytes:
    seqNum = seq_num.to_bytes(4, 'big')
    ackNum = ack_num.to_bytes(4, 'big')
    flagstr = '0b01010000000' + ('1' if ack else '0') + '0' + ('1' if rst else '0') + ('1' if syn else '0') + ('1' if fin else '0')
    flag = bytes.fromhex(hex(int(flagstr, 2))[2:])
    window = b'\x71\x10'
    self._header = self._srcPort+self._destPort+seqNum+ackNum+flag+window
    checksum = self.checksum()
    return self._header+checksum+b'\x00\x00'

class Ether:
  def __init__(self, src: str, dest: str) -> None:
    self._src = _MAC(src).toBytes()
    self._dest = _MAC(dest).toBytes()

  def packet(self, protocol: int) -> bytes:
    return self._dest+self._src+protocol.to_bytes(2, 'big')

class UDP:
  def __init__(self, source_ip: str, source_port: int, dest_ip: str, dest_port: int) -> None:
    self._srcIP = _IPv4(source_ip).toBytes()
    self._srcPort = source_port.to_bytes(2, 'big')
    self._destIP = _IPv4(dest_ip).toBytes()
    self._destPort = dest_port.to_bytes(2, 'big')

  def checksum(self) -> bytes: 
    arr = [n for n in (self._srcPort+self._destPort+b'\x00\x08'+self._srcIP+self._destIP)]
    sum = 25 # protocol (17) + length (8)
    for i in range(0, len(arr), 2):
      sum += (arr[i] << 8) + arr[i+1]
    carry = int(hex(sum)[:-4], 16) if len(hex(sum)[2:]) > 4 else 0
    check = 0xffff - (int(hex(sum)[-4:] if len(hex(sum)[2:]) else hex(sum), 16) + carry)
    return check.to_bytes(2, 'big')

  def packet(self) -> bytes:
    length = b'\x00\x08'
    checksum = self.checksum()
    return self._srcPort+self._destPort+length+checksum

class ARP:
  def __init__(self, src_ip: str, src_mac: str) -> None:
    self._ip = _IPv4(src_ip).toBytes()
    self._mac = _MAC(src_mac).toBytes()
  
  def packet(self, protocol: int, dest_ip: str) -> bytes:
    HTYPE = b'\x00\x01' # Ethernet
    PTYPE = protocol.to_bytes(2, 'big')
    HLEN = b'\x06' # MAC length
    PLEN = b'\x04' # IPv4 length
    OP = b'\x00\x01' # request
    SHA = self._mac
    SPA = self._ip
    THA = b'\xff\xff\xff\xff\xff\xff'
    TPA = _IPv4(dest_ip).toBytes()
    return HTYPE+PTYPE+HLEN+PLEN+OP+SHA+SPA+THA+TPA

class ICMP: 
  def __init__(self) -> None:
    pass

  def checksum(self) -> bytes:
    arr = [n for n in self._header]
    sum = 0
    for i in range(0, len(arr), 2):
      sum += (arr[i] << 8) + arr[i+1]
    carry = int(hex(sum)[:-4], 16) if len(hex(sum)[2:]) > 4 else 0
    check = 0xffff - (int(hex(sum)[-4:] if len(hex(sum)[2:]) else hex(sum), 16) + carry)
    return check.to_bytes(2, 'big')
  
  def packet(self, type: int, code: int) -> bytes:
    TYPE = type.to_bytes(1, 'big')
    CODE = code.to_bytes(1, 'big')
    DATA = b'\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef'
    self._header = TYPE+CODE+DATA
    checksum = self.checksum()
    return TYPE+CODE+checksum+DATA