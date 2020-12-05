""" 
View: ARP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *

from views.widgets.info.ether import EtherInfo
from views.widgets.info.arp import ARPInfo

class ARPView(QWidget):
  def __init__(self):
    super(ARPView, self).__init__()
    layout = QVBoxLayout()
    self.setLayout(layout)

    """
    Subview: Setup
    Widgets: 
      iface: QLineEdit + QPushButton
      localIP: QLabel
      localMAC: QLabel
      targetIP: QLineEdit
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

    localMAC = QLabel('Unknown')
    setupContent.addRow('Local MAC: ', localMAC)
    
    targetIP = QLineEdit()
    setupContent.addRow('Target IP: ', targetIP)

    sendBtn = QPushButton('Send')
    setupContent.addWidget(sendBtn)

    """
    Subview: Request
    Widgets:
      ether: QGroupBox
      arp: QGroupBox
    """
    req = QGroupBox('Request')
    layout.addWidget(req)
    reqContent = QHBoxLayout()
    req.setLayout(reqContent)
    req.setFixedHeight(300)

    req_ether = EtherInfo()
    reqContent.addWidget(req_ether)
    req_arp = ARPInfo()
    reqContent.addWidget(req_arp)

    """
    Subview: Result
    Widgets:
      srcIP: QLabel
      srcMAC: QLabel
      destIP: QLabel
      destMAC: QLabel
    """
    res = QGroupBox('Response')
    layout.addWidget(res)
    resContent = QHBoxLayout()
    res.setLayout(resContent)
    res.setFixedHeight(300)

    res_ether = EtherInfo()
    resContent.addWidget(res_ether)
    res_arp = ARPInfo()
    resContent.addWidget(res_arp)
    