import os
import sys
import unittest
from unittest.mock import MagicMock
import PySimpleGUI as sg

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath('../src'))
from main import main

class TestMain(unittest.TestCase):

    def test_main(self):
        # Mock the different frames
        with unittest.mock.patch('application.ApplicationInputFrame') as MockApplicationInputFrame,\
             unittest.mock.patch('assigner.AssignerFrame') as MockAssignerFrame,\
             unittest.mock.patch('checkin.CheckinFrame') as MockCheckinFrame,\
             unittest.mock.patch('refund.RefundFrame') as MockRefundFrame:
            
            # Create instances of the mock frames
            mock_application_input_frame = MagicMock()
            mock_assigner_frame = MagicMock()
            mock_checkin_frame = MagicMock()
            mock_refund_frame = MagicMock()

            # Assign the instances to the return values of the constructors
            MockApplicationInputFrame.return_value = mock_application_input_frame
            MockAssignerFrame.return_value = mock_assigner_frame
            MockCheckinFrame.return_value = mock_checkin_frame
            MockRefundFrame.return_value = mock_refund_frame

            # Define a function to simulate button clicks and close the window
            def fake_read():
                nonlocal fake_read
                fake_read.call_count += 1
                if fake_read.call_count == 1:
                    return 'Register', None
                elif fake_read.call_count == 2:
                    return 'Check-in', None
                elif fake_read.call_count == 3:
                    return 'Assign', None
                elif fake_read.call_count == 4:
                    return 'Refund', None
                else:
                    return 'Quit', None

            fake_read.call_count = 0

            # Replace the read method of the PySimpleGUI Window class with the fake_read function
            with unittest.mock.patch('PySimpleGUI.Window.read', new=fake_read):
                main()

            # Assert that the run method of the mock frames is called once
            mock_application_input_frame.run.assert_called_once()
            mock_assigner_frame.run.assert_called_once()
            mock_checkin_frame.run.assert_called_once()
            mock_refund_frame.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()

