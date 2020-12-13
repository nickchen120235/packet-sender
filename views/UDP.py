"""
View: UDP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *
import socket
import netifaces

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.udp import UDPInfo

from lib.packet import Ether, IPv4, UDP, ARP
from lib.helper import InputCheckError, Unpacker, ETH_P_ARP, ETH_P_IP, check_ip

class UDPView(QWidget):
  def __init__(self):
    self.ip = ''
    self.mac = ''
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
    setup.setFixedHeight(300)

    iface = QHBoxLayout()
    self.ifaceInput = QLineEdit()
    iface.addWidget(self.ifaceInput)
    ifaceSet = QPushButton('Set')
    iface.addWidget(ifaceSet)
    setupContent.addRow('Interface: ', iface)

    self.srcIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', self.srcIP)

    self.srcPort = QLineEdit()
    setupContent.addRow('Local Port: ', self.srcPort)

    self.destIP = QLineEdit()
    setupContent.addRow('Target IP: ', self.destIP)

    self.destPort = QLineEdit()
    setupContent.addRow('Target Port: ', self.destPort)

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

    self.req_ether = EtherInfo()
    reqContent.addWidget(self.req_ether)
    self.req_ipv4 = IPv4Info()
    reqContent.addWidget(self.req_ipv4)
    self.req_udp = UDPInfo()
    reqContent.addWidget(self.req_udp)

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

    self.res_ether = EtherInfo()
    resContent.addWidget(self.res_ether)
    self.res_ipv4 = IPv4Info()
    resContent.addWidget(self.res_ipv4)
    self.res_udp = UDPInfo()
    resContent.addWidget(self.res_udp)

    """
    Signals  -> Slots
    ifaceSet -> getLocalStat
    sendBtn  -> send
    """
    ifaceSet.clicked.connect(self.getLocalStat)
    self.ifaceInput.returnPressed.connect(self.getLocalStat)
    sendBtn.clicked.connect(self.send)

  # slots
  def getLocalStat(self):
    print('getLocalStat')
    print(f'ifaceInput: {self.ifaceInput.text()}')
    try:
      self.ip = netifaces.ifaddresses(self.ifaceInput.text())[netifaces.AF_INET][0]['addr']
      print(f'IP: {self.ip}')
      self.srcIP.setText(self.ip)
      self.mac = netifaces.ifaddresses(self.ifaceInput.text())[netifaces.AF_LINK][0]['addr']
      print(f'MAC: {self.mac}')
    except:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setWindowTitle('Invalid Interface')
      msg.setText(f'netifaces cannot find info of "{self.ifaceInput.text()}".')
      msg.setInformativeText('Try "ip addr" in your terminal to get a valid interface.')
      msg.exec_()
    
  def send(self):
    print('send')
    tar = self.destIP.text()
    print(f'Target IP: {tar}')
    try:
      self.check_input()
    except InputCheckError as ice:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setWindowTitle('Invalid Input')
      msg.setText('The following inputs are invalid:')
      msg.setInformativeText('\n'.join(ice.msg))
      msg.exec_()
    else:
      # getmac
      s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ARP))
      p = Ether(self.mac, 'FF:FF:FF:FF:FF:FF').packet(ETH_P_ARP)+ARP(self.ip, self.mac).packet(ETH_P_IP, tar)
      s.bind((self.ifaceInput.text(), 0))
      s.send(p)
      mac = Unpacker(s.recv(1024)).arp()['SHA']
      s.close()
      # mac ok
      print(f'Target MAC: {mac}')
      eth = Ether(self.mac, mac).packet(ETH_P_IP)
      udp = UDP(self.ip, int(self.srcPort.text()), self.destIP.text(), int(self.destPort.text())).packet()
      ip = IPv4(self.ip, self.destIP.text()).packet(socket.IPPROTO_UDP, 64, udp)
      packet = eth+ip+udp
      u = Unpacker(packet)
      self.req_ether.setInfo(u.ether())
      self.req_ipv4.setInfo(u.ipv4())
      self.req_udp.setInfo(u.udp())
      with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_IP)) as s:
        s.bind((self.ifaceInput.text(), 0))
        s.send(packet)
  def check_input(self):
    err = []

    if self.ip == '' or self.mac == '': err.append('Local IP (Set Interface First)')

    if self.srcPort.text().isdecimal() != True: err.append('Local Port (Not a Number)')
    else:
      if int(self.srcPort.text()) < 0 or int(self.srcPort.text()) > 65535: err.append('Local Port (Out of Range)')

    if check_ip(self.destIP.text()) != True: err.append('Target IP (Not a IPv4 Address)')
    
    if self.destPort.text().isdecimal() != True: err.append('Target Port (Not a Number)')
    else:
      if int(self.destPort.text()) < 0 or int(self.destPort.text()) > 65535: err.append('Target Port (Out of Range)')

    if len(err) > 0: raise InputCheckError(err)