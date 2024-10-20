from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle
from PySide6.QtCore import QThread, Qt, QEvent
from functional.voice_controller import VoiceController
from UI.main_page import MainPage
import traceback
from datetime import datetime
from page_manager import PageManager
from UI.main_window import Ui_MainWindow
import sys


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

        self.tray_icon = QSystemTrayIcon()
        self.trey_gui()

        # Создаем PageManager
        self.page_manager = PageManager()

        # Создаем страницы, которые автоматически регистрируются
        MainPage(self.page_manager)  # Регистрация страницы

        # Устанавливаем QStackedWidget в главное окно
        self.setCentralWidget(self.page_manager.stacked_widget)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMinimized:
                self.hide()

    def trey_gui(self):
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        self.tray_icon.activated.connect(self.restore_window)

        exit_action = QAction("Закрыть", self)
        exit_action.triggered.connect(self.close)

        tray_menu = QMenu()
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("Моника")
        self.tray_icon.show()

    def restore_window(self, reason):
        if reason != self.isHidden():
            self.tray_icon.show()
            self.showNormal()
        else:
            self.tray_icon.show()
            self.showNormal()

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
