import unittest
import pandas as pd
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from algorithm.assigner_algorithms import assign_tribe


class TestAssigningTribes(unittest.TestCase):
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

    def test_assigning_tribes(self):
        # Call the assigning_tribes function on the sample dataset
        result = assign_tribe(self.data)

        # Check if the 'tribe' column has been added to the dataset
        self.assertIn('Tribe', result.columns)

        # Check if all campers have been assigned to a tribe
        self.assertTrue(result['Tribe'].notna().all())

        # Check if there are exactly 12 campers in each tribe for each session
        for session in ['June', 'July', 'August']:
            for i in range(1, 7):
                tribe_name = f'Tribe{i}_{session}'
                tribe_count = result[result['Tribe'] == tribe_name]['Tribe'].count()
                self.assertEqual(tribe_count, 12, f"Wrong number of campers in {tribe_name} for {session} session")

        # Check if the age and gender are balanced in each tribe for each session
        for session in ['June', 'July', 'August']:
            for i in range(1, 7):
                tribe_name = f'Tribe{i}_{session}'
                tribe_data = result[result['Tribe'] == tribe_name]
                tribe_age_mean = tribe_data['Age'].mean()
                tribe_gender_count = tribe_data['Gender'].value_counts()

                # Check if age is balanced
                self.assertAlmostEqual(tribe_age_mean, 10, delta=0.5,
                                       msg=f"Age is not balanced in {tribe_name} for {session} session")

                # Check if gender is balanced
                self.assertAlmostEqual(tribe_gender_count['M'], 6, delta=2,
                                       msg=f"Male gender is not balanced in {tribe_name} for {session} session")
                self.assertAlmostEqual(tribe_gender_count['F'], 6, delta=2,
                                       msg=f"Female gender is not balanced in {tribe_name} for {session} session")


if __name__ == '__main__':
    unittest.main()
