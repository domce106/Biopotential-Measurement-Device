from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import numpy as np
import scipy.signal
from collections import deque

class PulseCalculator(QObject):
    # Signal to send out heart rate
    heartRateCalculated = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.sampling_rate = None
        self.buffer = deque(maxlen=4096)  # Buffer to store ECG signal chunks

    def add_to_buffer(self, ecg_signal_chunk):
        # Add new ECG signal chunk to the buffer
        self.buffer.extend(ecg_signal_chunk)

    def detect_r_peaks(self):
        # Detect peaks with a minimum height and distance
        ecg_signal = np.array(self.buffer)
        peaks, _ = scipy.signal.find_peaks(ecg_signal, height=np.max(ecg_signal)/4, distance=self.sampling_rate/2)
        return peaks

    def calculate_rr_intervals(self, peaks):
        # Calculate time differences between consecutive peaks
        rr_intervals = np.diff(peaks) / self.sampling_rate
        return rr_intervals

    def calculate_heart_rate(self, rr_intervals):
        # Calculate the average heart rate
        if len(rr_intervals) == 0:
            return 0
        average_rr_interval = np.mean(rr_intervals)
        heart_rate = 60 / average_rr_interval  # Convert to beats per minute
        return heart_rate

    @pyqtSlot(np.ndarray, int)
    def process_ecg_signal(self, ecg_signal_chunk, bitrate):
        # Process ECG signal chunk to find heart rate
        if self.sampling_rate != bitrate:
            # If the bitrate has changed, clear the buffer
            self.buffer.clear()
        self.sampling_rate = bitrate
        self.add_to_buffer(ecg_signal_chunk)
        peaks = self.detect_r_peaks()
        rr_intervals = self.calculate_rr_intervals(peaks)
        heart_rate = self.calculate_heart_rate(rr_intervals)
        self.heartRateCalculated.emit(heart_rate)