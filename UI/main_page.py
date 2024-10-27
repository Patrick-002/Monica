from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QScrollArea
from UI.ui_main_page import Ui_FormDock
from functional.appmanagement import AppManagement
from PySide6.QtCore import QSize

class MainPage(QWidget, Ui_FormDock):
    def __init__(self, page_manager):
        super().__init__()
        self.page_manager = page_manager
        self.setupUi(self)

        # Получаем словарь с путями
        self.dictn = AppManagement().paths

        # Регистрация страницы в менеджере страниц
        self.page_manager.register_page(self.__class__.__name__, self)

        self.pushButton.clicked.connect(self.on_add_button_click)

        self.keyword_lineEdit.setPlaceholderText('Ключевое слово')
        self.path_lineEdit.setPlaceholderText('Путь')

        # Связываем клики по элементам списка с переключением страниц
        self.category_list.currentRowChanged.connect(self.on_category_changed)

        # Инициализируем отображение словаря
        self.init_dictionary_view()

    def init_dictionary_view(self):
        # Очищаем предыдущие элементы из scroll area, если они были
        if hasattr(self, 'entry_layout'):
            for i in reversed(range(self.entry_layout.count())):
                widget = self.entry_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        self.entry_layout = QVBoxLayout()
        self.app_scrollArea.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(self.entry_layout)

        self.app_scrollArea.setWidget(container)

        # Создаем блоки для каждой пары из словаря
        for key, value in self.dictn.items():
            self.entry_layout.addWidget(self.create_entry_block(key, value))

    def create_entry_block(self, key, value):
        block = QWidget()
        block_layout = QHBoxLayout()

        key_edit = QLineEdit(key)
        key_edit.setStyleSheet(u"    QLineEdit {\n"
"        border: 2px solid #4a4a4a;\n"
"        border-radius: 10px;\n"
"        padding: 8px;\n"
"        font-size: 16px;\n"
"        background-color: #2b2b2b;\n"
"        color: #dcdcdc;\n"
"    }\n"
"    QLineEdit:focus {\n"
"        border: 2px solid #9a9edb;\n"
"        background-color: #3a3a3a;\n"
"    }")
        key_edit.setMinimumSize(QSize(140, 40))

        value_edit = QLineEdit(value)
        value_edit.setStyleSheet(u"    QLineEdit {\n"
                               "        border: 2px solid #4a4a4a;\n"
                               "        border-radius: 10px;\n"
                               "        padding: 8px;\n"
                               "        font-size: 16px;\n"
                               "        background-color: #2b2b2b;\n"
                               "        color: #dcdcdc;\n"
                               "    }\n"
                               "    QLineEdit:focus {\n"
                               "        border: 2px solid #9a9edb;\n"
                               "        background-color: #3a3a3a;\n"
                               "    }")
        value_edit.setMinimumSize(QSize(300, 40))

        edit_button = QPushButton("Р")
        edit_button.setMaximumSize(QSize(40, 40))
        delete_button = QPushButton("У")
        delete_button.setMaximumSize(QSize(40, 40))

        edit_button.clicked.connect(lambda: self.edit_entry(key_edit, value_edit))
        delete_button.clicked.connect(lambda: self.delete_entry(block, key))

        block_layout.addWidget(key_edit)
        block_layout.addWidget(value_edit)
        block_layout.addWidget(edit_button)
        block_layout.addWidget(delete_button)

        block.setLayout(block_layout)
        return block

    def edit_entry(self, key_edit, value_edit):
        new_key = key_edit.text()
        new_value = value_edit.text()
        # Обновляем словарь
        self.dictn[new_key] = new_value
        print(f"Отредактировано: {new_key} -> {new_value}")

    def delete_entry(self, block, key):
        del self.dictn[key]
        block.setParent(None)  # Убираем блок с интерфейса
        print(f"Удалено: {key}")
        self.init_dictionary_view()  # Обновляем представление

    def on_category_changed(self, index):
        self.page_dock.setCurrentIndex(index)

    def on_add_button_click(self):
        text = self.keyword_lineEdit.text()
        if text:
            am = AppManagement()
            am.add_path(self.keyword_lineEdit.text(), self.path_lineEdit.text())
            print(am.paths)
            self.init_dictionary_view()  # Обновляем представление при добавлении
        else:
            print("Пустое поле ввода")
