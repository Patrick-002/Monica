from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread
import sys_commands
from voice_controller import VoiceController
from UI.main_page import SettingsPage
import traceback
from datetime import datetime
import sys
from page_manager import PageManager
from UI.main_window import Ui_MainWindow


# Класс для работы с VoiceController в отдельном потоке
class VoiceThread(QThread):
    def __init__(self):
        super().__init__()
        self.voice_controller = VoiceController()

    def run(self):
        self.voice_controller.start()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создаем PageManager
        self.page_manager = PageManager()

        # Создаем страницы, которые автоматически регистрируются
        SettingsPage(self.page_manager)  # Регистрация страницы

        # Устанавливаем QStackedWidget в главное окно
        self.setCentralWidget(self.page_manager.stacked_widget)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        # Создаем и запускаем поток для VoiceController
        voice_thread = VoiceThread()
        voice_thread.start()

        # Запуск основного цикла приложения
        sys.exit(app.exec())

    except Exception as e:
        with open("error_log.txt", "a", encoding='utf-8') as f:
            f.write(f"Время ошибки: {datetime.now()}\n")
            f.write(f"Тип ошибки: {type(e).__name__}\n")
            f.write(f"Аргументы ошибки: {e.args}\n")
            f.write("Полный traceback:\n")
            traceback.print_exc(file=f)
            f.write("\n" + "-" * 50 + "\n")
