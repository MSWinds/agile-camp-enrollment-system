import os
import unittest
from unittest.mock import MagicMock
from pandas import DataFrame
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from algorithm.accpt_letter import create_acceptance_letter

class TestAcceptanceLetter(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = {
            'CamperID': [123],
            'Date': ['2023-05-01'],
            'First Name': ['John'],
            'Last Name': ['Doe'],
            'Session': ['June']
        }
        self.row = DataFrame(self.sample_data)
        self.file_path = f"files/{self.row['CamperID'].values[0]}/{self.row['CamperID'].values[0]}_{self.row['Date'].values[0]}_Accpt.pdf"
    
    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_create_acceptance_letter(self):
        create_acceptance_letter(self.row)
        self.assertTrue(os.path.exists(self.file_path))

if __name__ == '__main__':
    unittest.main()
