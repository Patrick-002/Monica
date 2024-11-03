from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class KeywordSpoiler(QWidget):
    del_ico = 'res/icon-delete.png'
    def __init__(self, key, keywords, rebind_func, add_func, parent=None):
        super().__init__(parent)
        self.key = key
        self.keywords = keywords
        self.rebind_func = rebind_func
        self.add_func = add_func

        # Основной макет для спойлера
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Кнопка для открытия/закрытия спойлера
        self.toggle_button = QPushButton(key)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setIcon(QIcon("res/arrow_right.png"))  # Иконка со стрелкой вправо
        self.toggle_button.clicked.connect(self.toggle_content)
        self.main_layout.addWidget(self.toggle_button)

        # Виджет-контейнер для содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setLayout(self.content_layout)
        self.content_widget.setVisible(False)
        self.main_layout.addWidget(self.content_widget)

        # Добавление LineEdit и кнопки удаления для каждого ключевого слова в две колонки
        for index, keyword in enumerate(keywords):
            keyword_layout = QHBoxLayout()

            keyword_line = QLineEdit()
            keyword_line.setText(keyword)
            keyword_line.setPlaceholderText(keyword)  # Устанавливаем placeholder с текущим значением
            keyword_line.textChanged.connect(
                lambda text, idx=index: self.rebind_func(self.key, text, idx)
            )

            # Кнопка для удаления ключевого слова
            delete_button = QPushButton()
            delete_button.setIcon(QIcon(self.del_ico))  # Путь к иконке удаления
            delete_button.setFixedSize(QSize(40, 40))
            delete_button.clicked.connect(lambda _, idx=index: self.delete_keyword(idx))

            keyword_layout.addWidget(keyword_line)
            keyword_layout.addWidget(delete_button)
            self.content_layout.addLayout(keyword_layout)

        # Поле для ввода нового ключевого слова
        self.new_keyword_line = QLineEdit()
        self.new_keyword_line.setPlaceholderText("Добавить новое ключевое слово")
        self.content_layout.addWidget(self.new_keyword_line)

        # Кнопка для добавления нового ключевого слова
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_new_keyword)
        self.content_layout.addWidget(self.add_button)

    def toggle_content(self):
        """Показать/скрыть содержимое спойлера и изменить иконку."""
        is_checked = self.toggle_button.isChecked()
        self.content_widget.setVisible(is_checked)
        arrow_icon = "res/arrow_down.png" if is_checked else "res/arrow_right.png"
        self.toggle_button.setIcon(QIcon(arrow_icon))

    def add_new_keyword(self):
        """Добавить новое ключевое слово в словарь и обновить UI."""
        new_keyword = self.new_keyword_line.text().strip()
        if new_keyword:
            self.add_func(self.key, new_keyword)
            keyword_layout = QHBoxLayout()

            new_keyword_line = QLineEdit(new_keyword)
            new_keyword_line.setPlaceholderText(new_keyword)  # Устанавливаем placeholder для нового слова
            new_keyword_line.textChanged.connect(
                lambda text, idx=len(self.keywords): self.rebind_func(self.key, text, idx)
            )

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(self.del_ico))  # Иконка для кнопки удаления
            delete_button.setFixedSize(QSize(40, 40))
            delete_button.clicked.connect(lambda _, idx=len(self.keywords): self.delete_keyword(idx))

            keyword_layout.addWidget(new_keyword_line)
            keyword_layout.addWidget(delete_button)
            self.content_layout.insertLayout(self.content_layout.count() - 2, keyword_layout)

            self.keywords.append(new_keyword)
            self.new_keyword_line.clear()

    def delete_keyword(self, idx):
        """Удалить ключевое слово из словаря и обновить UI."""
        if 0 <= idx < len(self.keywords):
            del self.keywords[idx]
            self.rebind_func(self.key, "", idx)
            # Обновляем UI или можно перерисовать полностью содержимое спойлера
            while self.content_layout.count() > 0:
                item = self.content_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            for index, keyword in enumerate(self.keywords):
                keyword_layout = QHBoxLayout()

                keyword_line = QLineEdit(keyword)
                keyword_line.setPlaceholderText(keyword)
                keyword_line.textChanged.connect(
                    lambda text, idx=index: self.rebind_func(self.key, text, idx)
                )

                delete_button = QPushButton()
                delete_button.setIcon(QIcon(self.del_ico))
                delete_button.setFixedSize(QSize(40, 40))
                delete_button.clicked.connect(lambda _, idx=index: self.delete_keyword(idx))

                keyword_layout.addWidget(keyword_line)
                keyword_layout.addWidget(delete_button)
                self.content_layout.addLayout(keyword_layout)