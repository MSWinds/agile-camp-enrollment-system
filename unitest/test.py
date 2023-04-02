import unittest

# Import all the test files
import app_unit_test
import assigner_frame_unit_test
import assigning_bh_unit_test
import assigning_tribe_unit_test
import checkin_unit_test
import mainframe_unit_test
import payment_unit_test

# Create a test suite to run all the tests
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(app_unit_test.TestApplicationInputFrame))
suite.addTest(unittest.makeSuite(assigner_frame_unit_test.TestPlotGenderDistribution))
suite.addTest(unittest.makeSuite(assigning_bh_unit_test.TestAssigningBunkhouses))
suite.addTest(unittest.makeSuite(assigning_tribe_unit_test.TestAssigningTribes))
suite.addTest(unittest.makeSuite(checkin_unit_test.TestCheckinFrame))
suite.addTest(unittest.makeSuite(mainframe_unit_test.TestMain))
suite.addTest(unittest.makeSuite(payment_unit_test.TestPaymentInputFrame))

# Run the test suite
unittest.TextTestRunner().run(suite)
