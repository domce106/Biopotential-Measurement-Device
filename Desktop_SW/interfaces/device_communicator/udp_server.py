import socket
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray, pyqtSlot, QThread, QTimer
import numpy as np
from interfaces.logger import global_logger


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

class UDPServer(QObject):
    udp_sender_signal = pyqtSignal(bytes)
    
    
    def __init__(self, port=7757):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcasting
        self.server_address = (get_ip_address(), port)
        self.sock.bind(self.server_address)
        self.client_address = None  # Will be set when a message is received
        global_logger.log(f"Server started on {self.server_address[0]}:{self.server_address[1]}.")

        self.udp_receiver = UDPReceiver(self.sock, self.client_address)
        self.udp_sender = UDPSender(self.sock, self.server_address, self.client_address)
        self.udp_receiver.client_address_updated.connect(self.udp_sender.update_client_address)
        
        # Create the threads
        self.recv_thread = QThread()
        self.send_thread = QThread()

        # Move the objects to the threads
        self.udp_receiver.moveToThread(self.recv_thread)
        self.udp_sender.moveToThread(self.send_thread)

        # Connections
        self.recv_thread.started.connect(self.udp_receiver.run)

        # Start the threads
        self.recv_thread.start()
        self.send_thread.start()
class UDPReceiver(QObject):
    # Signals
    data_received = pyqtSignal(QByteArray)
    connection_established = pyqtSignal()
    connection_lost = pyqtSignal()
    client_address_updated = pyqtSignal(tuple)
    restart_timer_signal = pyqtSignal()

    def __init__(self, sock, client_address=None):
        super().__init__()
        self.sock = sock
        self.client_address = client_address

        # Create a QTimer
        self.timer = QTimer()

        # Connect the QTimer.timeout signal to the reset_client_address slot
        self.timer.timeout.connect(self.reset_client_address)

        # Connect the QThread.started signal to start the timer
        QThread.currentThread().started.connect(self.start_timer)

        # Connect the restart_timer_signal to the start_timer slot
        self.restart_timer_signal.connect(self.start_timer)

    def start_timer(self):
        self.timer.start(15000)  # 15 seconds

    def reset_client_address(self):
        self.client_address = None
        self.connection_lost.emit()

    def run(self):
        while True:
            try:
                data, address = self.sock.recvfrom(4096)
            except socket.error as e:
                global_logger.log(f"Socket error occurred: {e}", 'ERROR')
                continue  # No data available, continue the loop

            # Ignore messages that come from the server's own IP address
            if address[0] == self.sock.getsockname()[0]:
                continue

            # This is the first message received, so save the client's address
            if self.client_address is None:
                self.client_address = address
                self.client_address_updated.emit(self.client_address)
                global_logger.log(f"Connected to client at {address[0]}:{address[1]}.")
                self.connection_established.emit()

            # Emit the restart_timer_signal every time data is received
            self.restart_timer_signal.emit()

            global_logger.log(f"Data received: {data}.", 'RECEIVER')
            self.data_received.emit(data)
class UDPSender(QObject):
    def __init__(self, sock, server_address, client_address=None):
        super().__init__()
        self.sock = sock
        self.server_address = server_address
        self.client_address = client_address

    @pyqtSlot(bytes)
    def send_data(self, data):
        print("send_data method called")
        if self.client_address is not None:
            self.sock.sendto(data, self.client_address)
        else:
            self.sock.sendto(data, ('<broadcast>', self.server_address[1]))
            global_logger.log("No client connected, sending ping message.", 'TRANSMISSION')
        global_logger.log(f"Data sent: {data}.", 'TRANSMISSION')
        
    @pyqtSlot(tuple)
    def update_client_address(self, address):
        self.client_address = address