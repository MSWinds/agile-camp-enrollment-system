import unittest
from test_accpt_letter import TestAcceptanceLetter
from test_bh import TestAssigningBunkhouses
from test_rejct_letter import TestRejectionLetter
from test_tribe import TestAssigningTribes

if __name__ == "__main__":
    # Create a test suite object
    suite = unittest.TestSuite()

    # Add tests from the test modules to the test suite
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAcceptanceLetter))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAssigningBunkhouses))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRejectionLetter))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAssigningTribes))

    # Run the test suite using the TextTestRunner
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
