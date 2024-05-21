from PyQt6.QtCore import pyqtSlot, QTimer

from ui.main_window import MainWindow
from .logger import Logger
from interfaces.device_communicator.device_communicator import DeviceCommunicator
from interfaces.calculator.measurement_data_handler import MeasurementDataHandler
from interfaces.save_to_file.save_data import SaveData
from interfaces.calculator.pulse_calculator import PulseCalculator

class Interface:
    def __init__(self):
        super().__init__()
        
    #Atributes
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        
        self.logger = Logger()
        self.device_communicator = DeviceCommunicator()
        self.measurement_data_handler = MeasurementDataHandler()
        self.save_data = SaveData()
        self.pulse_calculator1 = PulseCalculator()
        self.pulse_calculator2 = PulseCalculator()
        
    #Connections
        self.mainWindow.paramsChanged.connect(self.device_communicator.senderInst.set_work_parameters)
        self.device_communicator.receiverInst.status_parameters_signal.connect(self.mainWindow.receive_parameters)
        self.device_communicator.receiverInst.status_registers_signal.connect(self.mainWindow.receive_registers)
        self.mainWindow.registerChanged.connect(self.device_communicator.senderInst.set_register)
        self.device_communicator.receiverInst.measurement_data_signal.connect(self.measurement_data_handler.on_measurement_data_received)
        self.measurement_data_handler.temporal_data_signal_1.connect(self.mainWindow.plotWidget1.add_data)
        self.measurement_data_handler.temporal_data_signal_2.connect(self.mainWindow.plotWidget2.add_data)
        self.mainWindow.clearPlotSignal.connect(self.mainWindow.plotWidget1.clear_plot)
        self.mainWindow.clearPlotSignal.connect(self.mainWindow.plotWidget2.clear_plot)
        
        self.mainWindow.paramsChanged.connect(self.save_data.create_new_file_slot)
        self.measurement_data_handler.temporal_data_signal_1.connect(self.save_data.append_data_channel_1)
        self.measurement_data_handler.temporal_data_signal_2.connect(self.save_data.append_data_channel_2)
        
        self.measurement_data_handler.spectral_data_signal_1.connect(self.mainWindow.spectrogramWidget1.update_spectrogram)
        self.measurement_data_handler.spectral_data_signal_2.connect(self.mainWindow.spectrogramWidget2.update_spectrogram)
        
        self.mainWindow.filter_editor.filterDataChanged.connect(self.measurement_data_handler.change_filters)
        
        self.measurement_data_handler.temporal_data_signal_1.connect(self.pulse_calculator1.process_ecg_signal)
        self.measurement_data_handler.temporal_data_signal_2.connect(self.pulse_calculator2.process_ecg_signal)
        
        self.pulse_calculator1.heartRateCalculated.connect(self.mainWindow.display_heart_rate_1)
        self.pulse_calculator2.heartRateCalculated.connect(self.mainWindow.display_heart_rate_2)
        
        self.mainWindow.CMVCheckBoxesChanged.connect(self.measurement_data_handler.on_CMVCheckBoxes_state_changed)
    #Methods
    
    