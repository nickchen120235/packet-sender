"""
Widget: IPv4Info
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

class IPv4Info(QGroupBox):
  def __init__(self):
    super(IPv4Info, self).__init__('IPv4')
    content = QFormLayout()
    self.setLayout(content)

    self.ver = QLabel()
    content.addRow('Version: ', self.ver)
    self.ihl = QLabel()
    content.addRow('Internet Header Length: ', self.ihl)
    self.length = QLabel()
    content.addRow('Length: ', self.length)
    self.id = QLabel()
    content.addRow('ID: ', self.id)
    self.ttl = QLabel()
    content.addRow('TTL: ', self.ttl)
    self.proto = QLabel()
    content.addRow('Protocol: ', self.proto)
    self.checksum = QLabel()
    content.addRow('Checksum: ', self.checksum)
    self.src = QLabel()
    content.addRow('Source IP: ', self.src)
    self.dest = QLabel()
    content.addRow('Destination IP: ', self.dest)

  def setInfo(self, ip: dict):
    self.ver.setText(ip['ver'])
    self.ihl.setText(ip['IHL'])
    self.length.setText(ip['length'])
    self.id.setText(ip['ID'])
    self.ttl.setText(ip['ttl'])
    self.proto.setText(ip['protocol'])
    self.checksum.setText(ip['checksum'])
    self.src.setText(ip['src'])
    self.dest.setText(ip['dest'])
