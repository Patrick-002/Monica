# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_page.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QVBoxLayout,
    QWidget)

class UiMainPageFormDock(object):
    def setupUi(self, MainPage_FormDock):
        if not MainPage_FormDock.objectName():
            MainPage_FormDock.setObjectName(u"MainPage_FormDock")
        MainPage_FormDock.setWindowModality(Qt.WindowModality.NonModal)
        MainPage_FormDock.setEnabled(True)
        MainPage_FormDock.resize(900, 550)
        MainPage_FormDock.setStyleSheet(u"")
        self.verticalLayoutWidget = QWidget(MainPage_FormDock)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 881, 531))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.category_list = QListWidget(self.verticalLayoutWidget)
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.DemiBold)
        __qlistwidgetitem = QListWidgetItem(self.category_list)
        __qlistwidgetitem.setFont(font);
        __qlistwidgetitem1 = QListWidgetItem(self.category_list)
        __qlistwidgetitem1.setFont(font);
        __qlistwidgetitem2 = QListWidgetItem(self.category_list)
        __qlistwidgetitem2.setFont(font);
        __qlistwidgetitem3 = QListWidgetItem(self.category_list)
        __qlistwidgetitem3.setFont(font);
        self.category_list.setObjectName(u"category_list")
        self.category_list.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout.addWidget(self.category_list)

        self.frame = QFrame(self.verticalLayoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.page_dock = QStackedWidget(self.frame)
        self.page_dock.setObjectName(u"page_dock")
        self.page_dock.setGeometry(QRect(0, 0, 621, 531))
        self.page_dock.setStyleSheet(u"    alignment: center;\n"
"    background: transparent;\n"
"    height: 0px; /* \u0421\u043a\u0440\u044b\u0442\u044c \u0432\u044b\u0441\u043e\u0442\u0443 \u043a\u043d\u043e\u043f\u043e\u043a */")
        self.another_settings = QWidget()
        self.another_settings.setObjectName(u"another_settings")
        self.tab_app_commands = QTabWidget(self.another_settings)
        self.tab_app_commands.setObjectName(u"tab_app_commands")
        self.tab_app_commands.setGeometry(QRect(0, 0, 612, 531))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_7 = QVBoxLayout(self.tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(10, 0, 10, 0)
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.keyword_lineEdit = QLineEdit(self.tab)
        self.keyword_lineEdit.setObjectName(u"keyword_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyword_lineEdit.sizePolicy().hasHeightForWidth())
        self.keyword_lineEdit.setSizePolicy(sizePolicy)
        self.keyword_lineEdit.setMinimumSize(QSize(160, 40))

        self.horizontalLayout_2.addWidget(self.keyword_lineEdit)

        self.horizontalSpacer_4 = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.path_lineEdit = QLineEdit(self.tab)
        self.path_lineEdit.setObjectName(u"path_lineEdit")
        self.path_lineEdit.setMinimumSize(QSize(360, 40))

        self.horizontalLayout_2.addWidget(self.path_lineEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(450, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(110, 40))

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.app_scrollArea = QScrollArea(self.tab)
        self.app_scrollArea.setObjectName(u"app_scrollArea")
        self.app_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.app_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 99, 28))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.app_scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.app_scrollArea)


        self.verticalLayout_7.addLayout(self.verticalLayout_3)

        self.tab_app_commands.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_app_commands.addTab(self.tab_2, "")
        self.page_dock.addWidget(self.another_settings)
        self.monica_settings = QWidget()
        self.monica_settings.setObjectName(u"monica_settings")
        self.horizontalLayout_4 = QHBoxLayout(self.monica_settings)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.keywordType_label = QLabel(self.monica_settings)
        self.keywordType_label.setObjectName(u"keywordType_label")

        self.horizontalLayout_5.addWidget(self.keywordType_label)

        self.horizontalSpacer_2 = QSpacerItem(400, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.VoiceMode_comboBox = QComboBox(self.monica_settings)
        self.VoiceMode_comboBox.addItem("")
        self.VoiceMode_comboBox.addItem("")
        self.VoiceMode_comboBox.addItem("")
        self.VoiceMode_comboBox.setObjectName(u"VoiceMode_comboBox")
        self.VoiceMode_comboBox.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_5.addWidget(self.VoiceMode_comboBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 350, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.page_dock.addWidget(self.monica_settings)
        self.interface_settings_page = QWidget()
        self.interface_settings_page.setObjectName(u"interface_settings_page")
        self.label_2 = QLabel(self.interface_settings_page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(210, 140, 171, 51))
        self.page_dock.addWidget(self.interface_settings_page)
        self.voice_model_settings = QWidget()
        self.voice_model_settings.setObjectName(u"voice_model_settings")
        self.label_4 = QLabel(self.voice_model_settings)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(260, 170, 181, 61))
        self.page_dock.addWidget(self.voice_model_settings)

        self.horizontalLayout.addWidget(self.frame)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(MainPage_FormDock)

        self.page_dock.setCurrentIndex(1)
        self.tab_app_commands.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPage_FormDock)
    # setupUi

    def retranslateUi(self, MainPage_FormDock):
        MainPage_FormDock.setWindowTitle(QCoreApplication.translate("MainPage_FormDock", u"Form", None))

        __sortingEnabled = self.category_list.isSortingEnabled()
        self.category_list.setSortingEnabled(False)
        ___qlistwidgetitem = self.category_list.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainPage_FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u043a\u0438 \u041c\u043e\u043d\u0438\u043a\u0438", None));
        ___qlistwidgetitem1 = self.category_list.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainPage_FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None));
        ___qlistwidgetitem2 = self.category_list.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainPage_FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430", None));
        ___qlistwidgetitem3 = self.category_list.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainPage_FormDock", u"\u041f\u0440\u043e\u0447\u0438\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 ", None));
        self.category_list.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainPage_FormDock", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u043c\u0430\u043d\u0434\u0443:", None))
