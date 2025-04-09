import sys
from PySide6.QtWidgets import QApplication
from main_window import CurrencyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CurrencyWindow()
    window.show()
    sys.exit(app.exec()) 