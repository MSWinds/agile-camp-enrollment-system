import unittest
from unittest.mock import patch
from main import main, ApplicationInputFrame, AssignerFrame, CheckinFrame


class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['Quit'])
    @patch.object(ApplicationInputFrame, 'run')
    @patch.object(AssignerFrame, 'run')
    @patch.object(CheckinFrame, 'run')
    def test_main(self, mock_checkin_frame_run, mock_assigner_frame_run, mock_application_input_frame_run, mock_input):
        main()
        mock_application_input_frame_run.assert_not_called()
        mock_assigner_frame_run.assert_not_called()
        mock_checkin_frame_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
