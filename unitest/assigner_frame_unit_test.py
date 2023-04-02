import unittest
import pandas as pd
import os
import sys

try:
    sys.path.append(os.environ['IST303_PROJECT_SRC_DIR'])
except KeyError:
    print("Error: The environment variable IST303_PROJECT_SRC_DIR is not defined.")
    sys.exit(1)
from assigner import plot_gender_distribution


class TestPlotGenderDistribution(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'CamperID': range(1, 217),
            'Last Name': ['Doe'] * 216,
            'Gender': ['M'] * 108 + ['F'] * 108,
            'Age': [10] * 216,
            'Session': ['June'] * 36 + ['July'] * 36 + ['August'] * 36 +
                       ['June'] * 36 + ['July'] * 36 + ['August'] * 36
        })

    def test_plot_gender_distribution(self):
        fig = plot_gender_distribution(self.data)
        ax_list = fig.axes

        expected_distribution = {'June': (36, 36), 'July': (36, 36), 'August': (36, 36)}

        for ax, session in zip(ax_list, self.data['Session'].unique()):
            bars = ax.containers[0]
            bar_counts = [bar.get_height() for bar in bars]
            self.assertEqual(tuple(bar_counts), expected_distribution[session])


if __name__ == '__main__':
    unittest.main()
