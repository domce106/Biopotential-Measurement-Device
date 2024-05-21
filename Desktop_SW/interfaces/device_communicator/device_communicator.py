from PyQt6.QtCore import QTimer, QObject, QThread, pyqtSlot, QMetaObject, Q_ARG
from interfaces.device_communicator.udp_server import UDPServer
from interfaces.device_communicator.sender import Sender
from interfaces.device_communicator.receiver import Receiver
from interfaces.logger import global_logger

class DeviceCommunicator(QObject):
    def __init__(self):
        super().__init__()
        self.udp_server = UDPServer()
        self.senderInst = Sender()
        self.receiverInst = Receiver()
        self.device_connected = False
        self.pingFrequency = 1000 #miliseconds
        
# Connections
        self.senderInst.send_message_signal.connect(self.udp_server.udp_sender.send_data)
        self.udp_server.udp_receiver.connection_established.connect(self.connection_established)
        self.udp_server.udp_receiver.connection_lost.connect(self.connection_lost)
        self.udp_server.udp_receiver.data_received.connect(self.receiverInst.on_data_received)
        
# Connections end
        self.device_pinger()
        
# Methods
    def connection_established(self):
        self.device_connected = True
        self.senderInst.request_board_id()
        QTimer.singleShot(1000, self.senderInst.request_status)
        
    def connection_lost(self):
        self.device_connected = False
        global_logger.log("Connection lost. Attempting to reconnect.")
        
    def device_pinger(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.ping_device)
        self.timer.start(self.pingFrequency)  # QTimer expects milliseconds

    def ping_device(self):
        try:
            # This method will be called every pingFrequency seconds
            # Only ping the device if it's not connected
            if not self.device_connected:
                self.senderInst.request_board_id()
        except Exception as e:
            global_logger.log(f"An error occurred while pinging the device: {e}", "ERROR")

        
        