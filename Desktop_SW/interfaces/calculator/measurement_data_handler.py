from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
import numpy as np
from interfaces.logger import global_logger
from interfaces.calculator.filter_handler import FilterHandler
from scipy.signal import windows

class MeasurementDataHandler(QObject):
    temporal_data_signal_1 = pyqtSignal(np.ndarray, int)
    temporal_data_signal_2 = pyqtSignal(np.ndarray, int)
    spectral_data_signal_1 = pyqtSignal(np.ndarray, np.ndarray)  # Signal for emitting STFT results for channel 1
    spectral_data_signal_2 = pyqtSignal(np.ndarray, np.ndarray)  # Signal for emitting STFT results for channel 2
    
    def __init__(self):
        super().__init__()
        self.measurement_data = MeasurementData(1000)
        self.filter_handlers = {1: FilterHandler(), 2: FilterHandler()}
        self.old_chunk = {1: np.array([]), 2: np.array([])}
        
        self.CMVCheckBoxesState = [False, False]  # New attribute to store the checkboxes' states

    @pyqtSlot(dict, list)
    def on_measurement_data_received(self, measurement_parameters, measurement_data):
        self.measurement_data.input_data(measurement_parameters, measurement_data, self.CMVCheckBoxesState)
        channel = self.measurement_data.channel_number
        filtered_data = self.filter_handlers[channel].apply_filters(self.measurement_data.data, self.measurement_data.bitrate)

        # Emit temporal data
        if channel == 1:
            self.temporal_data_signal_1.emit(filtered_data, self.measurement_data.bitrate)
            self.calculate_and_emit_fft(filtered_data, self.measurement_data.bitrate, 1)
        elif channel == 2:
            self.temporal_data_signal_2.emit(filtered_data, self.measurement_data.bitrate)
            self.calculate_and_emit_fft(filtered_data, self.measurement_data.bitrate, 2)
        else:
            global_logger.log("Invalid channel number", 'ERROR')
    
    @pyqtSlot(list)        
    def change_filters(self, filters_list):
        for filter_handler in self.filter_handlers.values():
            filter_handler.change_filters(filters_list)
    
    def calculate_and_emit_fft(self, new_chunk, fs, channel):
        # Define your target length for consistent input size
        target_length = 8192
    
        # Apply windowing to new data
        windowed_new_chunk = self.apply_windowing(new_chunk)
    
        # If there is no old chunk for this channel, save the second half of the new chunk as the old chunk and return
        if len(self.old_chunk[channel]) == 0:
            self.old_chunk[channel] = self.get_second_half(windowed_new_chunk)
            return
    
        # Concatenate the old chunk and the first half of the new chunk
        data = self.concatenate_chunks(self.old_chunk[channel], self.get_first_half(windowed_new_chunk))
    
        # Save the second half of the new chunk as the old chunk for the next calculation
        self.old_chunk[channel] = self.get_second_half(windowed_new_chunk)
    
        # Zero padding to ensure a consistent input size
        padded_data = self.zero_padding(data, target_length)
    
        # Compute FFT
        Zxx = self.compute_fft(padded_data, target_length, fs)
    
        # Scale and correct the FFT results
        Zxx_magnitude = self.scale_and_correct_fft(Zxx, data)
    
        # Emit the FFT results based on channel
        self.emit_fft_results(Zxx_magnitude, channel)

    def get_first_half(self, chunk):
        return chunk[:len(chunk)//2]

    def concatenate_chunks(self, old_chunk, new_chunk):
        return np.concatenate((old_chunk, new_chunk))

    def get_second_half(self, chunk):
        return chunk[len(chunk)//2:]

    def zero_padding(self, data, target_length):
        return np.pad(data, (0, max(0, target_length - len(data))), mode='constant', constant_values=0)

    def apply_windowing(self, data):
        window = windows.hann(len(data))
        return data * window

    def compute_fft(self, data, target_length, fs):
        return np.fft.rfft(data)

    def scale_and_correct_fft(self, Zxx, data):
        Zxx_magnitude = np.abs(Zxx)
        window_gain = np.sum(windows.hann(len(data))**2)
        Zxx_magnitude /= window_gain
        Zxx_magnitude[1:-1] *= 2
        Zxx_magnitude /= len(data)
        # Convert to power spectral density in dB/Hz
        fs = self.measurement_data.bitrate
        df = fs / len(data)
        Zxx_magnitude = 10 * np.log10(Zxx_magnitude / df)
        return Zxx_magnitude
    
    def emit_fft_results(self, Zxx_magnitude, channel):
        N = 2*len(Zxx_magnitude)
        fs = self.measurement_data.bitrate
        freq_bins = np.fft.rfftfreq(N, 1/fs)

        if channel == 1:
            self.spectral_data_signal_1.emit(Zxx_magnitude, freq_bins)
        elif channel == 2:
            self.spectral_data_signal_2.emit(Zxx_magnitude, freq_bins)
            
    @pyqtSlot(list)
    def on_CMVCheckBoxes_state_changed(self, state_list):
        self.CMVCheckBoxesState = state_list
        
class MeasurementData:
    
    def __init__(self, size = 1000):
        super().__init__()
        self.channel_number = 0
        self.bitrate = 0
        self.gain = 0
        self.measurement_count = 0
        self.data = np.zeros(size)
                
    def input_data(self, parameters, data, CMVCheckBoxesState):
        self.channel_number = int(parameters['channel_number'])
        self.bitrate = int(parameters['bitrate'])
        self.gain = int(parameters['gain'])
        self.measurement_count = int(parameters['measurement_count'])
        self.CMVCheckBoxesState = CMVCheckBoxesState
        self.data = self.convert_to_voltage(data, self.gain)

    def convert_to_voltage(self, data, gain):
        voltage_reference = 2.42  # Reference voltage in volts
        # Ensure data is in the correct numpy dtype and view as signed integers
        data = np.array(data, dtype=np.int32)  # Use int32 to handle negative values correctly
        # Convert two's complement manually if necessary
        data[data & 0x800000 != 0] -= 0x1000000  # If the sign bit is set, adjust the value
        # Calculate the voltage
        if self.CMVCheckBoxesState[self.channel_number - 1]:  # Subtract 1 because channel_number starts at 1
            voltage = (data / float(2**23 - 1)) * (voltage_reference / gain) / (1.618)
        else:
            voltage = (data / float(2**23 - 1)) * (voltage_reference / gain)
        return voltage
        