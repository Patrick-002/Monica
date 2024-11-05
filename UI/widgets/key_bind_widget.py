from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QSize


class KeyWidget(QWidget):

    def __init__(self, key, key_combination, on_key_combination_clicked, parent=None):
        super().__init__(parent)
        self.key = key
        self.key_combination = key_combination
        self.on_key_combination_clicked = on_key_combination_clicked

        # Основной layout
        
        layout = QHBoxLayout()

        # Лейбл для отображения ключа
        self.key_label = QLabel(self.key)
        layout.addWidget(self.key_label)

        # Добавляем спейсер для выравнивания
        layout.addStretch()

        # Преобразуем список комбинаций в строку
        key_combination_text = ", ".join(self.key_combination)

        # Кнопка для отображения комбинации клавиш
        self.key_button = QPushButton(key_combination_text)
        self.key_button.setMinimumSize(QSize(120, 40))
        self.key_button.clicked.connect(self.on_button_click)
        layout.addWidget(self.key_button)

        self.setLayout(layout)

    def on_button_click(self):
        """Вызываем функцию для запоминания нажатых клавиш."""
        self.on_key_combination_clicked(self.key)
