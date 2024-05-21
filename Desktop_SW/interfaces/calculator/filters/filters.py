import numpy as np
from scipy.signal import butter, lfilter, iirnotch, freqz, medfilt, lfilter_zi
from scipy.stats import zscore
import matplotlib.pyplot as plt
from PyQt6.QtCore import QObject
import pandas as pd

class Filters(QObject):
    def __init__(self):
        super().__init__()
        self.filter_dict = {}  # Dictionary to store filters
        self.moving_avg_state = None
        self.outlier_filter_state = None

    # Overriding magic methods for dictionary-like access
    def __setitem__(self, key, value): self.filter_dict[key] = value
    def __getitem__(self, key): return self.filter_dict[key]
    def __contains__(self, key): return key in self.filter_dict
    def __iter__(self): return iter(self.filter_dict)
    def items(self): return self.filter_dict.items()

    # Lowpass Butterworth filter
    def butter_lowpass(self, data, cutoff, fs, order=5):
        self.validate_parameters(cutoff, fs, order)
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        zi = lfilter_zi(b, a)
        if not hasattr(self, 'lowpass_state'):
            self.lowpass_state = zi
        y, self.lowpass_state = lfilter(b, a, data, zi=self.lowpass_state)
        return y

    # Highpass Butterworth filter
    def butter_highpass(self, data, cutoff, fs, order=5):
        self.validate_parameters(cutoff, fs, order)
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        zi = lfilter_zi(b, a)
        if not hasattr(self, 'highpass_state'):
            self.highpass_state = zi
        y, self.highpass_state = lfilter(b, a, data, zi=self.highpass_state)
        return y

    # Notch filter
    def notch_filter(self, data, freq, Q, fs):
        try:
            self.validate_parameters(freq, fs)
            nyq = 0.5 * fs
            freq = freq / nyq
            b, a = iirnotch(freq, Q)
            zi = lfilter_zi(b, a)
            if not hasattr(self, 'notch_state'):
                self.notch_state = zi
            y, self.notch_state = lfilter(b, a, data, zi=self.notch_state)
            if y is None:
                print("lfilter returned None.")
                return None
            return y
        except Exception as e:
            print(f"Error in notch_filter: {e}")
            return None
    
    def moving_average_filter(self, data, window_size):
        if self.moving_avg_state is not None:
            # Prepend the state (last few values from previous chunk) to the new data
            data = np.concatenate((self.moving_avg_state, data))

        # Calculate moving average
        cumulative_sum = np.cumsum(data, dtype=float)
        moving_avg = (cumulative_sum[window_size:] - cumulative_sum[:-window_size]) / window_size

        # Update the state with the last few data points of the current chunk
        self.moving_avg_state = data[-window_size + 1:]

        # Ensure the output length matches the input data length of the current chunk
        return moving_avg[:len(data) - window_size + 1]

    # Median filter
    def apply_median_filter(self, data, kernel_size=3):
        if kernel_size <= 0 or not isinstance(kernel_size, int):
            raise ValueError("Kernel size must be a positive integer.")
        return medfilt(data, kernel_size)
    
    # Least Mean Squares (LMS) filter
    def lms_filter(self, x, d, mu, N):
        if N <= 0 or not isinstance(N, int):
            raise ValueError("N must be a positive integer.")
        n = len(x)
        w = np.zeros(N)
        y = np.zeros(n)

        for i in range(N, n):
            x_n = x[i-N:i][::-1]
            y[i] = np.dot(w, x_n)
            e = d[i] - y[i]
            w += 2 * mu * e * x_n

        return y
    
    def outlier_filter(self, data, window_size=10, threshold=3):
        # Ensure input data is a numpy array
        data = np.asarray(data)

        # Prepend the state (last few values from previous chunk) to the new data
        if self.outlier_filter_state is not None:
            data = np.concatenate((self.outlier_filter_state, data))

        # Create a rolling window for median and absolute deviation
        df = pd.DataFrame(data, columns=['voltage'])
        rolling_median = df['voltage'].rolling(window=window_size, min_periods=1).median()
        rolling_mad = df['voltage'].rolling(window=window_size, min_periods=1).apply(lambda x: np.median(np.abs(x - np.median(x))))
        
        # Identify outliers
        is_outlier = np.abs(df['voltage'] - rolling_median) / rolling_mad > threshold
        
        # Replace outliers with the rolling median
        df.loc[is_outlier, 'voltage'] = rolling_median[is_outlier]
        
        # Update the state with the last few data points of the current chunk
        self.outlier_filter_state = data[-window_size:]
        
        # Ensure the output length matches the input data length of the current chunk
        filtered_data = df['voltage'].values[-len(data):]

        return filtered_data
    
    # Validate parameters for filters
    def validate_parameters(self, cutoff, fs, order=None):
        if cutoff <= 0 or fs <= 0:
            raise ValueError("Cutoff frequency and sampling frequency must be positive.")
        if cutoff >= fs / 2:
            raise ValueError("Cutoff frequency must be less than half the sampling frequency (Nyquist frequency).")
        if order is not None and (order < 1 or not isinstance(order, int)):
            raise ValueError("Filter order must be a positive integer.")

    def add_filter(self, name, params):
        self.filter_dict[name] = params

    def clear_filters(self):
        self.filter_dict.clear()
        if hasattr(self, 'lowpass_state'):
            del self.lowpass_state
        if hasattr(self, 'highpass_state'):
            del self.highpass_state
        if hasattr(self, 'notch_state'):
            del self.notch_state

    def items(self):
        return self.filter_dict.items()