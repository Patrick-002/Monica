# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_page.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, Qt)
from PySide6.QtWidgets import (QLabel, QListWidget, QListWidgetItem,
                               QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy)


class SettingsPage(QWidget):
    def __init__(self, page_manager):
        super().__init__()

        self.page_manager = page_manager  # Сохраняем экземпляр PageManager
        self.page_manager.register_page(self.__class__.__name__, self)  # Регистрация страницы

        # Настройка пользовательского интерфейса
        self.ui = Ui_FormDock(page_manager)
        self.ui.setupUi(self)

    def retranslateUi(self):
        self.ui.retranslateUi(self)


class Ui_FormDock(object):
    def __init__(self, page_manager):
        self.page_manager = page_manager  # Сохраняем экземпляр PageManager

    def setupUi(self, FormDock):
        if not FormDock.objectName():
            FormDock.setObjectName(u"FormDock")
        FormDock.resize(900, 550)
        FormDock.setStyleSheet(u"""
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4B0082, 
                    stop:0.5 #3C3F41, 
                    stop:1 #2E8B57
                );
                font-family: 'Segoe UI'; 
                font-size: 12pt;         
                color: white;
        """)

        # Главный вертикальный layout
        self.verticalLayout = QVBoxLayout(FormDock)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        # Горизонтальный layout для списка категорий и контента
        self.horizontalLayout = QHBoxLayout()

        # Список категорий
        self.category_list = QListWidget(FormDock)
        font = self.category_list.font()
        font.setPointSize(11)
        self.category_list.setFont(font)

        # Устанавливаем политику размеров для списка категорий
        self.category_list.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.category_list.setMaximumWidth(250)

        # Добавляем элементы в список категорий
        self.add_list_items()

        # Добавляем список категорий в горизонтальный layout
        self.horizontalLayout.addWidget(self.category_list)

        # Добавляем область для контента (QStackedWidget)
        self.page_dock = QStackedWidget(FormDock)
        self.page_dock.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Добавляем страницы в QStackedWidget
        self.add_pages()

        # Добавляем QStackedWidget в горизонтальный layout
        self.horizontalLayout.addWidget(self.page_dock)

        # Добавляем горизонтальный layout в вертикальный layout
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Настраиваем начальную страницу
        self.page_dock.setCurrentIndex(0)

    def add_list_items(self):
        # Добавляем пункты в список категорий
        categories = [
            QCoreApplication.translate("FormDock", u"Настройки Моники", None),
            QCoreApplication.translate("FormDock", u"Настройки голосовой модели", None),
            QCoreApplication.translate("FormDock", u"Настройки интерфейса", None),
            QCoreApplication.translate("FormDock", u"Прочие настройки", None)
        ]
        for category in categories:
            item = QListWidgetItem(category)
            self.category_list.addItem(item)

    def add_pages(self):
        # Создаем страницы и добавляем их в page_dock
        self.another_settings = QWidget()
        self.label = QLabel(self.another_settings)
        self.label.setText("Another Settings")

        layout1 = QVBoxLayout(self.another_settings)
        layout1.addWidget(self.label)
        layout1.setAlignment(Qt.AlignCenter)

        self.page_dock.addWidget(self.another_settings)

        self.monica_settings = QWidget()
        self.label_3 = QLabel(self.monica_settings)
        self.label_3.setText("Monica Settings")

        layout2 = QVBoxLayout(self.monica_settings)
        layout2.addWidget(self.label_3)
        layout2.setAlignment(Qt.AlignCenter)

        self.page_dock.addWidget(self.monica_settings)

        self.interface_settings_page = QWidget()
        self.label_2 = QLabel(self.interface_settings_page)
        self.label_2.setText("Interface Settings")

        layout3 = QVBoxLayout(self.interface_settings_page)
        layout3.addWidget(self.label_2)
        layout3.setAlignment(Qt.AlignCenter)

        self.page_dock.addWidget(self.interface_settings_page)

        self.voice_model_settings = QWidget()
        self.label_4 = QLabel(self.voice_model_settings)
        self.label_4.setText("Voice Model Settings")

        layout4 = QVBoxLayout(self.voice_model_settings)
        layout4.addWidget(self.label_4)
        layout4.setAlignment(Qt.AlignCenter)

        self.page_dock.addWidget(self.voice_model_settings)

    def retranslateUi(self, FormDock):
        FormDock.setWindowTitle(QCoreApplication.translate("FormDock", u"Form", None))
        self.category_list.setSortingEnabled(True)
