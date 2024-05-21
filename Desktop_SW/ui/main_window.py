from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMessageBox, QSplitter, QVBoxLayout
import numpy as np
from interfaces.logger import global_logger
from ui.plot_widget import PlotWidget
from ui.spectrogram_widget import SpectrogramWidget
from ui.filter_editor import FilterEditor

class MainWindow(QtWidgets.QMainWindow):
#Signals
    paramsChanged = QtCore.pyqtSignal(np.ndarray)
    registerChanged = QtCore.pyqtSignal(str, str)
    clearPlotSignal = QtCore.pyqtSignal()
    CMVCheckBoxesChanged = QtCore.pyqtSignal(list)
    
#Init
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("ui/mainwindow.ui", self)
        
        self.filter_editor = FilterEditor(self)
        self.ui.filterTab.setLayout(QVBoxLayout())
        self.ui.filterTab.layout().addWidget(self.filter_editor)
        
        # Create two plot widgets for the two channels
        self.plotWidget1 = PlotWidget(self.plotTab)
        self.plotWidget2 = PlotWidget(self.plotTab)

        # Create a vertical splitter
        self.splitter = QSplitter(QtCore.Qt.Orientation.Vertical, self.plotTab)

        # Add the plot widgets to the splitter
        self.splitter.addWidget(self.plotWidget1)
        self.splitter.addWidget(self.plotWidget2)

        # Add the splitter to the plot layout
        self.plotLayout.addWidget(self.splitter)
        
        # Create two spectrogram widgets for the two channels
        self.spectrogramWidget1 = SpectrogramWidget(self.spectrogramTab)
        self.spectrogramWidget2 = SpectrogramWidget(self.spectrogramTab)

        # Create a vertical splitter
        self.splitter = QSplitter(QtCore.Qt.Orientation.Vertical, self.spectrogramTab)

        # Add the spectrogram widgets to the splitter
        self.splitter.addWidget(self.spectrogramWidget1)
        self.splitter.addWidget(self.spectrogramWidget2)

        # Add the splitter to the spectrogram layout
        self.spectrogramLayout.addWidget(self.splitter)
#Atributes

        
        
#Connections
        self.debugCheckBox.stateChanged.connect(self.toggle_debug_mode)
        self.receiverCheckBox.stateChanged.connect(self.toggle_receiver_mode)
        self.transmitterCheckBox.stateChanged.connect(self.toggle_transmitter_mode)
        
        global_logger.logMessageToGui.connect(self.log_message)
        
        self.darkModeCheckBox.stateChanged.connect(self.toggle_theme)
        self.saveParamsPushButton.clicked.connect(self.save_parameters)
        self.saveRegisterPushButton.clicked.connect(self.save_registers)
        
        self.CMV1_CheckBox.stateChanged.connect(self.CMV_CheckBoxes_state_changed)
        self.CMV2_CheckBox.stateChanged.connect(self.CMV_CheckBoxes_state_changed)
    
        
#Methods

    def toggle_debug_mode(self, state):
        global_logger.debug_mode = state == 2
        if global_logger.debug_mode:
            global_logger.log("Debug mode enabled")
        else:
            global_logger.log("Debug mode disabled")
            
    def toggle_receiver_mode(self, state):
        global_logger.receiver_mode = state == 2
        if global_logger.receiver_mode:
            global_logger.log("Receiver mode enabled")
        else:
            global_logger.log("Receiver mode disabled")
            
    def toggle_transmitter_mode(self, state):
        global_logger.transmission_mode = state == 2
        if global_logger.transmission_mode:
            global_logger.log("Transmitter mode enabled")
        else:
            global_logger.log("Transmitter mode disabled")

    def log_message(self, message):
        self.logOutput.append(message)
        
    def toggle_theme(self, state):
        if state == 2:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_dark_theme(self):
            style = """
            QWidget {
                background-color: #2b2b2b;
            }
            QLabel, QPushButton, QTextEdit, QComboBox, QLineEdit, QTableWidget, QCheckBox {
                color: #ffffff;
            }
            QTextEdit, QLineEdit, QTableWidget {
                background-color: #353535;
            }
            QHeaderView::section, QTableCornerButton::section {
                background-color: #353535;
                color: #ffffff;
            }
            """
            self.setStyleSheet(style)
            
    def set_light_theme(self):
        style = """
        QWidget {
            background-color: #f0f0f0;
            color: #000000;
        }
        QTextEdit, QLineEdit, QTableWidget {
            background-color: #ffffff;
        }
        QLabel, QPushButton, QTextEdit, QComboBox, QLineEdit, QTableWidget, QCheckBox {
            color: #000000;
        }
        QHeaderView::section, QTableCornerButton::section {
            background-color: #f0f0f0;
            color: #000000;
        }
        """
        self.setStyleSheet(style)
            
