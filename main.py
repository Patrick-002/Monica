import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from UI.main_page import MainPage
from UI.settings_page import SettingsPage
import traceback
from datetime import datetime
import sys
from page_manager import PageManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаем PageManager
        self.page_manager = PageManager()

        # Создаем страницы, которые автоматически регистрируются
        MainPage(self.page_manager)  # Регистрация MainPage
        SettingsPage(self.page_manager)  # Регистрация SecondPage

        # Устанавливаем QStackedWidget в главное окно
        self.setCentralWidget(self.page_manager.stacked_widget)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        window.resize(800, 600)
        window.setStyleSheet("background-color: rgb(36, 19, 59);")
        window.setWindowTitle('Monica Assistant')
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
