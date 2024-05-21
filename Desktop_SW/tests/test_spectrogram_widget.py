import numpy as np
import time
import unittest
from PyQt6.QtWidgets import QApplication
from ui.spectrogram_widget import SpectrogramWidget

class TestSpectrogramWidget(unittest.TestCase):
    def test_spectrogram_widget(self):
        # Create a QApplication (this is necessary for any tests involving Qt)
        app = QApplication([])

        # Create a SpectrogramWidget
        spectrogram = SpectrogramWidget()

        # Show the SpectrogramWidget
        spectrogram.show()

        # Frequency of the sine wave
        frequency = 5  # Hz

        # Time array
        t = np.linspace(0, 1, 8192, False)  # 1 second

        # Generate the sine wave
        sine_wave = np.sin(2 * np.pi * frequency * t)

        # Compute the FFT of the sine wave
        fft_data = np.fft.rfft(sine_wave)

        # Compute the frequencies corresponding to the FFT values
        fft_freq = np.fft.rfftfreq(len(sine_wave), d=t[1]-t[0])

        # Find the index of the frequency with the largest magnitude
        max_index = np.argmax(np.abs(fft_data))

        # Print the frequency with the largest magnitude
        print('Frequency with largest magnitude:', fft_freq[max_index], 'Hz')

        # Update the spectrogram 100 times
        for _ in range(100):
            spectrogram.update_spectrogram(np.abs(fft_data), fft_freq)
        
        # Run the QApplication for a while to allow the spectrogram to update
        end_time = time.time() + 10  # 10 seconds from now
        while time.time() < end_time:
            app.processEvents()
            time.sleep(0.01)  # Sleep a little to reduce CPU usage

        # Close the QApplication
        app.quit()

if __name__ == '__main__':
    unittest.main()