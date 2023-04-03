import unittest
import PySimpleGUI as sg
import pandas as pd

import os
import sys

try:
    sys.path.append(os.environ['IST303_PROJECT_SRC_DIR'])
except KeyError:
    print("Error: The environment variable IST303_PROJECT_SRC_DIR is not defined.")
    sys.exit(1)
from checkin import CheckinFrame


class TestCheckinFrame(unittest.TestCase):
    def setUp(self):
        self.test_window = sg.Window('Test Window', [[sg.Button('Exit')]])
        self.camper_info = pd.DataFrame({
            'Last Name': ['Doe', 'Smith'],
            'CamperID': [1, 2],
            'Gender': ['M', 'F'],
            'Check-in Status': [False, False],
            'Medical Condition': ['None', 'Asthma'],
            'Dietary Restriction': ['None', 'Vegetarian']
        })
        self.camper_info.to_csv('test_camper_info.csv', index=False)

    def tearDown(self):
        os.remove('test_camper_info.csv')

    def test_checkin_success(self):
        checkin_frame = CheckinFrame('test_camper_info.csv')
        checkin_frame.run()
        checkin_info = pd.read_csv('checkin_info.csv')
        self.assertEqual(len(checkin_info), 1)
        self.assertEqual(checkin_info['Last Name'][0], 'Doe')
        self.assertEqual(checkin_info['CamperID'][0], 1)
        self.assertEqual(checkin_info['Gender'][0], 'M')
        self.assertEqual(checkin_info['Check-in Status'][0], True)
        self.assertEqual(checkin_info['Medical Condition'][0], 'None')
        self.assertEqual(checkin_info['Dietary Restriction'][0], 'None')

    def test_checkin_error(self):
        checkin_frame = CheckinFrame('test_camper_info.csv')
        checkin_frame.run()
        checkin_info = pd.read_csv('checkin_info.csv')
        self.assertEqual(len(checkin_info), 0)
        self.assertEqual(checkin_frame.popup_message, 'Error: No matching record found. Please check your input.')


if __name__ == '__main__':
    unittest.main()
