""" 
View: ICMP
Widgets:
  Setup
  Result
"""

from PySide2.QtWidgets import *
import socket
import netifaces

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.icmp import ICMPInfo

from lib.packet import Ether, IPv4, ICMP, ARP
from lib.helper import Unpacker, ETH_P_IP, ETH_P_ARP, check_ip, InputCheckError

_ops = ['Echo Reply (0)', 'Echo Request (8)']

class ICMPView(QWidget):
  def __init__(self):
    self.ip = ''
    self.mac = ''
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
    self.ifaceInput = QLineEdit()
    iface.addWidget(self.ifaceInput)
    ifaceSet = QPushButton('Set')
    iface.addWidget(ifaceSet)
    setupContent.addRow('Interface: ', iface)

    self.localIP = QLabel('Unknown')
    setupContent.addRow('Local IP: ', self.localIP)

    self.tarIP = QLineEdit()
    setupContent.addRow('Target IP: ', self.tarIP)

    self.op = QComboBox()
    self.op.addItems(_ops)
    setupContent.addRow('Type: ', self.op)

    self.code = QLineEdit()
    setupContent.addRow('Code: ', self.code)

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

    self.req_ether = EtherInfo()
    reqContent.addWidget(self.req_ether)
    self.req_ipv4 = IPv4Info()
    reqContent.addWidget(self.req_ipv4)
    self.req_icmp = ICMPInfo()
    reqContent.addWidget(self.req_icmp)

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

    self.res_ether = EtherInfo()
    resContent.addWidget(self.res_ether)
    self.res_ipv4 = IPv4Info()
    resContent.addWidget(self.res_ipv4)
    self.res_icmp = ICMPInfo()
    resContent.addWidget(self.res_icmp)

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
      self.localIP.setText(self.ip)
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
    tar = self.tarIP.text()
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
      print(f'Type: [{self.op.currentIndex()}] {self.op.currentText()}')
      t = 0 if self.op.currentIndex() == 0 else 8
      icmp = ICMP().packet(t, int(self.code.text()))
      ipv4 = IPv4(self.ip, tar).packet(socket.IPPROTO_ICMP, 64, icmp)
      p = eth+ipv4+icmp
      self.req_ether.setInfo(Unpacker(p).ether())
      self.req_ipv4.setInfo(Unpacker(p).ipv4())
      self.req_icmp.setInfo(Unpacker(p).icmp())
      with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_IP)) as s:
        s.bind((self.ifaceInput.text(), 0))
        s.send(p)
        ru = Unpacker(s.recv(1024))
        self.res_ether.setInfo(ru.ether())
        self.res_ipv4.setInfo(ru.ipv4())
        self.res_icmp.setInfo(ru.icmp())

  def check_input(self):
    err = []

    if self.ip == '' or self.mac == '': err.append('Local IP (Set Interface First)')

    if check_ip(self.tarIP.text()) != True: err.append('Target IP (Not a IPv4 Address)')
    
    if self.code.text().isdecimal() != True: err.append('Code (Not a Number)')
    else:
      if int(self.code.text()) < 0: err.append('Code (Out of Range)')

    if len(err) > 0: raise InputCheckError(err)
