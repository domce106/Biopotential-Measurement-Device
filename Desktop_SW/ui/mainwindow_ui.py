# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1039, 648)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.configTab = QWidget()
        self.configTab.setObjectName(u"configTab")
        self.registerReadTable = QTableWidget(self.configTab)
        if (self.registerReadTable.columnCount() < 1):
            self.registerReadTable.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.registerReadTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.registerReadTable.rowCount() < 12):
            self.registerReadTable.setRowCount(12)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(6, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(7, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(8, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(9, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(10, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.registerReadTable.setVerticalHeaderItem(11, __qtablewidgetitem12)
        self.registerReadTable.setObjectName(u"registerReadTable")
        self.registerReadTable.setGeometry(QRect(590, 50, 221, 391))
        self.registerReadTable.setRowCount(12)
        self.registerReadTable.setColumnCount(1)
        self.registerReadTable.horizontalHeader().setDefaultSectionSize(100)
        self.modeComboBox = QComboBox(self.configTab)
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.setObjectName(u"modeComboBox")
        self.modeComboBox.setGeometry(QRect(110, 110, 79, 29))
        self.channel1ComboBox = QComboBox(self.configTab)
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.addItem("")
        self.channel1ComboBox.setObjectName(u"channel1ComboBox")
        self.channel1ComboBox.setGeometry(QRect(110, 160, 79, 29))
        self.channel2ComboBox = QComboBox(self.configTab)
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.addItem("")
        self.channel2ComboBox.setObjectName(u"channel2ComboBox")
        self.channel2ComboBox.setGeometry(QRect(110, 210, 79, 29))
        self.label = QLabel(self.configTab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 110, 63, 21))
        self.label_2 = QLabel(self.configTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(590, 20, 211, 21))
        self.label_3 = QLabel(self.configTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 160, 81, 21))
        self.label_4 = QLabel(self.configTab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 210, 81, 21))
        self.label_5 = QLabel(self.configTab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 260, 81, 21))
        self.bitrateComboBox = QComboBox(self.configTab)
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.addItem("")
        self.bitrateComboBox.setObjectName(u"bitrateComboBox")
        self.bitrateComboBox.setGeometry(QRect(110, 260, 79, 29))
        self.saveParamsPushButton = QPushButton(self.configTab)
        self.saveParamsPushButton.setObjectName(u"saveParamsPushButton")
        self.saveParamsPushButton.setGeometry(QRect(110, 330, 88, 29))
        self.setRegisterComboBox = QComboBox(self.configTab)
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.addItem("")
        self.setRegisterComboBox.setObjectName(u"setRegisterComboBox")
        self.setRegisterComboBox.setGeometry(QRect(130, 380, 111, 29))
        self.label_6 = QLabel(self.configTab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 380, 111, 21))
        self.label_7 = QLabel(self.configTab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 440, 101, 21))
        self.saveRegisterPushButton = QPushButton(self.configTab)
        self.saveRegisterPushButton.setObjectName(u"saveRegisterPushButton")
        self.saveRegisterPushButton.setGeometry(QRect(130, 480, 111, 29))
        self.setRegisterLineEdit = QLineEdit(self.configTab)
        self.setRegisterLineEdit.setObjectName(u"setRegisterLineEdit")
        self.setRegisterLineEdit.setGeometry(QRect(130, 430, 113, 29))
        self.channel1CheckBox = QCheckBox(self.configTab)
        self.channel1CheckBox.setObjectName(u"channel1CheckBox")
        self.channel1CheckBox.setGeometry(QRect(200, 160, 21, 27))
        self.channel2CheckBox = QCheckBox(self.configTab)
        self.channel2CheckBox.setObjectName(u"channel2CheckBox")
        self.channel2CheckBox.setGeometry(QRect(200, 210, 21, 27))
        self.modeLineEdit = QLineEdit(self.configTab)
        self.modeLineEdit.setObjectName(u"modeLineEdit")
        self.modeLineEdit.setGeometry(QRect(240, 110, 113, 29))
        self.channel1LineEdit = QLineEdit(self.configTab)
        self.channel1LineEdit.setObjectName(u"channel1LineEdit")
        self.channel1LineEdit.setGeometry(QRect(240, 160, 113, 29))
        self.channel2LineEdit = QLineEdit(self.configTab)
        self.channel2LineEdit.setObjectName(u"channel2LineEdit")
        self.channel2LineEdit.setGeometry(QRect(240, 210, 113, 29))
        self.bitrateLineEdit = QLineEdit(self.configTab)
        self.bitrateLineEdit.setObjectName(u"bitrateLineEdit")
        self.bitrateLineEdit.setGeometry(QRect(240, 260, 113, 29))
        self.RLDCH1PCheckBox = QCheckBox(self.configTab)
        self.RLDCH1PCheckBox.setObjectName(u"RLDCH1PCheckBox")
        self.RLDCH1PCheckBox.setGeometry(QRect(110, 300, 21, 27))
        self.label_8 = QLabel(self.configTab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 300, 63, 21))
        self.label_9 = QLabel(self.configTab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(60, 300, 41, 21))
        self.label_19 = QLabel(self.configTab)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(140, 300, 41, 21))
        self.RLDCH1NCheckBox = QCheckBox(self.configTab)
        self.RLDCH1NCheckBox.setObjectName(u"RLDCH1NCheckBox")
        self.RLDCH1NCheckBox.setGeometry(QRect(190, 300, 21, 27))
        self.label_20 = QLabel(self.configTab)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(220, 300, 41, 21))
        self.RLDCH2PCheckBox = QCheckBox(self.configTab)
        self.RLDCH2PCheckBox.setObjectName(u"RLDCH2PCheckBox")
        self.RLDCH2PCheckBox.setGeometry(QRect(270, 300, 21, 27))
        self.label_21 = QLabel(self.configTab)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(310, 300, 41, 21))
        self.RLDCH2NCheckBox = QCheckBox(self.configTab)
        self.RLDCH2NCheckBox.setObjectName(u"RLDCH2NCheckBox")
        self.RLDCH2NCheckBox.setGeometry(QRect(360, 300, 21, 27))
        self.pulseLineEdit_1 = QLineEdit(self.configTab)
        self.pulseLineEdit_1.setObjectName(u"pulseLineEdit_1")
        self.pulseLineEdit_1.setGeometry(QRect(360, 380, 113, 29))
        self.pulseLineEdit_2 = QLineEdit(self.configTab)
        self.pulseLineEdit_2.setObjectName(u"pulseLineEdit_2")
        self.pulseLineEdit_2.setGeometry(QRect(360, 420, 113, 29))
        self.label_10 = QLabel(self.configTab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(290, 380, 63, 21))
        self.label_11 = QLabel(self.configTab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(290, 420, 63, 21))
        self.tabWidget.addTab(self.configTab, "")
        self.logTab = QWidget()
        self.logTab.setObjectName(u"logTab")
        self.debugCheckBox = QCheckBox(self.logTab)
        self.debugCheckBox.setObjectName(u"debugCheckBox")
        self.debugCheckBox.setGeometry(QRect(820, 490, 71, 27))
        self.logOutput = QTextEdit(self.logTab)
        self.logOutput.setObjectName(u"logOutput")
        self.logOutput.setGeometry(QRect(10, 20, 800, 500))
        self.logOutput.setMaximumSize(QSize(800, 500))
        self.receiverCheckBox = QCheckBox(self.logTab)
        self.receiverCheckBox.setObjectName(u"receiverCheckBox")
        self.receiverCheckBox.setGeometry(QRect(820, 450, 101, 27))
        self.transmitterCheckBox = QCheckBox(self.logTab)
        self.transmitterCheckBox.setObjectName(u"transmitterCheckBox")
        self.transmitterCheckBox.setGeometry(QRect(820, 410, 111, 27))
        self.tabWidget.addTab(self.logTab, "")
        self.plotTab = QWidget()
        self.plotTab.setObjectName(u"plotTab")
        self.plotLayout = QVBoxLayout(self.plotTab)
        self.plotLayout.setObjectName(u"plotLayout")
        self.tabWidget.addTab(self.plotTab, "")
        self.spectrogramTab = QWidget()
        self.spectrogramTab.setObjectName(u"spectrogramTab")
        self.spectrogramLayout = QVBoxLayout(self.spectrogramTab)
        self.spectrogramLayout.setObjectName(u"spectrogramLayout")
        self.tabWidget.addTab(self.spectrogramTab, "")
        self.filterTab = QWidget()
        self.filterTab.setObjectName(u"filterTab")
        self.tabWidget.addTab(self.filterTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.darkModeCheckBox = QCheckBox(self.settingsTab)
        self.darkModeCheckBox.setObjectName(u"darkModeCheckBox")
        self.darkModeCheckBox.setGeometry(QRect(20, 20, 111, 27))
        self.CMV1_CheckBox = QCheckBox(self.settingsTab)
        self.CMV1_CheckBox.setObjectName(u"CMV1_CheckBox")
        self.CMV1_CheckBox.setGeometry(QRect(20, 90, 21, 27))
        self.label_14 = QLabel(self.settingsTab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(50, 90, 61, 21))
        self.CMV2_CheckBox = QCheckBox(self.settingsTab)
        self.CMV2_CheckBox.setObjectName(u"CMV2_CheckBox")
        self.CMV2_CheckBox.setGeometry(QRect(20, 120, 21, 27))
        self.label_15 = QLabel(self.settingsTab)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(50, 120, 61, 21))
        self.tabWidget.addTab(self.settingsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1039, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtablewidgetitem = self.registerReadTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Reg_val", None));
        ___qtablewidgetitem1 = self.registerReadTable.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem2 = self.registerReadTable.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"CONFIG1", None));
        ___qtablewidgetitem3 = self.registerReadTable.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"CONFIG2", None));
        ___qtablewidgetitem4 = self.registerReadTable.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"LOFF", None));
        ___qtablewidgetitem5 = self.registerReadTable.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"CH1SET", None));
        ___qtablewidgetitem6 = self.registerReadTable.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"CH2SET", None));
        ___qtablewidgetitem7 = self.registerReadTable.verticalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"RLD_SENS", None));
        ___qtablewidgetitem8 = self.registerReadTable.verticalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"LOFF_SENS", None));
        ___qtablewidgetitem9 = self.registerReadTable.verticalHeaderItem(8)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"LOFF_STAT", None));
        ___qtablewidgetitem10 = self.registerReadTable.verticalHeaderItem(9)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"RESP1", None));
        ___qtablewidgetitem11 = self.registerReadTable.verticalHeaderItem(10)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"RESP2", None));
        ___qtablewidgetitem12 = self.registerReadTable.verticalHeaderItem(11)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"GPIO", None));
        self.modeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Off", None))
        self.modeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"On", None))
        self.modeComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Test", None))

        self.channel1ComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.channel1ComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.channel1ComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.channel1ComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.channel1ComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"6", None))
        self.channel1ComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"8", None))
        self.channel1ComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"12", None))

        self.channel2ComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.channel2ComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.channel2ComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.channel2ComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.channel2ComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"6", None))
        self.channel2ComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"8", None))
        self.channel2ComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"12", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Register values from device", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Channel 1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Channel 2", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Bitrate", None))
        self.bitrateComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"125", None))
        self.bitrateComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"250", None))
        self.bitrateComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"500", None))
        self.bitrateComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"1000", None))
        self.bitrateComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"2000", None))
        self.bitrateComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"4000", None))
        self.bitrateComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"8000", None))

        self.saveParamsPushButton.setText(QCoreApplication.translate("MainWindow", u"Set Params", None))
        self.setRegisterComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"ID", None))
        self.setRegisterComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"CONFIG1", None))
        self.setRegisterComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"CONFIG2", None))
        self.setRegisterComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"LOFF", None))
        self.setRegisterComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"CH1SET", None))
        self.setRegisterComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"CH2SET", None))
        self.setRegisterComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"RLD_SENS", None))
        self.setRegisterComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"LOFF_SENS", None))
        self.setRegisterComboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"LOFF_STAT", None))
        self.setRegisterComboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"RESP1", None))
        self.setRegisterComboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"RESP2", None))
        self.setRegisterComboBox.setItemText(11, QCoreApplication.translate("MainWindow", u"GPIO", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Register name", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Register value", None))
        self.saveRegisterPushButton.setText(QCoreApplication.translate("MainWindow", u"Set Register", None))
        self.channel1CheckBox.setText("")
        self.channel2CheckBox.setText("")
        self.RLDCH1PCheckBox.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"RLD", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"CH1P", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"CH1N", None))
        self.RLDCH1NCheckBox.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"CH2P", None))
        self.RLDCH2PCheckBox.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"CH2N", None))
        self.RLDCH2NCheckBox.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"HR, CH1", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"HR, CH2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configTab), QCoreApplication.translate("MainWindow", u"Config", None))
        self.debugCheckBox.setText(QCoreApplication.translate("MainWindow", u"Debug", None))
        self.receiverCheckBox.setText(QCoreApplication.translate("MainWindow", u"Receiver", None))
        self.transmitterCheckBox.setText(QCoreApplication.translate("MainWindow", u"Transmitter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), QCoreApplication.translate("MainWindow", u"Log", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), QCoreApplication.translate("MainWindow", u"Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spectrogramTab), QCoreApplication.translate("MainWindow", u"Spectrogram", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filterTab), QCoreApplication.translate("MainWindow", u"Filters", None))
        self.darkModeCheckBox.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.CMV1_CheckBox.setText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"CM CH1", None))
        self.CMV2_CheckBox.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"CM CH2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

