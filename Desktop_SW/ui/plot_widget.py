from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSlot
import pyqtgraph as pg
import numpy as np
class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        
        self.plot_widget.showGrid(x=True, y=True)

        self.y_data = np.array([])
        self.data_limit = 1000  # Set the data limit

        # Generate the x_data as a constant range
        self.x_data = np.arange(self.data_limit)
        
        self.plot_widget.getAxis('left').setLabel('Voltage', units='V')
        self.plot_widget.getAxis('bottom').setLabel('Time', units='s')

        # Create the reset button
        self.reset_button = QPushButton("Reset")
        self.layout.addWidget(self.reset_button)

        # Connect the reset button's clicked signal to the reset slot
        self.reset_button.clicked.connect(self.reset)
        
        # Create QLabel instances for the min and max amplitude values
        self.min_label = QLabel()
        self.max_label = QLabel()
        self.layout.addWidget(self.min_label)
        self.layout.addWidget(self.max_label)

        # Create the checkbox for toggling the min and max amplitude values
        self.toggle_checkbox = QCheckBox("Show Min/Max Amplitude")
        self.layout.addWidget(self.toggle_checkbox)

    @pyqtSlot(np.ndarray, int)
    def add_data(self, y, bitrate):
        self.y_data = np.append(self.y_data, y)
    
        # If the data limit is exceeded, remove old data
        if len(self.y_data) > self.data_limit:
            self.y_data = self.y_data[-self.data_limit:]
    
        # Generate the x_data based on the bitrate
        self.x_data = np.linspace(0, self.data_limit/bitrate, num=len(self.y_data))
    
        self.update_plot()
    
    def update_amplitude_labels(self):
        # Update the min and max amplitude values
        if len(self.y_data) > 0 and self.toggle_checkbox.isChecked():
            min_val = np.min(self.y_data)
            max_val = np.max(self.y_data)
            self.min_label.setText(f'Min amplitude: {self.format_amplitude(min_val)}')
            self.max_label.setText(f'Max amplitude: {self.format_amplitude(max_val)}')
            self.min_label.setVisible(True)
            self.max_label.setVisible(True)
        else:
            self.min_label.setVisible(False)
            self.max_label.setVisible(False)
            
    def format_amplitude(self, amplitude):
        # Convert the amplitude to millivolts and microvolts
        amplitude_mv = amplitude * 1e3
        amplitude_uv = amplitude * 1e6
    
        # Choose the most convenient unit based on the amplitude value
        if abs(amplitude) < 1e-3:
            return f'{round(amplitude_uv, 3)} uV'
        elif abs(amplitude) < 1:
            return f'{round(amplitude_mv, 3)} mV'
        else:
            return f'{round(amplitude, 3)} V'
    
    def update_plot(self):
        self.plot_widget.clear()
        self.plot_widget.plot(self.x_data, self.y_data)

        self.update_amplitude_labels()

    def plot(self, y):
        self.plot_widget.plot(self.x_data[:len(self.y_data)], y)
        
    @pyqtSlot()
    def clear_plot(self):
        self.y_data = np.array([])
        self.update_plot()
        
    @pyqtSlot()
    def reset(self):
        self.clear_plot()
        self.y_data = np.array([])
        self.x_data = np.arange(self.data_limit)
        
    def print_average(self):
        if len(self.y_data) > 0:
            average = np.mean(self.y_data)
            print(f'Average value of the data: {average}')
        else:
            print('No data to calculate the average.')