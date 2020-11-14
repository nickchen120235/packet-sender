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
  print('header: {}'.format(header))
  print('source: {}'.format(source))
  print('dest: {}'.format(dest))
  print('arr: {}'.format(arr))
  sum = 0

  for i in range(0, len(arr), 2):
    print('*****************************')
    sum += (arr[i] << 8) + arr[i+1]
    print('[{}]: {}'.format(i, arr[i]))
    print('[{}]: {}'.format(i+1, arr[i+1]))
    print('sum = {}'.format(hex(sum)))
  
  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def tcp_checksum(header: bytearray, source: bytearray, dest: bytearray) -> bytearray:
  arr = [n for n in (header+source+dest)]
  print('header: {}'.format(header))
  print('arr: {}'.format(arr))
  sum = 0

  sum += 26
  for i in range(0, len(arr), 2):
    print('*****************************')
    sum += (arr[i] << 8) + arr[i+1]
    print('[{}]: {}'.format(i, arr[i]))
    print('[{}]: {}'.format(i+1, arr[i+1]))
    print('sum = {}'.format(hex(sum)))

  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def tcp_packet(source_port: int, dest_port: int, source_ip: str, dest_ip: str, seq_num: int, ack_num: int, ack: bool=False, rst: bool=False, syn: bool=False, fin: bool=False) -> bytearray:
  source = bytearray.fromhex('{0:#0{1}x}'.format(source_port, 6)[2:])
  print(f'source: {source}')
  dest = bytearray.fromhex('{0:#0{1}x}'.format(dest_port, 6)[2:])
  print(f'dest: {dest}')
  seq_arr = bytearray.fromhex('{0:#0{1}x}'.format(seq_num, 10)[2:])
  print(f'seq_arr: {seq_arr}')
  ack_arr = bytearray.fromhex('{0:#0{1}x}'.format(ack_num, 10)[2:])
  print(f'ack_arr: {ack_arr}')
  flag = '0b01010000000' + ('1' if ack else '0') + '0' + ('1' if rst else '0') + ('1' if syn else '0') + ('1' if fin else '0')
  print(f'flag: {flag} (ack: {ack}, rst: {rst}, syn: {syn}, fin: {fin})')
  flag_arr = bytearray.fromhex(hex(int(flag, 2))[2:])
  print(f'flag_arr: {flag_arr}')
  window = b'\x71\x10'
  print(f'window: {window}')
  checksum = tcp_checksum(source+dest+seq_arr+ack_arr+flag_arr+window, ipToBytearray(source_ip), ipToBytearray(dest_ip))
  print(f'checksum: {checksum}')
  packet = source+dest+seq_arr+ack_arr+flag_arr+window+checksum+b'\x00\x00'
  print(f'packet: {packet}, length: {len(packet)}')
  return packet

def ipv4_packet(protocol: int, ttl: int, source_ip: str, dest_ip: str) -> bytearray:
  header = b'\x45\x00\x00\x28\xab\xcd\x00\x00' # ver | IHL | ToS | len | ID | flags | frag offest
  source = ipToBytearray(source_ip)
  print(f'source: {source}')
  dest = ipToBytearray(dest_ip)
  print(f'dest: {dest}')
  pro_arr = bytearray.fromhex('{0:#0{1}x}'.format(protocol, 4)[2:])
  print(f'pro_arr: {pro_arr}')
  ttl_arr = bytearray.fromhex('{0:#0{1}x}'.format(ttl, 4)[2:])
  print(f'ttl_arr: {ttl_arr}')
  checksum = ip_checksum(header+ttl_arr+pro_arr, source, dest)
  print(f'checksum: {checksum}')
  packet = header+ttl_arr+pro_arr+checksum+source+dest
  print(f'packet: {packet}, length: {len(packet)}')
  return packet

def macToBytearray(mac: str) -> bytearray:
  return bytearray.fromhex(mac.replace(':', ''))

def ether_packet(dest_mac: str,src_mac: str) -> bytearray:
  return macToBytearray(dest_mac)+macToBytearray(src_mac)+b'\x08\x00'

