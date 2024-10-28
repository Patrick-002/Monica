from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QScrollArea
from UI.ui_main_page import Ui_FormDock
from functional.appmanagement import AppManagement
from functional.voice_controller import VoiceController
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon


class MainPage(QWidget, Ui_FormDock):
    am = AppManagement()

    def __init__(self, page_manager):
        super().__init__()
        self.page_manager = page_manager
        self.setupUi(self)

        # Получаем словарь с путями
        self.path_dict = AppManagement().paths

        # Регистрация страницы в менеджере страниц
        self.page_manager.register_page(self.__class__.__name__, self)

        self.pushButton.clicked.connect(self.on_add_button_click)

        self.keyword_lineEdit.setPlaceholderText('Ключевое слово')
        self.path_lineEdit.setPlaceholderText('Путь')

        self.VoiceMode_comboBox.currentIndexChanged.connect(self.on_voicemode_combobox_changed)
        image_path = "res/arrow_down.png"
        self.VoiceMode_comboBox.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid #4a4a4a;
                border-radius: 10px;
                padding: 8px;
                padding-right: 30px;
                font-size: 16px;
                background-color: #2b2b2b;
                color: #dcdcdc;
            }}
            QComboBox:hover {{
                border: 2px solid #6a6a6a;
            }}
            QComboBox:focus {{
                border: 2px solid #9a9edb;
                background-color: #3a3a3a;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 18px; /* Уменьшение ширины для меньшего отступа */
                background-color: transparent;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                margin: 2px;
            }}
            QComboBox::down-arrow {{
                image: url({image_path});
                width: 12px;
                height: 12px;
            }}
        """)

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
        for key, value in self.path_dict.items():
            self.entry_layout.addWidget(self.create_entry_block(key, value))

    def create_entry_block(self, key, value):
        block = QWidget()
        block_layout = QHBoxLayout()

        key_edit = QLineEdit(key)
        key_edit.setReadOnly(True)
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

        edit_button = QPushButton("")
        edit_button.setIcon(QIcon("res/icon-diskette.png"))
        edit_button.setIconSize(QSize(20, 20))
        edit_button.setMinimumSize(QSize(40, 40))
        delete_button = QPushButton("")
        delete_button.setIcon(QIcon("res/icon-delete.png"))
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setMinimumSize(QSize(40, 40))

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
        self.am.edit_path(new_key, new_value)

    def delete_entry(self, block, key):
        del self.path_dict[key]
        block.setParent(None)
        self.am.delete_path(key)
        self.init_dictionary_view()

    def on_category_changed(self, index):
        self.page_dock.setCurrentIndex(index)

    def on_add_button_click(self):
        text = self.keyword_lineEdit.text()
        path_text = self.path_lineEdit.text()
        if text and path_text:
            self.am.add_path(text, path_text)
            self.path_dict = self.am.paths
            self.init_dictionary_view()
        else:
            print("Пустое поле ввода")

    def on_voicemode_combobox_changed(self, index):
        vc = VoiceController()
        vc.operating_mode = index + 1
