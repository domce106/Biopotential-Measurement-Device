from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
import numpy as np
from interfaces.calculator.filters.filters import Filters
from interfaces.logger import global_logger

class FilterHandler(QObject):
    data_filtered = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.filters = Filters()
        self.sampling_frequency = None
        self.last_received_data = None  # to store the last data received

    @pyqtSlot(list)
    def change_filters(self, filters_list):
        # Clear existing filters before adding new ones
        self.filters.clear_filters()
        for filter_name, params in filters_list:
            self.filters.add_filter(filter_name, params)
            global_logger.log(f"Filter {filter_name} with parameters {params} added")

    @pyqtSlot(np.ndarray, int)
    def apply_filters(self, data, sampling_frequency):
        self.last_received_data = data  # Store the latest data
        if data is None:
            global_logger.log("No data to apply filters to.", 'ERROR')
            return

        # Check if the received sampling frequency is different from the previous one
        if self.sampling_frequency != sampling_frequency:
            self.sampling_frequency = sampling_frequency
            global_logger.log(f"Updated sampling frequency to {sampling_frequency}")
            self.reinitialize_filters()

        # Apply outlier filter first if it exists
        if 'outlier_filter' in self.filters:
            try:
                filter_func = getattr(self.filters, 'outlier_filter')
                if callable(filter_func):
                    params = self.filters['outlier_filter']
                    if 'fs' in filter_func.__code__.co_varnames:
                        params['fs'] = self.sampling_frequency  # Ensure 'fs' is always updated

                    data = filter_func(data, **params)  # Passing parameters unpacked
                    if data is None:
                        global_logger.log(f"Filter outlier_filter returned None.", 'ERROR')
                        return
            except AttributeError:
                global_logger.log(f"Filter function for outlier_filter is not defined.", 'ERROR')
            except TypeError as e:
                global_logger.log(f"Error applying filter outlier_filter: {e}", 'ERROR')

        # Apply the rest of the filters
        for filter_name, params in self.filters.items():
            if filter_name == 'outlier_filter':
                continue  # Skip outlier filter as it has already been applied

            try:
                filter_func = getattr(self.filters, filter_name)
                if callable(filter_func):
                    # Ensure all required parameters are included
                    if 'fs' in filter_func.__code__.co_varnames:
                        params['fs'] = self.sampling_frequency  # Ensure 'fs' is always updated

                    data = filter_func(data, **params)  # Passing parameters unpacked
                    if data is None:
                        global_logger.log(f"Filter {filter_name} returned None.", 'ERROR')
                        return
                else:
                    global_logger.log(f"No callable filter function found for {filter_name}", 'ERROR')
            except AttributeError:
                global_logger.log(f"Filter function for {filter_name} is not defined.", 'ERROR')
            except TypeError as e:
                global_logger.log(f"Error applying filter {filter_name}: {e}", 'ERROR')

        self.data_filtered.emit(data)  # Emit the filtered data
        return data

    def reinitialize_filters(self):
        # Fetch existing filters, clear them, and re-add with new frequency
        existing_filters = list(self.filters.items())
        self.filters.clear_filters()
        for filter_name, params in existing_filters:
            params['fs'] = self.sampling_frequency  # Update sampling frequency
            self.filters.add_filter(filter_name, params)

        if self.last_received_data is not None:
            self.apply_filters(self.last_received_data, self.sampling_frequency)
