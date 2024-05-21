from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QByteArray
import numpy as np
from interfaces.logger import global_logger

class Receiver(QObject):
#Signals
    board_info_signal = pyqtSignal(dict)
    status_parameters_signal = pyqtSignal(dict)
    status_registers_signal = pyqtSignal(dict)
    measurement_data_signal = pyqtSignal(dict, list)
    
#Constructor
    def __init__(self):
        super().__init__()

    @pyqtSlot(QByteArray)
    def on_data_received(self, data: QByteArray):
        # Convert QByteArray to bytes
        data_bytes = bytes(data)
        # Convert every four bytes to a uint32 value
        data_uint32 = [int.from_bytes(data_bytes[i:i+4], byteorder='big') for i in range(0, len(data_bytes), 4)]

        self.parse_data(data_uint32)

    def parse_data(self, data):
        # The first element of the data array is the message type
        message_type = data[0]
        if message_type == 0x02:
            self.parse_board_id(data)
        elif message_type == 0x04:
            self.parse_status(data)
        elif message_type == 0x06:
            self.parse_status_send_period_set(data)
        elif message_type == 0x08:
            self.parse_work_parameter_set(data)
        elif message_type == 0x0A:
            self.parse_measurement_data(data)
        else:
            print(f"Unknown message type: {message_type}")
            
    def parse_board_id(self, data):
        # Assuming that the board number, hardware version, and software version
        # are the second, third, and fourth elements of the data array
        self.board_info = {
            'board_number': data[1],
            'hardware_version': data[2],
            'software_version': data[3],
        }
        self.board_info_signal.emit(self.board_info)
        global_logger.log(f"Board ID received: {self.board_info}", 'RECEIVER')
    
    def parse_status(self, data):
        self.status_parameters = {
            'board_number': data[1],
            'measurement_status': data[2],
            'channel_status': data[3],
            'bitrate': data[4],
            'gain_1': data[5],
            'gain_2': data[6],
        }
        
        self.status_registers = {
            "ID": data[7],
            "CONFIG1": data[8],
            "CONFIG2": data[9],
            "LOFF": data[10],
            "CH1SET": data[11],
            "CH2SET": data[12],
            "RLD_SENS": data[13],
            "LOFF_SENS": data[14],
            "LOFF_STAT": data[15],
            "RESP1": data[16],
            "RESP2": data[17],
            "GPIO": data[18],
        }
        self.status_parameters_signal.emit(self.status_parameters)
        self.status_registers_signal.emit(self.status_registers)
        global_logger.log(f"Status received: {self.status_parameters}, {self.status_registers}", 'RECEIVER')
        
    def parse_status_send_period_set(self, data):
        if data[2] != 0:
            global_logger.log("Send period set failed.", 'ERROR')
        else:
            global_logger.log("Send period set successfully.", 'INFO')
    
    def parse_work_parameter_set(self, data):
        if data[2] != 0:
            global_logger.log("Work parameter set failed.", 'ERROR')
        else:
            global_logger.log("Work parameter set successfully.", 'INFO')
            
    def parse_measurement_data(self, data):
        self.measurement_parameters = {
            'board_number': data[1],
            'channel_number': data[2],
            'bitrate': data[3],
            'gain': data[4],
            'packet_number': data[5],
            'measurement_count': data[6]
        }
        self.measurement_data = data[7:]
        global_logger.log(f"Measurement data received: Packet -- {self.measurement_parameters['packet_number']}, channel -- {self.measurement_parameters['channel_number']}", 'RECEIVER')
        self.measurement_data_signal.emit(self.measurement_parameters, self.measurement_data)
        
        
        
        
        
        