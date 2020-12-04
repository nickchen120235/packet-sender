""" 
View: ARP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *

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

    localIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', localIP)

    localMAC = QLabel('Unknown')
    setupContent.addRow('Local MAC: ', localMAC)
    
    targetIP = QLineEdit()
    setupContent.addRow('Target IP: ', targetIP)

    """
    Subview: Result
    Widgets:
      srcIP: QLabel
      srcMAC: QLabel
      destIP: QLabel
      destMAC: QLabel
    """
    res = QGroupBox('Result')
    layout.addWidget(res)
    resContent = QFormLayout()
    res.setLayout(resContent)

    srcIP = QLabel()
    resContent.addRow('Source IP: ', srcIP)
    srcMAC = QLabel()
    resContent.addRow('Source MAC: ', srcMAC)
    destIP = QLabel()
    resContent.addRow('Destination IP: ', destIP)
    destMAC = QLabel()
    resContent.addRow('Destination MAC: ', destMAC)