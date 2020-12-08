"""
Widget: ICMPInfo
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout, QTextBrowser

class ICMPInfo(QGroupBox):
  def __init__(self):
    super(ICMPInfo, self).__init__('ICMP')
    content = QFormLayout()
    self.setLayout(content)

    self.TYPE = QLabel()
    content.addRow('Type: ', self.TYPE)
    self.CODE = QLabel()
    content.addRow('Code: ', self.CODE)
    self.checksum = QLabel()
    content.addRow('Checksum: ', self.checksum)
    self.DATA = QTextBrowser()
    content.addRow('Data: ', self.DATA)

  def setInfo(self, icmp: dict):
    self.TYPE.setText(str(icmp['TYPE']))
    self.CODE.setText(str(icmp['CODE']))
    self.checksum.setText(icmp['checksum'])
    self.DATA.setText(icmp['DATA'])