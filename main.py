from PySide2.QtWidgets import *

from views.ARP import ARPView
from views.TCP import TCPView
from views.UDP import UDPView
from views.ICMP import ICMPView

class MainView(QMainWindow):
  def __init__(self, parent = None):
    super(MainView, self).__init__(parent)
    tab = QTabWidget()
    self.setCentralWidget(tab)
    tab1 = ARPView()
    tab2 = TCPView()
    tab3 = UDPView()
    tab4 = ICMPView()

    tab.addTab(tab1, 'ARP')
    tab.addTab(tab2, 'TCP')
    tab.addTab(tab3, 'UDP')
    tab.addTab(tab4, 'ICMP')

    self.setWindowTitle('Packet Sender')

def main():
  app = QApplication([])
  test = MainView()
  test.setFixedSize(1000, 950)
  test.show()
  app.exec_()

if __name__ == '__main__': main()