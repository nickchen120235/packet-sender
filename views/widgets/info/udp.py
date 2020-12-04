"""
Widget: UDPInfo
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

class UDPInfo(QGroupBox):
  def __init__(self):
    super(UDPInfo, self).__init__('UDP')
    content = QFormLayout()
    self.setLayout(content)

    self.src = QLabel()
    content.addRow('Source Port: ', self.src)
    self.dest = QLabel()
    content.addRow('Destination Port: ', self.dest)
    self.length = QLabel()
    content.addRow('Length: ', self.length)
    self.checksum = QLabel()
    content.addRow('Checksum: ', self.checksum)

  def setInfo(self, udp: dict):
    self.src.setText(udp['srcPort'])
    self.dest.setText(udp['destPort'])
    self.length.setText(udp['length'])
    self.checksum.setText(udp['checksum'])