def unpackage(arr: bytearray) -> dict:
  ether = arr[0:14]
  print(f'ether: {ether}')
  destMac = ether[0:6].hex(':')
  print(f'destMac: {destMac}')
  srcMac = ether[6:12].hex(':')
  print(f'srcMac: {srcMac}\n')
  

  ip = arr[14:34]
  print(f'ip: {ip}')
  IPver = int(ip[0]) >> 4
  print(f'IPver: {IPver}')
  IHL = int(ip[0]) - (IPver << 4)
  print(f'IHL: {IHL}')
  length = (int(ip[2]) << 8) + int(ip[3])
  print(f'Length: {length}')
  ID = hex((int(ip[4]) << 8) + int(ip[5]))
  print(f'ID: {ID}')
  ttl = int(ip[8])
  print(f'TTL: {ttl}')
  proto = int(ip[9])
  print(f'protocol: {proto}')
  IPchecksum = hex((int(ip[10]) << 8) + int(ip[11]))
  print(f'IPchecksum: {IPchecksum}')
  srcIP = f'{int(ip[12])}.{int(ip[13])}.{int(ip[14])}.{int(ip[15])}'
  print(f'srcIP: {srcIP}')
  destIP = f'{int(ip[16])}.{int(ip[17])}.{int(ip[18])}.{int(ip[19])}'
  print(f'destIP: {destIP}\n')

  tcp = arr[34:54]
  print(f'tcp: {tcp}')
  srcPort = (int(tcp[0]) << 8) + int(tcp[1])
  print(f'srcPort: {srcPort}')
  destPort = (int(tcp[2]) << 8) + int(tcp[3])
  print(f'destPort: {destPort}')
  seq_num = (int(tcp[4]) << 24) + (int(tcp[5]) << 16) + (int(tcp[6]) << 8) + int(tcp[7])
  print(f'seq_num: {seq_num}')
  ack_num = (int(tcp[8]) << 24) + (int(tcp[9]) << 16) + (int(tcp[10]) << 8) + int(tcp[11])
  print(f'ack_num: {ack_num}')
  flags = bin((int(tcp[12]) << 8) + int(tcp[13]))[2:].zfill(16)
  offset = int(flags[0:4], 2)
  print(f'offset: {offset} ({flags[0:4]})')
  ack = True if flags[11] == '1' else False
  print(f'ack: {ack}')
  rst = True if flags[13] == '1' else False
  print(f'rst: {rst}')
  syn = True if flags[14] == '1' else False
  print(f'syn: {syn}')
  fin = True if flags[15] == '1' else False
  print(f'fin: {fin}')
  window = (int(tcp[14]) << 8) + int(tcp[15])
  print(f'window: {window}')
  TCPchecksum = hex((int(tcp[16]) << 8) + int(tcp[17]))
  print(f'TCPchecksum: {TCPchecksum}')

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
def udp_checksum(header: bytearray, source: bytearray, dest: bytearray) -> bytearray:
  arr = [n for n in (header+source+dest)]
  print('header: {}'.format(header))
  print('source: {}'.format(source))
  print('dest: {}'.format(dest))
  print('arr: {}'.format(arr))
  sum = 0

  sum += 8 # UDP Length
  sum += 17 # IPPROTO_UDP
  for i in range(0, len(arr), 2):
    print('*****************************')
    sum += (arr[i] << 8) + arr[i+1]
    print('[{}]: {}'.format(i, arr[i]))
    print('[{}]: {}'.format(i+1, arr[i+1]))
    print('sum = {}'.format(hex(sum)))
  carry = int(hex(sum)[:-4], 16)
  check = 0xffff - (int(hex(sum)[-4:], 16) + carry)
  return bytearray.fromhex(hex(check)[-4:])

def udp_packet(source_port: int, dest_port: int, source_ip: str, dest_ip: str) -> bytearray:
  source = bytearray.fromhex('{0:#0{1}x}'.format(source_port, 6)[2:])
  print(f'source: {source}')
  dest = bytearray.fromhex('{0:#0{1}x}'.format(dest_port, 6)[2:])
  print(f'dest: {dest}')
  length = b'\x00\x08'
  checksum = udp_checksum(source+dest+length, ipToBytearray(source_ip), ipToBytearray(dest_ip))
  print(f'checksum: {checksum}')
  packet = source + dest + length + checksum
  print(f'packet: {packet}, length: {len(packet)}')
  return packet