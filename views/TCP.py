"""
View: TCP
Widgets:
  Setup
  Request
  Response
"""

from PySide2.QtWidgets import *

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.tcp import TCPInfo

class TCPView(QWidget):
  def __init__(self):
    super(TCPView, self).__init__()
    layout = QVBoxLayout()
    self.setLayout(layout)

    """
    Subview: Setup
    Widgets:
      iface: QLineEdit + QPushButton
      srcIP: QLabel
      srcPort: QLineEdit
      destIP: QLineEdit
      destPort: QLineEdit
      seq_num: QLineEdit
      ack_num: QLineEdit
      flags: QChackBox x 4
      sendBtn: QPushButton
    """
    setup = QGroupBox('Setup')
    layout.addWidget(setup)
    setupContent = QFormLayout()
    setup.setLayout(setupContent)
    setup.setFixedHeight(300)

    iface = QHBoxLayout()
    ifaceInput = QLineEdit()
    iface.addWidget(ifaceInput)
    ifaceSet = QPushButton('Set')
    iface.addWidget(ifaceSet)
    setupContent.addRow('Interface: ', iface)

    srcIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', srcIP)

    srcPort = QLineEdit()
    setupContent.addRow('Local Port: ', srcPort)

    destIP = QLineEdit()
    setupContent.addRow('Target IP: ', destIP)

    destPort = QLineEdit()
    setupContent.addRow('Target Port: ', destPort)

    seq_num = QLineEdit()
    setupContent.addRow('Sequence Number: ', seq_num)
    ack_num = QLineEdit()
    setupContent.addRow('Acknowledgement Number: ', ack_num)

    flags = QHBoxLayout()
    ack = QCheckBox('ACK')
    flags.addWidget(ack)
    rst = QCheckBox('RST')
    flags.addWidget(rst)
    syn = QCheckBox('SYN')
    flags.addWidget(syn)
    fin = QCheckBox('FIN')
    flags.addWidget(fin)
    setupContent.addRow('Flags: ', flags)

    sendBtn = QPushButton('Send')
    setupContent.addWidget(sendBtn)

    """Subview: Request
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      tcp: QGroupBox
    """
    req = QGroupBox('Request')
    layout.addWidget(req)
    reqContent = QHBoxLayout()
    req.setLayout(reqContent)
    req.setFixedHeight(300)

    req_ether = EtherInfo()
    reqContent.addWidget(req_ether)
    req_ipv4 = IPv4Info()
    reqContent.addWidget(req_ipv4)
    req_tcp = TCPInfo()
    reqContent.addWidget(req_tcp)

    """Subview: Response
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      tcp: QGroupBox
    """
    res = QGroupBox('Response')
    layout.addWidget(res)
    resContent = QHBoxLayout()
    res.setLayout(resContent)
    res.setFixedHeight(300)

    res_ether = EtherInfo()
    resContent.addWidget(res_ether)
    res_ipv4 = IPv4Info()
    resContent.addWidget(res_ipv4)
    res_tcp = TCPInfo()
    resContent.addWidget(res_tcp)