"""
Widget: EtherInfo
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

class EtherInfo(QGroupBox):
  def __init__(self):
    super(EtherInfo, self).__init__('Ethernet')
    content = QFormLayout()
    self.setLayout(content)

    self.src = QLabel()
    content.addRow('Source MAC: ', self.src)
    self.dest = QLabel()
    content.addRow('Destination MAC: ', self.dest)
    self.proto = QLabel()
    content.addRow('Protocol: ', self.proto)

  def setInfo(self, ether: dict):
    self.src.setText(ether['src'])
    self.dest.setText(ether['dest'])
    self.proto.setText(ether['proto'])
