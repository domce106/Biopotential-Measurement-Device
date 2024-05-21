from PyQt6.QtCore import pyqtSlot, QObject
import os
import time
import numpy as np

class SaveData(QObject):

    def __init__(self):
        super().__init__()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.file1 = None
        self.file2 = None
        self.create_new_file(timestamp)

    @pyqtSlot(object)
    def append_data_channel_1(self, data):
        if self.file1:
            self.file1.write('\n'.join(map(str, data)) + '\n')

    @pyqtSlot(object)
    def append_data_channel_2(self, data):
        if self.file2:
            self.file2.write('\n'.join(map(str, data)) + '\n')

    @pyqtSlot(np.ndarray)
    def create_new_file_slot(self, params):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.create_new_file(timestamp)

    def create_new_file(self, filename):
        if self.file1:
            self.file1.close()
        if self.file2:
            self.file2.close()

        # Check if the directory exists, if not, create it
        if not os.path.exists('data'):
            os.makedirs('data')

        self.file1 = open(os.path.join('data', filename + '_1.txt'), 'w')
        self.file2 = open(os.path.join('data', filename + '_2.txt'), 'w')