import pandas as pd
import PySimpleGUI as sg
import os

from algorithm.assigner_algorithms import assign_bunkhouse, assign_tribe


class AssignerFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Session:'), sg.Combo(["June", "July", "August"], key="session_choice", default_value="June")],
            [sg.Button('Assign'), sg.Button('Reset')],
            [sg.Text('', size=(30, 2), key='success_msg')],
            [sg.Text('', size=(30, 2), key='reset_msg')]
        ]

    def run(self):
        # Create the GUI window
        window = sg.Window('Assigner', self.layout)

        # Define the function for assigning bunkhouses and tribes
        def assign_button(s):
            try:
                # Load the camper information data set
                camper_info = pd.read_csv('data/camper_info.csv')

                # Filter the data set to include only the specified session
                camper_info = camper_info[camper_info['Session'] == s]

                # data has only the CamperID, Last Name, Gender, Age, and Session columns from camper_info
                data = camper_info[["CamperID","Last Name","Gender","Age","Session"]]

                # Assign bunkhouses and tribes
                data['Bunkhouse'] = assign_bunkhouse(data)
                data['Tribe'] = assign_tribe(data)

                # Save the assigned data to a csv file if exists, otherwise create a new file
                if os.path.exists('data/assignment.csv'):
                    data.to_csv('data/assignment.csv', mode='a', header=False, index=False)
                else:
                    data.to_csv('data/assignment.csv', index=False)

                # Display a success message
                success_msg = f'{len(data)} campers have been successfully assigned.'
                window['success_msg'].update(success_msg)

            except FileNotFoundError:
                # Display an error message if the input file doesn't exist
                sg.popup_error('The input file does not exist.')

            except Exception as e:
                # Display a generic error message for any other errors
                sg.popup_error(f'An error occurred: {str(e)}')

        # Define the function for resetting the assignments
        def reset_button(s):
            try:
                # Check if the assignment file exists
                if os.path.exists('data/assignment.csv'):
                    # Load the assignment data set
                    data = pd.read_csv('data/assignment.csv')

                    # Filter the data set to include only the specified session
                    data = data[data['Session'] == s]

                    # Reset the bunkhouse and tribe columns
                    data['Bunkhouse'] = ''
                    data['Tribe'] = ''

                    # Save the reset data to the assignment file
                    data.to_csv('data/assignment.csv', index=False)

                    # Display a reset message
                    reset_msg = f'{len(data)} campers have been successfully reset.'
                    window['reset_msg'].update(reset_msg)
                else:
                    # Display an error message if the assignment file doesn't exist
                    sg.popup_error('No assignments found to reset.')

            except Exception as e:
                # Display a generic error message for any other errors
                sg.popup_error(f'An error occurred: {str(e)}')

        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Assign':
                session = values['session_choice']
                assign_button(session)
            elif event == 'Reset':
                session = values['session_choice']
                reset_button(session)

        # Close the window when the loop ends
        window.close()
        return None


if __name__ == '__main__':
    AssignerFrame().run()
