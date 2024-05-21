from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLineEdit, QLabel, QHBoxLayout, QFormLayout, QListWidget
from PyQt6.QtCore import pyqtSignal
from interfaces.logger import global_logger

class FilterEditor(QWidget):
    filterDataChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.filterComboBox = QComboBox(self)
        self.filterComboBox.addItems(['butter_lowpass', 'butter_highpass', 'notch_filter', 'moving_average_filter', 'apply_median_filter', 'lms_filter', 'outlier_filter'])
        self.filterComboBox.currentTextChanged.connect(self.updateParameterInputs)
        self.layout.addWidget(QLabel("Select Filter"))
        self.layout.addWidget(self.filterComboBox)
        
        self.filtersList = [] 

        self.parametersLayout = QFormLayout()
        self.layout.addLayout(self.parametersLayout)
        
        # Add a QListWidget to the layout to show added filters
        self.filtersListWidget = QListWidget(self)
        self.layout.addWidget(self.filtersListWidget)

        self.addButton = QPushButton("Add Filter", self)
        self.addButton.clicked.connect(self.addFilter)
        self.layout.addWidget(self.addButton)

        self.removeButton = QPushButton("Remove Filter", self)
        self.removeButton.clicked.connect(self.removeFilter)
        self.layout.addWidget(self.removeButton)

        self.saveButton = QPushButton("Save Filters", self)
        self.saveButton.clicked.connect(self.saveFilters)
        self.layout.addWidget(self.saveButton)
        
        self.editButton = QPushButton("Update Filter", self)
        self.editButton.clicked.connect(self.editFilter)
        self.layout.addWidget(self.editButton)
        
        # Modify the list widget to enable item selection
        self.filtersListWidget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.filtersListWidget.itemSelectionChanged.connect(self.loadSelectedFilter)

        self.filters = {}
        self.parameterWidgets = {}
        self.filterParameters = {
            'butter_lowpass': [('cutoff', 'Hz'), ('order', 'int')],
            'butter_highpass': [('cutoff', 'Hz'), ('order', 'int')],
            'notch_filter': [('freq', 'Hz'), ('Q', 'float')],  # Assuming 'freq' is intended to be 'cutoff'
            'moving_average_filter': [('window_size', 'int')],
            'apply_median_filter': [('kernel_size', 'int')],
            'lms_filter': [('step_size', 'float'), ('filter_length', 'int')],
            'outlier_filter': [('threshold', 'float'), ('window_size', 'int')]
        }

        
        self.updateParameterInputs(self.filterComboBox.currentText())

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    # Recursively clear sublayouts
                    self.clearLayout(item.layout())

    def updateParameterInputs(self, filter_name):
        # Clear existing parameter widgets and their references
        self.clearLayout(self.parametersLayout)
        self.parameterWidgets.clear()  # Clear the references

        # Create new parameter widgets
        for param, units in self.filterParameters.get(filter_name, []):
            label = QLabel(f"{param} ({units})")
            line_edit = QLineEdit()
            self.parametersLayout.addRow(label, line_edit)
            self.parameterWidgets[param] = line_edit


    def addFilter(self):
        filter_name = self.filterComboBox.currentText()
        parameters = {}
        for param, edit in self.parameterWidgets.items():
            if param != 'fs':
                value = edit.text()
                if not value:  # Check if the field is empty
                    global_logger.log(f"Field {param} must not be empty.", 'ERROR')
                    return
                try:
                    # Try to convert the value to the correct type
                    parameters[param] = float(value) if param in ['cutoff', 'Q', 'step_size'] else int(value)
                except ValueError:
                    # Log an error message if the value cannot be converted to the correct type
                    global_logger.log(f"Invalid value for {param}: {value}.", 'ERROR')
                    return
    
        # Add filter as a tuple (or you could define a custom class) to the list
        filter_entry = (filter_name, parameters)
        self.filtersList.append(filter_entry)
    
        # Update QListWidget
        self.updateFiltersListWidget()

    def removeFilter(self):
        selected_item = self.filtersListWidget.currentRow()
        if selected_item >= 0:
            # Remove from list widget and filters list
            self.filtersListWidget.takeItem(selected_item)
            del self.filtersList[selected_item]

    def updateFiltersListWidget(self):
        # Clears the list and repopulates it, can be optimized
        self.filtersListWidget.clear()
        for filter_name, params in self.filtersList:
            filter_description = f"{filter_name}: " + ", ".join(f"{k}={v}" for k, v in params.items())
            self.filtersListWidget.addItem(filter_description)

    def saveFilters(self):
        # Emit the list of filters
        self.filterDataChanged.emit(self.filtersList)
    
        # Print the saved filters
        for filter_name, params in self.filtersList:
            filter_description = f"{filter_name}: " + ", ".join(f"{k}={v}" for k, v in params.items())
            global_logger.log(filter_description, 'INFO')
            
    def loadSelectedFilter(self):
        selected_items = self.filtersListWidget.selectedItems()
        if selected_items:
            selected_text = selected_items[0].text()
            filter_name, params_string = selected_text.split(': ', 1)
            params = dict(param.split('=') for param in params_string.split(', '))
            self.updateParameterInputs(filter_name)
            for param, value in params.items():
                if param in self.parameterWidgets:
                    self.parameterWidgets[param].setText(value)

    def editFilter(self):
        selected_row = self.filtersListWidget.currentRow()
        if selected_row >= 0:
            filter_name = self.filterComboBox.currentText()
            parameters = {param: edit.text() for param, edit in self.parameterWidgets.items()}
            filter_entry = (filter_name, parameters)
            self.filtersList[selected_row] = filter_entry  # Update the existing filter entry
            self.updateFiltersListWidget()  # Refresh the list

