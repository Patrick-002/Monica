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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_FormDock(object):
    def setupUi(self, FormDock):
        if not FormDock.objectName():
            FormDock.setObjectName(u"FormDock")
        FormDock.setWindowModality(Qt.WindowModality.NonModal)
        FormDock.setEnabled(True)
        FormDock.resize(900, 550)
        FormDock.setStyleSheet(u"                background: qlineargradient(\n"
"                    spread:pad, \n"
"                    x1:0, y1:0, x2:1, y2:1, \n"
"                    stop:0 #4B0082,   /* \u0422\u0451\u043c\u043d\u043e-\u0444\u0438\u043e\u043b\u0435\u0442\u043e\u0432\u044b\u0439 */\n"
"                    stop:0.5 #3C3F41, /* \u0422\u0451\u043c\u043d\u043e-\u0441\u0435\u0440\u044b\u0439 */\n"
"                    stop:1 #2E8B57    /* \u0422\u0451\u043c\u043d\u043e-\u0437\u0435\u043b\u0451\u043d\u044b\u0439 */\n"
"                );\n"
"                font-family: 'Segoe UI'; /* \u0428\u0440\u0438\u0444\u0442 Segoe UI */\n"
"                font-size: 12pt;         /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430 */\n"
"                color: white;            /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */")
        self.verticalLayoutWidget = QWidget(FormDock)
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
        self.page_dock.setGeometry(QRect(10, 10, 605, 527))
        self.page_dock.setStyleSheet(u"    alignment: center;\n"
"    background: transparent;\n"
"    height: 0px; /* \u0421\u043a\u0440\u044b\u0442\u044c \u0432\u044b\u0441\u043e\u0442\u0443 \u043a\u043d\u043e\u043f\u043e\u043a */")
        self.another_settings = QWidget()
        self.another_settings.setObjectName(u"another_settings")
        self.tab_app_commands = QTabWidget(self.another_settings)
        self.tab_app_commands.setObjectName(u"tab_app_commands")
        self.tab_app_commands.setGeometry(QRect(0, 0, 601, 501))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 151, 21))
        self.keyword_lineEdit = QLineEdit(self.tab)
        self.keyword_lineEdit.setObjectName(u"keyword_lineEdit")
        self.keyword_lineEdit.setGeometry(QRect(10, 50, 181, 41))
        self.keyword_lineEdit.setStyleSheet(u"    QLineEdit {\n"
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
        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(200, 50, 361, 41))
        self.lineEdit.setStyleSheet(u"    QLineEdit {\n"
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
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(450, 110, 111, 41))
        self.pushButton.setStyleSheet(u"    QPushButton {\n"
"        border: 2px solid #4a4a4a;\n"
"        border-radius: 10px;\n"
"        padding: 8px 16px;\n"
"        font-size: 16px;\n"
"        background-color: #2b2b2b;\n"
"        color: #dcdcdc;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #3a3a3a;\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: #4e4e4e;\n"
"        border: 2px solid #9a9edb;\n"
"    }")
        self.tab_app_commands.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_app_commands.addTab(self.tab_2, "")
        self.page_dock.addWidget(self.another_settings)
        self.monica_settings = QWidget()
        self.monica_settings.setObjectName(u"monica_settings")
        self.label_3 = QLabel(self.monica_settings)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(260, 180, 251, 91))
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


        self.retranslateUi(FormDock)

        self.page_dock.setCurrentIndex(0)
        self.tab_app_commands.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FormDock)
    # setupUi

    def retranslateUi(self, FormDock):
        FormDock.setWindowTitle(QCoreApplication.translate("FormDock", u"Form", None))

        __sortingEnabled = self.category_list.isSortingEnabled()
        self.category_list.setSortingEnabled(False)
        ___qlistwidgetitem = self.category_list.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u043a\u0438 \u041c\u043e\u043d\u0438\u043a\u0438", None));
        ___qlistwidgetitem1 = self.category_list.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None));
        ___qlistwidgetitem2 = self.category_list.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("FormDock", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430", None));
        ___qlistwidgetitem3 = self.category_list.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("FormDock", u"\u041f\u0440\u043e\u0447\u0438\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 ", None));
        self.category_list.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("FormDock", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u043c\u0430\u043d\u0434\u0443:", None))
#if QT_CONFIG(tooltip)
        self.keyword_lineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.keyword_lineEdit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.keyword_lineEdit.setInputMask("")
        self.keyword_lineEdit.setText("")
        self.pushButton.setText(QCoreApplication.translate("FormDock", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.tab_app_commands.setTabText(self.tab_app_commands.indexOf(self.tab), QCoreApplication.translate("FormDock", u"\u0417\u0430\u043f\u0443\u0441\u043a \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0439", None))
        self.tab_app_commands.setTabText(self.tab_app_commands.indexOf(self.tab_2), QCoreApplication.translate("FormDock", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043c\u0435\u0434\u0438\u0430", None))
        self.label_3.setText(QCoreApplication.translate("FormDock", u"monica_settings", None))
        self.label_2.setText(QCoreApplication.translate("FormDock", u"interface_settings_page", None))
        self.label_4.setText(QCoreApplication.translate("FormDock", u"voice_model_settings", None))
    # retranslateUi

