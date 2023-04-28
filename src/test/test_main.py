import unittest
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath('../src'))
from main import main


# unit test for main function without pop-up windows
class TestMain(unittest.TestCase):
    def test_main(self):
        main()


if __name__ == '__main__':
    unittest.main()
