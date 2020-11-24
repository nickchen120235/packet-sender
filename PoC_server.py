import socket
from packet import Ether, IPv4, TCP
from helper import ETH_P_ALL, ETH_P_IP, Unpacker

PORT = 20000

with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL)):
  s.bind(('eth0', PORT))
  s.listen(1)
  conn, addr = s.accept()
  with conn:
    while True:
     data = conn.recv(1024)
     if not data: break
     conn.sendall(data)