import unittest
import pandas as pd
from unittest.mock import patch
import os
import sys

try:
    sys.path.append(os.environ['IST303_PROJECT_SRC_DIR'])
except KeyError:
    print("Error: The environment variable IST303_PROJECT_SRC_DIR is not defined.")
    sys.exit(1)


# pytest app_unit_test.py

class TestApplicationInputFrame(unittest.TestCase):
    def setUp(self):
        self.application_input_frame = ApplicationInputFrame()

    @patch('application_input.PaymentInputFrame.run')
    @patch('builtins.input',
           side_effect=['June', 'John', 'Doe', '22', 'M', '01/01/2000', 'john.doe@example.com', 'None'])
    def test_run(self, mock_input, mock_payment_input_frame_run):
        self.application_input_frame.run()
        # Check that the camper data is saved to a DataFrame
        camper_data = pd.DataFrame({
            'CamperID': [mock_payment_input_frame_run.call_args[0][0]['CamperID']],
            'First Name': [mock_payment_input_frame_run.call_args[0][0]['First Name']],
            'Last Name': [mock_payment_input_frame_run.call_args[0][0]['Last Name']],
            'Birth Date': [mock_payment_input_frame_run.call_args[0][0]['Birth Date']],
            'Age': [mock_payment_input_frame_run.call_args[0][0]['Age']],
            'Gender': [mock_payment_input_frame_run.call_args[0][0]['Gender']],
            'Session': [mock_payment_input_frame_run.call_args[0][0]['Session']],
            'Contact Information': [mock_payment_input_frame_run.call_args[0][0]['Contact Information']],
            'Special Requests': [mock_payment_input_frame_run.call_args[0][0]['Special Requests']]
        })
        self.assertEqual(camper_data['First Name'][0], 'John')
        self.assertEqual(camper_data['Last Name'][0], 'Doe')
        self.assertEqual(camper_data['Age'][0], '22')
        self.assertEqual(camper_data['Gender'][0], 'M')
        self.assertEqual(camper_data['Birth Date'][0], '01/01/2000')
        self.assertEqual(camper_data['Contact Information'][0], 'john.doe@example.com')
        self.assertEqual(camper_data['Special Requests'][0], 'None')


if __name__ == '__main__':
    unittest.main()
