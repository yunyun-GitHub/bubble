# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetUp.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_SetUp(object):
    def setupUi(self, SetUp):
        if not SetUp.objectName():
            SetUp.setObjectName(u"SetUp")
        SetUp.resize(498, 433)
        SetUp.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(SetUp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(SetUp)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel{\n"
"	font: 20pt \"\u6977\u4f53\";\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius:4px;\n"
"}")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.hideButton = QPushButton(self.widget)
        self.hideButton.setObjectName(u"hideButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setStyleSheet(u"QPushButton{\n"
"	width:20px;\n"
"	height:20px;\n"
"	border-radius:4px;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 25pt;\n"
"}")

        self.horizontalLayout.addWidget(self.hideButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.horizontalLayout_2.addWidget(self.stackedWidget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.addButton = QPushButton(self.widget)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setMinimumSize(QSize(0, 30))
        self.addButton.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.addButton)

        self.ListWidgetFloatWindow = QListWidget(self.widget)
        self.ListWidgetFloatWindow.setObjectName(u"ListWidgetFloatWindow")
        self.ListWidgetFloatWindow.setMaximumSize(QSize(150, 16777215))
        self.ListWidgetFloatWindow.setStyleSheet(u"QListView::item {\n"
"    height: 50px;\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"	background:rgba(255,255,255,0.8);\n"
"}\n"
"\n"
"QListView::item:selected { \n"
"     background:rgba(255,255,255,0.8);\n"
"}\n"
"\n"
"QPushButton {\n"
"	width:10px;\n"
"	height:10px;\n"
"	border-radius:4px;\n"
"}\n"
"\n"
"QListWidget {\n"
"	background-color: rgba(255,255,255,0.4);\n"
"}")

        self.verticalLayout_3.addWidget(self.ListWidgetFloatWindow)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(SetUp)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(SetUp)
    # setupUi

    def retranslateUi(self, SetUp):
        SetUp.setWindowTitle(QCoreApplication.translate("SetUp", u"Form", None))
        self.label.setText(QCoreApplication.translate("SetUp", u"\u8bbe\u7f6e", None))
        self.hideButton.setText(QCoreApplication.translate("SetUp", u"X", None))
        self.addButton.setText(QCoreApplication.translate("SetUp", u"\u6dfb\u52a0", None))
    # retranslateUi

