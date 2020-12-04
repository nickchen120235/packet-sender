from PySide2.QtWidgets import *

from views.ARP import ARPView

class MainView(QTabWidget):
  def __init__(self, parent = None):
    super(MainView, self).__init__(parent)
    self.tab1 = ARPView()

    self.addTab(self.tab1, 'ARP')

    self.setWindowTitle('Packet Sender')

def main():
  app = QApplication([])
  test = MainView()
  test.show()
  app.exec_()

if __name__ == '__main__': main()