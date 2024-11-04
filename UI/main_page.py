from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from UI.theme_manager import ThemeManager
from UI.ui_main_page import Ui_MainPage_FormDock
from UI.widgets.key_bind_widget import KeyWidget
from functional.app_management import AppManagement
from functional.keywords_settings import KeywordsSettings
from logger.logger_config import logger as log
from UI.widgets.keyword_spoiler import KeywordSpoiler


class MainPage(QWidget, Ui_MainPage_FormDock):
    theme_manager = ThemeManager()

    def __init__(self, page_manager):
        super().__init__()
        self.page_manager = page_manager
        self.setupUi(self)

        # Инициализация необходимых классов
        self.ks = KeywordsSettings()
        self.am = AppManagement()
        self.path_dict = self.am.paths
        self.ks.keys_updated.connect(self.init_keys_view)

        # Регистрация страницы в менеджере страниц
        self.page_manager.register_page(self.__class__.__name__, self)

        # Настройка элементов интерфейса
        self.pushButton.clicked.connect(self.on_add_button_click)
        self.keyword_lineEdit.setPlaceholderText('Ключевое слово')
        self.path_lineEdit.setPlaceholderText('Путь')
        self.VoiceMode_comboBox.setCurrentIndex(self.ks.vc.operating_mode)
        self.VoiceMode_comboBox.currentIndexChanged.connect(self.on_voice_mode_combobox_changed)
        self.theme_comboBox.setCurrentIndex(self.theme_manager.get_app_theme_index())
        self.theme_comboBox.currentIndexChanged.connect(self.on_theme_combobox_changed)

        # Связываем клики по элементам списка с переключением страниц
        self.category_list.currentRowChanged.connect(self.on_category_changed)

        # Лейаут для отображения спойлеров и путей
        self.keyword_layout = QVBoxLayout()
        self.keys_verticalLayout.setAlignment(Qt.AlignTop)
        self.keyword_verticalLayout.addLayout(self.keyword_layout)
        self.entry_layout = QVBoxLayout()
        self.init_keywords_view()
        self.init_dictionary_view()
        self.init_keys_view()  # Вызов метода для инициализации ключей

        log.debug('Главная страница инициализирована')
        self.theme_manager.apply_theme(self)
        self.init_keys_view()

    def init_keys_view(self):
        """Создаем виджеты для каждого ключа в словаре keys и добавляем их в keys_verticalLayout."""
        # Очищаем layout перед добавлением новых виджетов
        for i in reversed(range(self.keys_verticalLayout.count())):
            widget = self.keys_verticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Создаем виджет для каждого ключа и комбинации из словаря keys
        for key, key_combination in self.ks.vc.keys.items():
            key_widget = KeyWidget(key, key_combination, self.ks.rebind_vc_keys)
            self.keys_verticalLayout.addWidget(key_widget)

    def init_keywords_view(self):
        """Создаем и добавляем KeywordSpoiler для каждого ключа в словаре ключевых слов."""
        # Очищаем предыдущие элементы из layout
        for i in reversed(range(self.keyword_layout.count())):
            widget = self.keyword_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Создаем и добавляем KeywordSpoiler для каждого ключа в словаре
        for key, keywords in self.ks.vc.keywords.items():
            spoiler = KeywordSpoiler(
                key,
                keywords,
                self.ks.rebind_vc_keywords,
                self.ks.add_vc_keywords
            )
            self.keyword_layout.addWidget(spoiler)
            log.debug(f'Добавлен спойлер для ключа: {key}')

    def init_dictionary_view(self):
        """Метод для инициализации отображения словаря путей."""
        # Очищаем предыдущие элементы из layout, если они были
        if hasattr(self, 'entry_layout'):
            for i in reversed(range(self.entry_layout.count())):
                widget = self.entry_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        # Создаем блоки для каждой пары из словаря путей
        for key, value in self.path_dict.items():
            self.entry_layout.addWidget(self.create_entry_block(key, value))
            log.debug(f'Добавлен элемент для ключа: {key}')

        # Устанавливаем виджет в scroll area
        container = QWidget()
        container.setLayout(self.entry_layout)
        self.app_scrollArea.setWidgetResizable(True)
        self.app_scrollArea.setWidget(container)

    def create_entry_block(self, key, value):
        """Создание блока для отображения и редактирования элементов словаря путей."""
        block = QWidget()
        block_layout = QHBoxLayout()

        key_edit = QLineEdit(key)
        key_edit.setReadOnly(True)
        key_edit.setMinimumSize(QSize(140, 40))

        value_edit = QLineEdit(value)
        value_edit.setMinimumSize(QSize(300, 40))

        edit_button = QPushButton("")
        edit_button.setIconSize(QSize(20, 20))
        edit_button.setMinimumSize(QSize(40, 40))

        delete_button = QPushButton("")
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setMinimumSize(QSize(40, 40))

        # Устанавливаем иконки в зависимости от темы
        if self.theme_manager.get_app_theme_index() == 0:
            edit_button.setIcon(QIcon("res/icon-diskette_dark.png"))
            delete_button.setIcon(QIcon("res/icon-delete_dark.png"))
        else:
            edit_button.setIcon(QIcon("res/icon-diskette.png"))
            delete_button.setIcon(QIcon("res/icon-delete.png"))

        # Связываем действия кнопок с методами редактирования и удаления
        edit_button.clicked.connect(lambda: self.edit_entry(key_edit, value_edit))
        delete_button.clicked.connect(lambda: self.delete_entry(block, key))

        block_layout.addWidget(key_edit)
        block_layout.addWidget(value_edit)
        block_layout.addWidget(edit_button)
        block_layout.addWidget(delete_button)

        block.setLayout(block_layout)
        return block

    def edit_entry(self, key_edit, value_edit):
        """Редактирование существующего элемента словаря путей."""
        new_key = key_edit.text()
        new_value = value_edit.text()
        self.am.edit_path(new_key, new_value)
        log.debug(f'Изменено значение для ключа: {new_key}, новое значение: {new_value}')

    def delete_entry(self, block, key):
        """Удаление элемента из словаря путей и обновление интерфейса."""
        block.setParent(None)
        self.am.delete_path(key)
        log.debug(f'Удален элемент с ключом: {key}')
        self.init_dictionary_view()

    def on_add_button_click(self):
        """Добавить новое ключевое слово и его путь."""
        text = self.keyword_lineEdit.text()
        path_text = self.path_lineEdit.text()
        if text and path_text:
            self.am.add_path(text, path_text)
            self.path_dict = self.am.paths
            self.init_dictionary_view()
            log.debug(f'Добавлен элемент с ключом: {text} и значением: {path_text}')

            # Очищаем поля после добавления
            self.keyword_lineEdit.clear()
            self.path_lineEdit.clear()
        else:
            log.warning("Попытка добавления пустого значения")

    def on_voice_mode_combobox_changed(self, index):
        """Изменить режим голосового управления."""
        self.ks.vc.operating_mode = index
        log.debug(f'Режим голосового управления изменен на: {index}')

    def on_theme_combobox_changed(self, index):
        """Изменить тему приложения."""
        self.theme_manager.set_app_theme(index)
        self.theme_manager.apply_theme(self)
        self.init_keywords_view()
        self.init_dictionary_view()
        log.debug(f'Тема приложения изменена на: {index}')

    def on_category_changed(self, index):
        """Переключение категории по индексу."""
        self.page_dock.setCurrentIndex(index)
        log.debug(f'Переключена категория на индекс: {index}')

