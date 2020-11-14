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