#!/usr/bin/env python3

from lib.packet import Ether, ICMP, TCP, IPv4, ARP
from lib.helper import ETH_P_IP, ETH_P_ARP, ETH_P_ALL, Unpacker

import socket
import netifaces
from getmac import getmac

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

source = netifaces.ifaddresses('ens33')[netifaces.AF_INET][0]['addr']
sourceMac = netifaces.ifaddresses('ens33')[netifaces.AF_LINK][0]['addr']
dest = '192.168.1.106'
destMac = getmac.get_mac_address(ip=dest, network_request=True)

eth = Ether(sourceMac, destMac)
ip = IPv4(source, dest)
icmp = ICMP()

eth_p = eth.packet(ETH_P_IP)
icmp_p = icmp.packet(8, 0)
ip_p = ip.packet(socket.IPPROTO_ICMP, 64, icmp_p)

s.bind(('ens33', 0))
s.send(eth_p+ip_p+icmp_p)

u = Unpacker(eth_p+ip_p+icmp_p)
print(u.icmp())