import sys
from PyQt5.QtWidgets import QApplication
from UI.main_page import MonicaUI

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MonicaUI()
    window.resize(800, 600)
    window.setWindowTitle('Monica Assistant')
    window.setStyleSheet("background-color: rgb(36, 19, 59);")
    window.show()

    sys.exit(app.exec_())
