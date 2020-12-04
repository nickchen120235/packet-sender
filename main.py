import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

def window():
  app = QApplication(sys.argv)
  widget = QWidget()

  text = QLabel(widget)
  text.setText('Hello World!')
  text.move(110, 85)

  widget.setGeometry(50, 50, 320, 200)
  widget.setWindowTitle('Test')
  widget.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  window()