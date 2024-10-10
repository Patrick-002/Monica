from PySide6.QtWidgets import QStackedWidget

class PageManager:
    def __init__(self):
        self.stacked_widget = QStackedWidget()
        self.pages = {}
        self.current_index = 0
        self.previous_index = None

    def register_page(self, page_name, page_widget):
        """Регистрация страницы и её добавление в QStackedWidget"""
        index = self.stacked_widget.addWidget(page_widget)
        self.pages[page_name] = index
        print(f"Страница '{page_name}' успешно добавлена.")

    def show_page(self, page_name):
        """Показ страницы по её имени"""
        if page_name in self.pages:
            self.previous_index = self.current_index
            self.current_index = self.pages[page_name]
            self.stacked_widget.setCurrentIndex(self.current_index)
        else:
            print(f"Страница '{page_name}' не найдена.")

    def show_previous_page(self):
        """Переход на предыдущую страницу"""
        if self.previous_index is not None:
            self.stacked_widget.setCurrentIndex(self.previous_index)
