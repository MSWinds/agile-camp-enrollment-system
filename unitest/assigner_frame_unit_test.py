import unittest
import pandas as pd
from matplotlib.figure import Figure
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from assigner import AssignerFrame


class TestAssignerFrame(unittest.TestCase):

    def test_assigner_frame(self):
        # initialize the AssignerFrame class
        assigner = AssignerFrame()

        # check that the window and layout are initialized correctly
        self.assertIsInstance(assigner.window, sg.Window)
        self.assertIsInstance(assigner.layout, list)

        # check that the gender distribution plot is created correctly
        checkin_data = pd.read_csv('checkin_info.csv')
        fig = assigner.create_gender_distribution_plot(checkin_data)
        self.assertIsInstance(fig, Figure)

        # check that the assigning functions work correctly
        camper_info = pd.read_csv('../camper_info.csv')
        merged_data = pd.merge(checkin_data, camper_info[['CamperID', 'Age', 'Session']], on='CamperID')
        merged_data['Bunkhouse'] = merged_data.apply(assigner.assigning_bunkhouse, axis=1)
        merged_data['Tribe'] = merged_data.apply(assigner.assigning_tribe, axis=1)
        self.assertIsNotNone(merged_data['Bunkhouse'])
        self.assertIsNotNone(merged_data['Tribe'])

        # check that the assignment data is saved correctly
        assigner.save_assignment_data(merged_data)
        assigned_data = pd.read_csv('assignment.csv')
        self.assertEqual(len(assigned_data), len(merged_data))