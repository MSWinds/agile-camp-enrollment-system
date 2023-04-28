import unittest
import os
from unittest.mock import MagicMock
from pandas import DataFrame
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from algorithm.rejct_letter import create_rejection_letter

class TestRejectionLetter(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = {
            'First Name': ['Jane'],
            'Last Name': ['Doe'],
            'Session': ['July']
        }
        self.row = DataFrame(self.sample_data)
        self.rejection_result = "Incomplete application"
        self.file_path = f"files/rejection/{self.row['First Name'].values[0]}_{self.row['Last Name'].values[0]}_{self.row['Session'].values[0]}_Reject.pdf"

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_create_rejection_letter(self):
        create_rejection_letter(self.row, self.rejection_result)
        self.assertTrue(os.path.exists(self.file_path))

if __name__ == '__main__':
    unittest.main()
