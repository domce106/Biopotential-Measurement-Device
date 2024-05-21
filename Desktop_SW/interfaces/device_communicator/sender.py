from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
import numpy as np
from interfaces.logger import global_logger
from assets.ads1292_registers import ads1292Registers

class Sender(QObject):
    send_message_signal = pyqtSignal(bytes)
    
    def __init__(self):
        super().__init__()
        
    def send_message(self, message):
        message = np.array(message, dtype=np.uint32)
        packed_message = self.pack_data(message)
        print(f"Packed message: {packed_message}")
        self.send_message_signal.emit(packed_message)
        
    def pack_data(self, data):
        data_uint8 = np.zeros(4 * len(data), dtype=np.uint8)
        for i, value in enumerate(data):
            data_uint8[4*i] = value >> 24 & 0xff
            data_uint8[4*i + 1] = value >> 16 & 0xff
            data_uint8[4*i + 2] = value >> 8 & 0xff
            data_uint8[4*i + 3] = value & 0xff
        packed_data = data_uint8.tobytes()
        return packed_data
        
    def request_board_id(self):
        data = np.array([0x01])
        self.send_message(data)
        global_logger.log("Request board ID sent.", 'TRANSMISSION')
        
    def request_status(self):
        data = np.array([0x03])
        self.send_message(data)
        global_logger.log("Request status sent.", 'TRANSMISSION')
        
    @pyqtSlot(int)    
    def set_status_send_period(self, period):
        data = np.array([0x05])
        data = np.append(data, period)
        self.send_message(data)
        global_logger.log(f"Set status send period to {period}.", 'TRANSMISSION')
    
    @pyqtSlot(np.ndarray)    
    def set_work_parameters(self, work_parameters):
        data = np.array([0x07])
        data = np.append(data, work_parameters)
        print(f"Data: {data}")
        self.send_message(data)
        global_logger.log(f"Set work parameters to {work_parameters}.", 'TRANSMISSION')
    
    @pyqtSlot(str, str)    
    def set_register(self, register_name, register_value):
        data = np.array([0x0B], dtype=np.uint8)
        register_address = ads1292Registers.get(register_name)
        data = np.append(data, np.uint8(register_address))
        data = np.append(data, np.uint8(int(register_value, 2)))
        print(np.uint8(int(register_value, 2)))
        print(f"Data: {data}")
        self.send_message(data)
        global_logger.log(f"Set register {register_name} to {register_value}.", 'TRANSMISSION')