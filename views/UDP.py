"""
View: UDP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.udp import UDPInfo

class UDPView(QWidget):
  def __init__(self):
    super(UDPView, self).__init__()
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
      sendBtn: QPushButton
    """
    setup = QGroupBox('Setup')
    layout.addWidget(setup)
    setupContent = QFormLayout()
    setup.setLayout(setupContent)
    setup.setFixedHeight(200)

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

    sendBtn = QPushButton('Send')
    setupContent.addWidget(sendBtn)

    """Subview: Request
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      udp: QGroupBox
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
    req_udp = UDPInfo()
    reqContent.addWidget(req_udp)

    """Subview: Response
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      udp: QGroupBox
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
    res_udp = UDPInfo()
    resContent.addWidget(res_udp)
