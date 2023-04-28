import unittest
import pandas as pd
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from algorithm.assigner_algorithms import assign_bunkhouse


class TestAssigningBunkhouses(unittest.TestCase):

    def setUp(self):
        # Define a sample dataset
        self.data = pd.DataFrame({
            'CamperID': range(1, 217),
            'Last Name': ['Doe'] * 216,
            'Gender': ['M'] * 108 + ['F'] * 108,
            'Age': [10] * 216,
            'Session': ['June'] * 36 + ['July'] * 36 + ['August'] * 36 +
                       ['June'] * 36 + ['July'] * 36 + ['August'] * 36

        })

    def test_assigning_bunkhouse(self):
        # Test that the function returns a dataframe with the 'bunkhouse' column
        result = assign_bunkhouse(self.data)
        self.assertTrue('Bunkhouse' in result.columns)

        # Test that each camper is assigned to a bunkhouse
        self.assertTrue(result['Bunkhouse'].isna().sum() == 0)

        # Test that each bunkhouse has 12 campers or fewer
        for bunkhouse in result['Bunkhouse'].unique():
            num_campers = len(result[result['Bunkhouse'] == bunkhouse])
            self.assertTrue(num_campers <= 12)

        # Test that the means of each bunkhouse for each gender and session are within 0.5 range
        for session in ['June', 'July', 'August']:
            for gender in ['M', 'F']:
                subset = result[(result['Session'] == session) & (result['Gender'] == gender)]
                means = subset.groupby('Bunkhouse')['Age'].mean()
                self.assertTrue((means.max() - means.min()) <= 0.5)


if __name__ == '__main__':
    unittest.main()
