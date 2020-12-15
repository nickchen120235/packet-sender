"""
Widget: ARPInfo
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

class ARPInfo(QGroupBox):
  def __init__(self):
    super(ARPInfo, self).__init__('ARP')
    content = QFormLayout()
    self.setLayout(content)

    self.HTYPE = QLabel()
    content.addRow('Hardware Type: ', self.HTYPE)
    self.PTYPE = QLabel()
    content.addRow('Protocol Type: ', self.PTYPE)
    self.HLEN = QLabel()
    content.addRow('Hardware Address Length: ', self.HLEN)
    self.PLEN = QLabel()
    content.addRow('Protocol Address Length: ', self.PLEN)
    self.OP = QLabel()
    content.addRow('Operation: ', self.OP)
    self.SHA = QLabel()
    content.addRow('Source MAC: ', self.SHA)
    self.SPA = QLabel()
    content.addRow('Source IP: ', self.SPA)
    self.THA = QLabel()
    content.addRow('Destination MAC: ', self.THA)
    self.TPA = QLabel()
    content.addRow('Destination IP: ', self.TPA)

  def setInfo(self, arp: dict):
    self.HTYPE.setText(str(arp['HTYPE']) + ' (' + ('Ethernet' if arp['HTYPE'] == 1 else 'Unknown') + ')')
    self.PTYPE.setText(arp['PTYPE'] + ' (' + ('IPv4' if arp['PTYPE'] == '0x0800' else ('ARP' if arp['PTYPE'] == '0x0806' else 'Unknown')) + ')')
    self.HLEN.setText(str(arp['HLEN']))
    self.PLEN.setText(str(arp['PLEN']))
    self.OP.setText(str(arp['OP']) + ' (' + ('request' if arp['OP'] == 1 else ('response' if arp['OP'] == 2 else 'Unknown')) + ')')
    self.SHA.setText(arp['SHA'])
    self.SPA.setText(arp['SPA'])
    self.THA.setText(arp['THA'])
    self.TPA.setText(arp['TPA'])
