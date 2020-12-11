"""
View: TCP
Widgets:
  Setup
  Request
  Response
"""

from PySide2.QtWidgets import *
import socket 
import netifaces

from views.widgets.info.ether import EtherInfo
from views.widgets.info.ipv4 import IPv4Info
from views.widgets.info.tcp import TCPInfo

from lib.packet import Ether, IPv4, TCP, ARP
from lib.helper import Unpacker, ETH_P_ARP, ETH_P_IP

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

    self.seq_num = QLineEdit()
    setupContent.addRow('Sequence Number: ', self.seq_num)
    self.ack_num = QLineEdit()
    setupContent.addRow('Acknowledgement Number: ', self.ack_num)

    flags = QHBoxLayout()
    self.ack = QCheckBox('ACK')
    flags.addWidget(self.ack)
    self.rst = QCheckBox('RST')
    flags.addWidget(self.rst)
    self.syn = QCheckBox('SYN')
    flags.addWidget(self.syn)
    self.fin = QCheckBox('FIN')
    flags.addWidget(self.fin)
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

    self.req_ether = EtherInfo()
    reqContent.addWidget(self.req_ether)
    self.req_ipv4 = IPv4Info()
    reqContent.addWidget(self.req_ipv4)
    self.req_tcp = TCPInfo()
    reqContent.addWidget(self.req_tcp)

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

    self.res_ether = EtherInfo()
    resContent.addWidget(self.res_ether)
    self.res_ipv4 = IPv4Info()
    resContent.addWidget(self.res_ipv4)
    self.res_tcp = TCPInfo()
    resContent.addWidget(self.res_tcp)

    """
    Signals  -> Slots
    ifaceSet -> getLocalStat
    sendBtn  -> send
    """
    ifaceSet.clicked.connect(self.getLocalStat)
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
    tcp = TCP(self.ip, int(self.srcPort.text()), self.destIP.text(), int(self.destPort.text())).packet(int(self.seq_num.text()), int(self.ack_num.text()), self.ack.isChecked(), self.rst.isChecked(), self.syn.isChecked(), self.fin.isChecked())
    ip = IPv4(self.ip, self.destIP.text()).packet(socket.IPPROTO_TCP, 64, tcp)
    packet = eth+ip+tcp
    u = Unpacker(packet)
    self.req_ether.setInfo(u.ether())
    self.req_ipv4.setInfo(u.ipv4())
    self.req_tcp.setInfo(u.tcp())
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_IP)) as s:
      s.bind((self.ifaceInput.text(), 0))
      s.send(packet)
      ru = Unpacker(s.recv(1024))
      self.res_ether.setInfo(ru.ether())
      self.res_ipv4.setInfo(ru.ipv4())
      self.res_tcp.setInfo(ru.tcp())