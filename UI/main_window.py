# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 550)
        MainWindow.setStyleSheet(u"                background: qlineargradient(\n"
                                 "                    spread:pad, \n"
                                 "                    x1:0, y1:0, x2:1, y2:1, \n"
                                 "                    stop:0 #4B0082,   /* \u0422\u0451\u043c\u043d\u043e-\u0444\u0438\u043e\u043b\u0435\u0442\u043e\u0432\u044b\u0439 */\n"
                                 "                    stop:0.5 #3C3F41, /* \u0422\u0451\u043c\u043d\u043e-\u0441\u0435\u0440\u044b\u0439 */\n"
                                 "                    stop:1 #2E8B57    /* \u0422\u0451\u043c\u043d\u043e-\u0437\u0435\u043b\u0451\u043d\u044b\u0439 */\n"
                                 "                );\n"
                                 "                font-family: 'Segoe UI'; /* \u0428\u0440\u0438\u0444\u0442 Segoe UI */\n"
                                 "                font-size: 12pt;         /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430 */\n"
                                 "                color: white;            /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi
