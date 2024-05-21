import unittest
import numpy as np
from interfaces.calculator.measurement_data_handler import MeasurementData

class TestMeasurementData(unittest.TestCase):
    def setUp(self):
        self.data = MeasurementData()

    def test_convert_to_voltage(self):
        # Define test input and expected output for multiple gain values
        test_input = [0x7FFFFF, 0x800000, 0x0, 0x000001, 0xFFFFFF]
        gains = [1, 2, 4, 8]
        expected_outputs = [
            [2.42, -2.42, 0.0, 0.00001, -0.00001],
            [1.21, -1.21, 0.0, 0.000005, -0.000005],
            [0.605, -0.605, 0.0, 0.0000025, -0.0000025],
            [0.3025, -0.3025, 0.0, 0.00000125, -0.00000125]
        ]

        for gain, expected_output in zip(gains, expected_outputs):
            # Call the function with the test input and current gain
            actual_output = self.data.convert_to_voltage(test_input, gain)

            # Print the actual and expected outputs
            print(f"For gain {gain}, actual output is {actual_output} and expected output is {expected_output}")

            # Check that the actual output matches the expected output
            np.testing.assert_almost_equal(actual_output, expected_output, decimal=5)

if __name__ == '__main__':
    unittest.main()