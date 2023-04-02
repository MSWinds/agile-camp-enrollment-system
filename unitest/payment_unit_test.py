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
from application_input import PaymentInputFrame


class TestPaymentInputFrame(unittest.TestCase):
    def setUp(self):
        self.payment_input_frame = PaymentInputFrame()

    def test_run(self):
        camper_data = pd.DataFrame({
            'CamperID': [1],
            'First Name': ['John'],
            'Last Name': ['Doe'],
            'Birth Date': ['01/01/2000'],
            'Age': [22],
            'Gender': ['Male'],
            'Session': ['Session 1'],
            'Contact Information': ['john.doe@example.com'],
            'Special Requests': ['None']
        })
        with patch('builtins.input', side_effect=[123, 'John Doe', '100', True]):
            self.payment_input_frame.run(camper_data)
        payment_data = pd.read_csv('../camper_info.csv')
        self.assertEqual(payment_data['Check Number'][0], 123)
        self.assertEqual(payment_data['Payee Name'][0], 'John Doe')
        self.assertEqual(payment_data['Amount'][0], 100)
        self.assertEqual(payment_data['Valid'][0], 'Yes')


if __name__ == '__main__':
    unittest.main()
