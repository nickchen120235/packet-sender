def ipToBytearray(ip: str) -> bytearray:
  numbered_ip = [int(n) for n in ip.split('.')]
  for num in numbered_ip:
    if num < 0 or num > 255:
      raise ValueError('Invalid IP Range')
    
  if numbered_ip[0] >= 224:
    raise ValueError('Class D/E IP shouldn\'t be used.')

  return bytearray(numbered_ip)

def ip_checksum(header: bytearray, source: bytearray, dest: bytearray) -> bytearray:
  arr = [n for n in (header+source+dest)]
  sum = 0

  for i in range(0, len(arr), 2):
    sum += (arr[i] << 8) + arr[i+1]
  
  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def ipv4_packet(protocol: int, ttl: int, src: str, dest: str, nextHeader: bytearray) -> bytearray:
  ver_IHL_TOS = b'\x45\x00'
  length = (20+len(nextHeader)).to_bytes(2, 'big')
  ID = b'\xde\xad'
  flags = b'\x00\x00'
  TTL = ttl.to_bytes(1, 'big')
  proto = protocol.to_bytes(1, 'big')
  srcIP = ipToBytearray(src)
  destIP = ipToBytearray(dest)
  checksum = ip_checksum(ver_IHL_TOS+length+ID+flags+TTL+proto, srcIP, destIP)
  packet = ver_IHL_TOS+length+ID+flags+TTL+proto+checksum+srcIP+destIP
  return packet

def tcp_checksum(header: bytearray, source: bytearray, dest: bytearray) -> bytearray:
  arr = [n for n in (header+source+dest)]
  print('header: {}'.format(header))
  print('arr: {}'.format(arr))
  sum = 0

  sum += 26
  for i in range(0, len(arr), 2):
    sum += (arr[i] << 8) + arr[i+1]

  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def tcp_packet(source_port: int, dest_port: int, source_ip: str, dest_ip: str, seq_num: int, ack_num: int, ack: bool=False, rst: bool=False, syn: bool=False, fin: bool=False) -> bytearray:
  source = bytearray.fromhex('{0:#0{1}x}'.format(source_port, 6)[2:])
  dest = bytearray.fromhex('{0:#0{1}x}'.format(dest_port, 6)[2:])
  seq_arr = bytearray.fromhex('{0:#0{1}x}'.format(seq_num, 10)[2:])
  ack_arr = bytearray.fromhex('{0:#0{1}x}'.format(ack_num, 10)[2:])
  flag = '0b01010000000' + ('1' if ack else '0') + '0' + ('1' if rst else '0') + ('1' if syn else '0') + ('1' if fin else '0')
  flag_arr = bytearray.fromhex(hex(int(flag, 2))[2:])
  window = b'\x71\x10'
  checksum = tcp_checksum(source+dest+seq_arr+ack_arr+flag_arr+window, ipToBytearray(source_ip), ipToBytearray(dest_ip))
  packet = source+dest+seq_arr+ack_arr+flag_arr+window+checksum+b'\x00\x00'
  return packet

def macToBytearray(mac: str) -> bytearray:
  return bytearray.fromhex(mac.replace(':', ''))

def ether_packet(dest_mac: str,src_mac: str) -> bytearray:
  return macToBytearray(dest_mac)+macToBytearray(src_mac)+b'\x08\x00'

def udp_checksum(header: bytearray, source: bytearray, dest: bytearray) -> bytearray:
  arr = [n for n in (header+source+dest)]
  sum = 0

  sum += 8 # UDP Length
  sum += 17 # IPPROTO_UDP
  for i in range(0, len(arr), 2):
    sum += (arr[i] << 8) + arr[i+1]

  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def udp_packet(source_port: int, dest_port: int, source_ip: str, dest_ip: str) -> bytearray:
  source = bytearray.fromhex('{0:#0{1}x}'.format(source_port, 6)[2:])
  dest = bytearray.fromhex('{0:#0{1}x}'.format(dest_port, 6)[2:])
  length = b'\x00\x08'
  checksum = udp_checksum(source+dest+length, ipToBytearray(source_ip), ipToBytearray(dest_ip))
  packet = source + dest + length + checksum
  return packet

def unpackage(arr: bytearray) -> dict:
  ether = arr[0:14]
  destMac = ether[0:6].hex(':')
  srcMac = ether[6:12].hex(':')  

  ip = arr[14:34]
  IPver = int(ip[0]) >> 4
  IHL = int(ip[0]) - (IPver << 4)
  length = (int(ip[2]) << 8) + int(ip[3])
  ID = hex((int(ip[4]) << 8) + int(ip[5]))
  ttl = int(ip[8])
  proto = int(ip[9])
  IPchecksum = hex((int(ip[10]) << 8) + int(ip[11]))
  srcIP = f'{int(ip[12])}.{int(ip[13])}.{int(ip[14])}.{int(ip[15])}'
  destIP = f'{int(ip[16])}.{int(ip[17])}.{int(ip[18])}.{int(ip[19])}'

  tcp = arr[34:54]
  srcPort = (int(tcp[0]) << 8) + int(tcp[1])
  destPort = (int(tcp[2]) << 8) + int(tcp[3])
  seq_num = (int(tcp[4]) << 24) + (int(tcp[5]) << 16) + (int(tcp[6]) << 8) + int(tcp[7])
  ack_num = (int(tcp[8]) << 24) + (int(tcp[9]) << 16) + (int(tcp[10]) << 8) + int(tcp[11])
  flags = bin((int(tcp[12]) << 8) + int(tcp[13]))[2:].zfill(16)
  offset = int(flags[0:4], 2)
  ack = True if flags[11] == '1' else False
  rst = True if flags[13] == '1' else False
  syn = True if flags[14] == '1' else False
  fin = True if flags[15] == '1' else False
  window = (int(tcp[14]) << 8) + int(tcp[15])
  TCPchecksum = hex((int(tcp[16]) << 8) + int(tcp[17]))

  return {
    'ether': {
      'dest': destMac,
      'src': srcMac
    },
    'IP': {
      'ver': IPver,
      'IHL': IHL,
      'length': length,
      'ID': ID,
      'ttl': ttl,
      'proto': proto,
      'checksum': IPchecksum,
      'src': srcIP,
      'dest': destIP
    },
    'TCP': {
      'src': srcPort,
      'dest': destPort,
      'seq_num': seq_num,
      'ack_num': ack_num,
      'offset': offset,
      'ack': ack,
      'rst': rst,
      'syn': syn,
      'fin': fin,
      'window': window,
      'checksum': TCPchecksum
    }
  }

