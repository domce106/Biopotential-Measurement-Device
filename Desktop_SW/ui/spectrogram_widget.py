from PyQt6.QtCore import pyqtSignal, pyqtSlot, QRectF
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton
import pyqtgraph as pg
import numpy as np
from collections import deque

class SpectrogramWidget(QWidget):
    data_received = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.num_freq_bins = 4097
        self.num_time_points = 100
        
        # Initialize a numpy array with a shape of (num_freq_bins, num_time_points)
        self.buffer = np.zeros((self.num_freq_bins, self.num_time_points))
        
        self.buffer[:self.num_freq_bins] = -100

        self.plotItem = pg.PlotItem()
        self.plotItem.getViewBox().setContentsMargins(0, 0, 0, 0)
        self.plotItem.setLabels(left='Frequency (Hz)', bottom='Time (s)')

        self.spectrogram = pg.ImageView(view=self.plotItem)
        self.layout.addWidget(self.spectrogram)

        self.data_received.connect(self.update_spectrogram)

        colors = [
            (0, 0, 128),  # Dark blue
            (0, 0, 255),  # Blue
            (255, 0, 0),  # Red
            (255, 255, 0) # Yellow
        ]
        pos = np.linspace(0.0, 1.0, len(colors))
        self.colormap = pg.ColorMap(pos, colors)
        
        self.spectrogram.setColorMap(self.colormap)
        
        # Add a reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_spectrogram)
        self.layout.addWidget(self.reset_button)


    @pyqtSlot(np.ndarray, np.ndarray)
    def update_spectrogram(self, data, freq_bins):
        # Check if this is the first update
        if not hasattr(self, 'updated'):
            self.updated = False
    
        self.freq_bins = freq_bins
    
        # Check the shape of the data
        if len(data.shape) == 1:
            # If data is one-dimensional, shift the buffer to the left and replace the last column with the new data
            self.buffer = np.roll(self.buffer, -1, axis=1)
            self.buffer[:, -1] = data
        elif len(data.shape) == 2:
            # If data is two-dimensional, shift the buffer to the left by the number of columns in data and replace the last columns with the new data
            num_new_columns = data.shape[1]
            self.buffer = np.roll(self.buffer, -num_new_columns, axis=1)
            self.buffer[:, -num_new_columns:] = data
        else:
            raise ValueError("Data must be a one or two dimensional array")
    
        # Convert the buffer to a numpy array and transpose it
        buffer_data = self.buffer.T
    
        # Save the current view range
        current_range = self.spectrogram.getView().viewRange()
    
        # Update the image with new data
        self.spectrogram.setImage(buffer_data)
    
        # Manually scale the image to fill the ImageView
        self.spectrogram.getView().setAspectLocked(False)
    
        self.spectrogram.getView().invertY(False)
    
        self.set_custom_y_axis_labels()
        self.set_custom_x_axis_labels()
    
        if not self.updated:
            # If this is the first update, use autoRange to fit the data
            self.spectrogram.getView().autoRange()
            self.updated = True
        else:
            # If this is not the first update, reapply the saved view range
            self.spectrogram.getView().setRange(xRange=current_range[0], yRange=current_range[1], padding=0)
    
        # If this is the first update, calculate the min and max from the data and set the levels
        min_val = np.min(buffer_data)
        max_val = np.max(buffer_data)
        self.spectrogram.getHistogramWidget().setLevels(min_val, max_val)
            
    def reset_spectrogram(self):
        self.buffer = np.zeros((self.num_freq_bins, self.num_time_points))
        self.spectrogram.setImage(self.buffer.T)
        # self.set_custom_y_axis_labels()  # Reset or adjust labels as needed

        
    def set_custom_y_axis_labels(self):
        if hasattr(self, 'freq_bins') and self.freq_bins is not None:
            # Define how many ticks you want across the axis
            num_ticks = 5  # Less ticks for better readability
            if num_ticks > len(self.freq_bins):
                num_ticks = len(self.freq_bins)
            tick_step = len(self.freq_bins) // num_ticks
            tick_indices = np.arange(0, len(self.freq_bins), tick_step)
            
            # Round labels to the nearest 5 or 10
            tick_labels = ["{:.0f}".format(round(self.freq_bins[idx], -1)) for idx in tick_indices]
            tick_labels = [str(int(label) // 10 * 10) if int(label) % 10 < 5 else str(int(label) // 10 * 10 + 10) + " Hz" for label in tick_labels]
    
            # Set ticks on the plot
            ticks = [(i, tick_labels[j]) for j, i in enumerate(tick_indices)]
            self.plotItem.getAxis('left').setTicks([ticks])
            
    def set_custom_x_axis_labels(self):
        # Check if freq_bins is defined
        if not hasattr(self, 'freq_bins'):
            return

        # Calculate the bitrate
        bitrate = np.max(self.freq_bins) * 2

        # Calculate the value of one bin
        bin_value = 200 / bitrate

        # Define how many ticks you want across the axis
        num_ticks = 10  # Set a reasonable number of ticks

        # Calculate the step size based on the total number of time points
        step_size = self.num_time_points // num_ticks

        # Calculate the x-values for the ticks based on the range of the x-axis
        x_values = np.arange(0, self.num_time_points, step_size)

        # Format the x-values as strings without adding the unit
        x_labels = [f'{x * bin_value:.1f}' for x in x_values]

        # Set ticks on the plot
        ticks = [(x_values[i], x_labels[i]) for i in range(num_ticks)]
        self.plotItem.getAxis('bottom').setTicks([ticks])

