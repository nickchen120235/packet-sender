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

