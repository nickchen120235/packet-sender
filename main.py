from PySide2.QtWidgets import *

from views.ARP import ARPView
from views.UDP import UDPView

class MainView(QTabWidget):
  def __init__(self, parent = None):
    super(MainView, self).__init__(parent)
    self.tab1 = ARPView()
    self.tab3 = UDPView()

    self.addTab(self.tab1, 'ARP')
    self.addTab(self.tab3, 'UDP')

    self.setWindowTitle('Packet Sender')

def main():
  app = QApplication([])
  test = MainView()
  test.show()
  app.exec_()

if __name__ == '__main__': main()