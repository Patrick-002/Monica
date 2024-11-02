from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QScrollArea

from UI.styles.theme_manager import apply_theme
from UI.ui_main_page import Ui_FormDock
from functional.app_management import AppManagement
from functional.voice_controller import VoiceCommands
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from logger.logger_config import logger as log


class MainPage(QWidget, Ui_FormDock):

    def __init__(self, page_manager):
        super().__init__()
        self.page_manager = page_manager
        self.setupUi(self)
        self.vc = VoiceCommands()
        self.am = AppManagement()

        # Получаем словарь с путями
        self.path_dict = self.am.paths

        # Регистрация страницы в менеджере страниц
        self.page_manager.register_page(self.__class__.__name__, self)

        self.pushButton.clicked.connect(self.on_add_button_click)

        self.keyword_lineEdit.setPlaceholderText('Ключевое слово')
        self.path_lineEdit.setPlaceholderText('Путь')

        self.VoiceMode_comboBox.setCurrentIndex(self.vc.operating_mode)
        self.VoiceMode_comboBox.currentIndexChanged.connect(self.on_voicemode_combobox_changed)
        log.debug('ComboBox установлен в начальный индекс')

        image_path = "res/arrow_down.png"
        image_path = "res/arrow_down.png"

        # Связываем клики по элементам списка с переключением страниц
        self.category_list.currentRowChanged.connect(self.on_category_changed)

        # Инициализируем отображение словаря
        self.init_dictionary_view()
        log.debug('Главная страница инициализирована')

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
            log.debug(f'Добавлен элемент для ключа: {key}')

    def create_entry_block(self, key, value):
        block = QWidget()
        block_layout = QHBoxLayout()

        key_edit = QLineEdit(key)
        key_edit.setReadOnly(True)
        key_edit.setMinimumSize(QSize(140, 40))

        value_edit = QLineEdit(value)
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
        apply_theme(self)
        return block

    def edit_entry(self, key_edit, value_edit):
        new_key = key_edit.text()
        new_value = value_edit.text()
        self.am.edit_path(new_key, new_value)
        log.debug(f'Изменено значение для ключа: {new_key}, новое значение: {new_value}')

    def delete_entry(self, block, key):
        del self.path_dict[key]
        block.setParent(None)
        self.am.delete_path(key)
        log.debug(f'Удален элемент с ключом: {key}')
        self.init_dictionary_view()

    def on_category_changed(self, index):
        self.page_dock.setCurrentIndex(index)
        log.debug(f'Переключена категория на индекс: {index}')

    def on_add_button_click(self):
        text = self.keyword_lineEdit.text()
        path_text = self.path_lineEdit.text()
        if text and path_text:
            self.am.add_path(text, path_text)
            self.path_dict = self.am.paths
            self.init_dictionary_view()
            log.debug(f'Добавлен элемент с ключом: {text} и значением: {path_text}')

            self.keyword_lineEdit.setText('')
            self.path_lineEdit.setText('')
        else:
            log.warning("Попытка добавления пустого значения")

    def on_voicemode_combobox_changed(self, index):
        self.vc.operating_mode = index
        log.debug(f'Режим голосового управления изменен на: {index}')
