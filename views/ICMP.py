""" 
View: ICMP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.icmp import ICMPInfo

_ops = ['Echo Reply (0)', 'Echo Request (8)']

class ICMPView(QWidget):
  def __init__(self):
    super(ICMPView, self).__init__()
    layout = QVBoxLayout()
    self.setLayout(layout)

    """
    Subview: Setup
    Widgets: 
      iface: QLineEdit + QPushButton
      localIP: QLabel
      tarIP: QLineEdit
      op: QComboBox
      code: QLineEdit
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

    localIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', localIP)

    tarIP = QLineEdit()
    setupContent.addRow('Target IP: ', tarIP)

    op = QComboBox()
    op.addItems(_ops)
    setupContent.addRow('Type: ', op)

    code = QLineEdit()
    setupContent.addRow('Code: ', code)

    sendBtn = QPushButton('Send')
    setupContent.addWidget(sendBtn)

    """Subview: Request
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      icmp: QGroupBox
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
    req_icmp = ICMPInfo()
    reqContent.addWidget(req_icmp)

    """Subview: Result
    Widgets:
      ether: QGroupBox
      ip: QGroupBox
      icmp: QGroupBox
    """
    res = QGroupBox('Result')
    layout.addWidget(res)
    resContent = QHBoxLayout()
    res.setLayout(resContent)
    res.setFixedHeight(300)

    res_ether = EtherInfo()
    resContent.addWidget(res_ether)
    res_ipv4 = IPv4Info()
    resContent.addWidget(res_ipv4)
    res_icmp = ICMPInfo()
    resContent.addWidget(res_icmp)
