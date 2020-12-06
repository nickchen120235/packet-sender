""" 
View: ARP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *
import socket

from views.widgets.info.ether import EtherInfo
from views.widgets.info.arp import ARPInfo

from lib.packet import Ether, ARP
from lib.helper import ETH_P_ARP, Unpacker, ETH_P_IP

import netifaces

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
    self.ifaceInput = QLineEdit()
    iface.addWidget(self.ifaceInput)
    ifaceSet = QPushButton('Set')
    iface.addWidget(ifaceSet)
    setupContent.addRow('Interface: ', iface)

    self.localIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', self.localIP)

    self.localMAC = QLabel('Unknown')
    setupContent.addRow('Local MAC: ', self.localMAC)
    
    self.targetIP = QLineEdit()
    setupContent.addRow('Target IP: ', self.targetIP)

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

    self.req_ether = EtherInfo()
    reqContent.addWidget(self.req_ether)
    self.req_arp = ARPInfo()
    reqContent.addWidget(self.req_arp)

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

    self.res_ether = EtherInfo()
    resContent.addWidget(self.res_ether)
    self.res_arp = ARPInfo()
    resContent.addWidget(self.res_arp)

    """
    Signals  -> Slots
    ifaceSet -> getLocalStat
    sendBtn  -> send
    """
    ifaceSet.clicked.connect(self.getLocalStat)
    sendBtn.clicked.connect(self.send)
    
  # slots
  def getLocalStat(self): # ifaceSet
    print('getLocalStat')
    print(f'ifaceInput: {self.ifaceInput.text()}')
    try:
      self.ip = netifaces.ifaddresses(self.ifaceInput.text())[netifaces.AF_INET][0]['addr']
      print(f'IP: {self.ip}')
      self.localIP.setText(self.ip)
      self.mac = netifaces.ifaddresses(self.ifaceInput.text())[netifaces.AF_LINK][0]['addr']
      print(f'MAC: {self.mac}')
      self.localMAC.setText(self.mac)
    except:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setWindowTitle('Invalid Interface')
      msg.setText(f'netifaces cannot find info of "{self.ifaceInput.text()}".')
      msg.setInformativeText('Try "ip addr" in your terminal to get a valid interface.')
      msg.exec_()

  def send(self): # sendBtn
    print('send')
    tar = self.targetIP.text()
    print(f'Target: {tar}')
    eth = Ether(self.mac, 'FF:FF:FF:FF:FF:FF').packet(ETH_P_ARP)
    arp = ARP(self.ip, self.mac).packet(ETH_P_IP, tar)
    packet = eth+arp
    u = Unpacker(packet)
    self.req_ether.setInfo(u.ether())
    self.req_arp.setInfo(u.arp())
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ARP)) as s:
      s.bind((self.ifaceInput.text(), 0))
      s.send(packet)
      r = s.recv(1024)
      ru = Unpacker(r)
      self.res_ether.setInfo(ru.ether())
      self.res_arp.setInfo(ru.arp())