#Socket methods

    @pyqtSlot(dict)
    def receive_parameters(self, parameters):
        measurement_status = parameters['measurement_status']
        if measurement_status == 0:
            self.modeLineEdit.setText("Off")
        elif measurement_status == 1:
            self.modeLineEdit.setText("Test")
        elif measurement_status == 2:
            self.modeLineEdit.setText("On")
        else:
            self.modeLineEdit.setText("Unknown")
            
        channel_status = parameters['channel_status']
        if channel_status == 0:
            self.channel1LineEdit.setText("Off")
            self.channel2LineEdit.setText("Off")
        elif channel_status == 1:
            self.channel1LineEdit.setText("On")
            self.channel2LineEdit.setText("Off")
        elif channel_status == 2:
            self.channel1LineEdit.setText("Off")
            self.channel2LineEdit.setText("On")
        elif channel_status == 3:
            self.channel1LineEdit.setText("On")
            self.channel2LineEdit.setText("On")
        else:
            self.channel1LineEdit.setText("Unknown")
            self.channel2LineEdit.setText("Unknown")
        
        bitrate = parameters['bitrate']
        self.bitrateLineEdit.setText(str(bitrate))
        
        gain_1 = parameters['gain_1']
        self.append_to_line_edit(self.channel1LineEdit, f" -- Gain: {gain_1}")
        
        gain_2 = parameters['gain_2']
        self.append_to_line_edit(self.channel2LineEdit, f" -- Gain: {gain_2}")
        
    def append_to_line_edit(self, line_edit, text_to_append):
        current_text = line_edit.text()
        new_text = current_text + text_to_append
        line_edit.setText(new_text)
        
    @pyqtSlot(dict)
    def receive_registers(self, registers):
        for key, value in registers.items():
            for i in range(self.registerReadTable.rowCount()):
                row_name_item = self.registerReadTable.verticalHeaderItem(i)
                if row_name_item is not None:
                    row_name = row_name_item.text()
                    if row_name == key:
                        # Convert value to binary, ensure it's 8 digits, and remove the '0b' prefix
                        binary_value = format(value, '08b')
                        # Insert a space after every 4 digits
                        binary_value = binary_value[:4] + ' ' + binary_value[4:]
                        # Subtract 1 from the row index when setting the item
                        self.registerReadTable.setItem(i - 1, 1, QtWidgets.QTableWidgetItem(binary_value))
        
            
# Emit methods

    def save_parameters(self):
        params = np.empty(0, dtype=np.uint32)
        mode = self.modeComboBox.currentText()
        if mode == "Off":
            params = np.append(params, 0)
        elif mode == "On":
            params = np.append(params, 2)
        elif mode == "Test":
            params = np.append(params, 1)
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Invalid mode.")
            return
        
        channelStatus = 0
        if self.channel1CheckBox.isChecked():
            channelStatus = channelStatus | 1
        if self.channel2CheckBox.isChecked():
            channelStatus = channelStatus | 2
        params = np.append(params, channelStatus)
        
        bitrate = self.bitrateComboBox.currentText()
        params = np.append(params, int(bitrate))
        
        channel_1 = self.channel1ComboBox.currentText()
        channel_2 = self.channel2ComboBox.currentText()
        params = np.append(params, int(channel_1))
        params = np.append(params, int(channel_2))
        
        rld = 0
        if self.RLDCH1PCheckBox.isChecked():
            rld = rld | 1
        if self.RLDCH1NCheckBox.isChecked():
            rld = rld | 2
        if self.RLDCH2PCheckBox.isChecked():
            rld = rld | 4
        if self.RLDCH2NCheckBox.isChecked():
            rld = rld | 8
        params = np.append(params, rld)
        
        self.paramsChanged.emit(params)
        
        self.clearPlotSignal.emit()
        

    def save_registers(self):
        register_name = self.setRegisterComboBox.currentText()
        register_value = self.setRegisterLineEdit.text()

        # Check if exactly eight characters were entered
        if len(register_value) == 8:
            self.registerChanged.emit(register_name, register_value)
        else:
            # Create a QMessageBox to display the error message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.warning)
            msg.setText("Invalid input")
            msg.setInformativeText("Please enter exactly eight characters.")
            msg.setWindowTitle("Error")
            msg.exec_()
    
    @pyqtSlot(float)        
    def display_heart_rate_1(self, heart_rate):
        if 0 <= heart_rate <= 500:
            self.pulseLineEdit_1.setText("{:.1f}".format(heart_rate))  # Display heart rate with one decimal place
        else:
            self.pulseLineEdit_1.setText("NaN")  # Display 'NaN' if heart rate is outside the range
    
    @pyqtSlot(float)    
    def display_heart_rate_2(self, heart_rate):
        if 0 <= heart_rate <= 500:
            self.pulseLineEdit_2.setText("{:.1f}".format(heart_rate))  # Display heart rate with one decimal place
        else:
            self.pulseLineEdit_2.setText("NaN")  # Display 'NaN' if heart rate is outside the range
        
    @pyqtSlot(int)
    def CMV_CheckBoxes_state_changed(self, state):
        CMV1_state = self.ui.CMV1_CheckBox.isChecked()
        CMV2_state = self.ui.CMV2_CheckBox.isChecked()
        self.CMVCheckBoxesChanged.emit([CMV1_state, CMV2_state])
        



        
        