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