from PyQt6.QtCore import QThread, pyqtSignal
from queue import Queue
from datetime import datetime

class Logger(QThread):
    
#Signals
    logMessageToGui = pyqtSignal(str)
    
#Constructor

    def __init__(self):
        super().__init__()
        
    #Attributes
        self.debug_mode = False
        self.transmission_mode = False
        self.receiver_mode = False
        self.queue = Queue()
        self.start()
        
    #Methods

    def run(self):
        while True:
            message = self.queue.get()
            if message is None:  # None is used as a sentinel to stop the thread
                self.logMessageToGui.emit("Logger stopped.")
                break
            self.logMessageToGui.emit(message)
            
    def log(self, message, message_type='INFO'):
        if message_type == 'INFO':
            self.info(message)
        elif message_type == 'DEBUG':
            self.debug(message)
        elif message_type == 'ERROR':
            self.error(message)
        elif message_type == 'TRANSMISSION':
            self.transmission(message)
        elif message_type == 'RECEIVER':
            self.receiver(message)
        else:
            self.log_message('UNKNOWN', message)

    def log_message(self, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        formatted_message = f'{timestamp} - {level}: {message}'
        self.queue.put(formatted_message)

    def info(self, message):
        self.log_message('INFO', message)

    def debug(self, message):
        if self.debug_mode:
            self.log_message('DEBUG', message)
            
    def error(self, message):
        self.log_message('ERROR', message)
        
    def transmission(self, message):
        if self.transmission_mode:
            self.log_message('TRANSMISSION', message)
            
    def receiver(self, message):
        if self.receiver_mode:
            self.log_message('RECEIVER', message)

    def stop(self):
        self.queue.put(None)  # Put None in the queue to stop the thread
        
global_logger = Logger()