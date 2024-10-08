import sys
from PyQt5.QtWidgets import QApplication
from UI.main_page import MonicaUI
import traceback
from datetime import datetime

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        window = MonicaUI()
        window.resize(800, 600)
        window.setWindowTitle('Monica Assistant')
        window.setStyleSheet("background-color: rgb(36, 19, 59);")
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        with open("error_log.txt", "a", encoding='utf-8') as f:
            f.write(f"Время ошибки: {datetime.now()}\n")

            f.write(f"Тип ошибки: {type(e).__name__}\n")

            f.write(f"Аргументы ошибки: {e.args}\n")

            f.write("Полный traceback:\n")
            traceback.print_exc(file=f)

            f.write("\n" + "-" * 50 + "\n")