#if QT_CONFIG(tooltip)
        self.keyword_lineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.keyword_lineEdit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.keyword_lineEdit.setInputMask("")
        self.keyword_lineEdit.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainPage_FormDock", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.tab_app_commands.setTabText(self.tab_app_commands.indexOf(self.tab), QCoreApplication.translate("MainPage_FormDock", u"\u0417\u0430\u043f\u0443\u0441\u043a \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0439", None))
        self.tab_app_commands.setTabText(self.tab_app_commands.indexOf(self.tab_2), QCoreApplication.translate("MainPage_FormDock", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043c\u0435\u0434\u0438\u0430", None))
        self.keywordType_label.setText(QCoreApplication.translate("MainPage_FormDock", u"\u0420\u0435\u0436\u0438\u043c \u0430\u043a\u0442\u0438\u0432\u0430\u0446\u0438\u0438:", None))
        self.VoiceMode_comboBox.setItemText(0, QCoreApplication.translate("MainPage_FormDock", u"\u041f\u043e \u043a\u043b\u044e\u0447\u0435\u0432\u043e\u043c\u0443 \u0441\u043b\u043e\u0432\u0443", None))
        self.VoiceMode_comboBox.setItemText(1, QCoreApplication.translate("MainPage_FormDock", u"\u041f\u043e \u043d\u0430\u0436\u0430\u0442\u0438\u044e", None))
        self.VoiceMode_comboBox.setItemText(2, QCoreApplication.translate("MainPage_FormDock", u"\u041f\u043e \u0443\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044e", None))

        self.label_2.setText(QCoreApplication.translate("MainPage_FormDock", u"interface_settings_page", None))
        self.label_4.setText(QCoreApplication.translate("MainPage_FormDock", u"voice_model_settings", None))
    # retranslateUi

