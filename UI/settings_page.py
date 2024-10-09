from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from page_manager import PageManager


class SettingsPage(QWidget):
    def __init__(self, page_manager):
        super().__init__()

        self.page_manager = page_manager  # Сохраняем экземпляр PageManager
        self.page_manager.register_page(self.__class__.__name__, self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
