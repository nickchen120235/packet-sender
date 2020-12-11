"""
Widget: TCPInfo
Type: QGroupBox
"""

from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

class TCPInfo(QGroupBox):
  def __init__(self):
    super(TCPInfo, self).__init__('TCP')
    content = QFormLayout()
    self.setLayout(content)

    self.src = QLabel()
    content.addRow('Source Port: ', self.src)
    self.dest = QLabel()
    content.addRow('Destination Port: ', self.dest)
    self.seq_num = QLabel()
    content.addRow('Sequence Number: ', self.seq_num)
    self.ack_num = QLabel()
    content.addRow('Acknowledgement Number: ', self.ack_num)
    self.offset = QLabel()
    content.addRow('Offset: ', self.offset)
    self.flag = QLabel()
    content.addRow('Flag: ', self.flag)
    self.windowSize = QLabel()
    content.addRow('Window Size: ', self.windowSize)
    self.checksum = QLabel()
    content.addRow('Checksum: ', self.checksum)

  def setInfo(self, tcp: dict):
    self.src.setText(str(tcp['srcPort']))
    self.dest.setText(str(tcp['destPort']))
    self.seq_num.setText(str(tcp['seq_num']))
    self.ack_num.setText(str(tcp['ack_num']))
    self.offset.setText(str(tcp['offset']))
    f  = 'ACK ' if tcp['ack'] else ''
    f += 'RST ' if tcp['rst'] else ''
    f += 'SYN ' if tcp['syn'] else ''
    f += 'FIN ' if tcp['fin'] else ''
    self.flag.setText(f)
    self.windowSize.setText(str(tcp['window']))
    self.checksum.setText(tcp['checksum'])
