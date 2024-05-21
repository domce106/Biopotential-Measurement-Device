import unittest
import numpy as np
from scipy.signal import butter, lfilter
from interfaces.calculator.filters.filters import Filters
from interfaces.calculator.filter_handler import FilterHandler

class TestFilters(unittest.TestCase):
    def setUp(self):
        self.filter_handler = FilterHandler()

    def test_apply_filters(self):
        fs = 500.0  # Sample frequency (Hz)
        cutoff = 50.0  # cutoff frequency (Hz)
        order = 5  # Filter order
        t = np.linspace(0, 1, int(fs), False)  # Time array for one second
        x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)  # Signal with two frequency components

        self.filter_handler.change_filters([('butter_lowpass', {'cutoff': cutoff, 'fs': fs, 'order': order})])
        filtered_data = self.filter_handler.apply_filters(x.copy())

        # Perform the FFT and check the result
        fft_result = np.abs(np.fft.rfft(filtered_data))
        freqs = np.fft.rfftfreq(len(filtered_data), d=1/fs)

        # Debug: Print or plot the FFT result
        # For example:
        print("FFT Magnitude at frequencies above cutoff:")
        for freq, mag in zip(freqs, fft_result):
            if freq > cutoff:
                print(f"Frequency {freq} Hz: {mag}")

        # Check if the high frequency component is attenuated
        attenuation = np.all(fft_result[freqs > cutoff] < 1)  # Adjust threshold if necessary
        self.assertTrue(attenuation, "High frequencies not sufficiently attenuated")



    def test_apply_filters_with_different_signal(self):
        # Generate a sample signal
        t = np.linspace(0, 1, 500, endpoint=False)  # 1 second
        x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)  # 5 Hz and 120 Hz components

        # Define filter parameters
        fs = 500  # Sample frequency
        cutoff = 50  # cutoff frequency
        b, a = butter(5, cutoff / (0.5 * fs), btype='low')
        self.filter_handler.change_filters([('butter_lowpass', {'b': b, 'a': a})])
        # Add assertions here to check the result