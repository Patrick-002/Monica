from PySide6.QtWidgets import QWidget
from UI.ui_main_page import Ui_FormDock
from functional.appmanagement import AppManagement

class MainPage(QWidget, Ui_FormDock):
    def __init__(self, page_manager):
        super().__init__()
        self.page_manager = page_manager
        self.setupUi(self)
        # Регистрация страницы в менеджере страниц
        self.page_manager.register_page(self.__class__.__name__, self)

        self.pushButton.clicked.connect(self.on_add_button_click)

        self.keyword_lineEdit.setPlaceholderText('Ключевое слово')
        self.path_lineEdit.setPlaceholderText('Путь')

        # Связываем клики по элементам списка с переключением страниц
        self.category_list.currentRowChanged.connect(self.on_category_changed)

    def on_category_changed(self, index):
        self.page_dock.setCurrentIndex(index)

    def on_add_button_click(self):
        text = self.keyword_lineEdit.text()
        if text:
            am = AppManagement()
            am.add_app_path(self.keyword_lineEdit.text(), self.path_lineEdit.text())
            print(am.apps)
            # am.load_data()
        else:
            print("Пустое поле ввода")

