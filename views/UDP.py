"""
View: UDP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *

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
    """
    setup = QGroupBox('Setup')
    layout.addWidget(setup)
    setupContent = QFormLayout()
    setup.setLayout(setupContent)

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
    setupContent.addRow('Destination IP: ', destIP)

    destPort = QLineEdit()
    setupContent.addRow('Local Port: ', destPort)

    sendBtn = QPushButton('Send')
    setupContent.addWidget(sendBtn)

    """
    Subview: Result
    Widgets:
      checksum: QLabel
    """
    res = QGroupBox('Result')
    layout.addWidget(res)
    resContent = QFormLayout()
    res.setLayout(resContent)

    checksum = QLabel('Unknown')
    resContent.addRow('Checksum: ', checksum)
