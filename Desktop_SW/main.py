from interfaces.interface import Interface
import sys
from PyQt6.QtWidgets import QApplication

# main function of pyqt6
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec())
     