from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt  # Импортируем Qt для выравнивания
from UI.theme_manager import ThemeManager


class KeywordSpoiler(QWidget):

    def __init__(self, key, keywords, rebind_func, add_func, parent=None):
        super().__init__(parent)
        self.key = key
        self.keywords = keywords
        self.rebind_func = rebind_func
        self.add_func = add_func

        self.theme_manager = ThemeManager()
        self.theme_id = self.theme_manager.get_app_theme_index()
        if self.theme_id == 0:
            self.del_ico = 'res/icon-delete_dark.png'
            self.right_arr_ico = 'res/arrow_right_dark.png'
            self.down_arr_ico = 'res/arrow_down_dark.png'
        else:
            self.del_ico = 'res/icon-delete.png'
            self.right_arr_ico = 'res/arrow_right.png'
            self.down_arr_ico = 'res/arrow_down.png'

        # Основной макет для спойлера
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Кнопка для открытия/закрытия спойлера
        self.toggle_button = QPushButton(key)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setIcon(QIcon(self.right_arr_ico))  # Иконка со стрелкой вправо
        self.toggle_button.clicked.connect(self.toggle_content)
        self.main_layout.addWidget(self.toggle_button)

        # Виджет-контейнер для содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setLayout(self.content_layout)
        self.content_widget.setVisible(False)
        self.main_layout.addWidget(self.content_widget)

        # Горизонтальный лейаут для двух колонок
        self.columns_layout = QHBoxLayout()
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()
        self.columns_layout.addLayout(self.left_column)
        self.columns_layout.addLayout(self.right_column)
        self.content_layout.addLayout(self.columns_layout)

        # Привязка колонок к верхнему краю и отключение растяжения
        self.left_column.setAlignment(Qt.AlignTop)
        self.right_column.setAlignment(Qt.AlignTop)

        # Флаг для отслеживания текущей колонки
        self.current_column = self.left_column

        # Добавление LineEdit и кнопки удаления для каждого ключевого слова
        for index, keyword in enumerate(keywords):
            self.add_keyword_widget(keyword, index)

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
        arrow_icon = self.down_arr_ico if is_checked else self.right_arr_ico
        self.toggle_button.setIcon(QIcon(arrow_icon))

    def add_new_keyword(self):
        """Добавить новое ключевое слово в словарь и обновить UI."""
        new_keyword = self.new_keyword_line.text().strip()
        if new_keyword:
            self.add_func(self.key, new_keyword)
            self.keywords.append(new_keyword)
            self.add_keyword_widget(new_keyword, len(self.keywords) - 1)
            self.new_keyword_line.clear()

    def add_keyword_widget(self, keyword, index):
        """Добавить виджет для ключевого слова в одну из колонок."""
        keyword_layout = QHBoxLayout()

        keyword_line = QLineEdit(keyword)
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

        # Добавляем виджет в текущую колонку и чередуем колонки
        self.current_column.addLayout(keyword_layout)
        self.current_column = self.right_column if self.current_column == self.left_column else self.left_column

    def delete_keyword(self, idx):
        """Удалить ключевое слово из словаря и обновить UI."""
        if 0 <= idx < len(self.keywords):
            del self.keywords[idx]
            self.rebind_func(self.key, "", idx)

            # Очищаем текущие виджеты перед перерисовкой
            while self.left_column.count() > 0:
                item = self.left_column.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            while self.right_column.count() > 0:
                item = self.right_column.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Заново добавляем ключевые слова в обе колонки
            self.current_column = self.left_column  # Сбрасываем колонку для чередования
            for index, keyword in enumerate(self.keywords):
                self.add_keyword_widget(keyword, index)
