import pandas as pd
import PySimpleGUI as sg
import os
import subprocess
import sys

from algorithm.assigner_algorithms import assign_bunkhouse, assign_tribe


class AssignerFrame:
    def __init__(self):
        self.layout = [
            [sg.Button('Assign'), sg.Button('Reset'), sg.Button('Edit')],
            [sg.Text('', size=(30, 2), key='success_msg')],
            [sg.Text('', size=(30, 2), key='reset_msg')]
        ]

    def run(self):
        # Create the GUI window
        window = sg.Window('Assigner', self.layout)

        # Define the function for assigning bunkhouses and tribes
        def assign_button():
            try:
                # Load the camper information data set
                camper_info = pd.read_csv('data/camper_info.csv')

                # data has only the CamperID, Last Name, Gender, Age, and Session columns from camper_info
                data_raw = camper_info[["CamperID","Last Name","Gender","Age","Session"]]

                # Assign bunkhouses and tribes
                data = pd.merge(assign_bunkhouse(data_raw), assign_tribe(data_raw), on=['CamperID', 'Last Name', 'Gender', 'Age', 'Session'])

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
        def reset_button():
            try:
                # Check if the assignment file exists
                if os.path.exists('data/assignment.csv'):
                    # Load the assignment data set
                    data = pd.read_csv('data/assignment.csv')

                    # Reset the bunkhouse and tribe columns
                    data['Bunkhouse'] = ''
                    data['Tribe'] = ''

                    # Save the reset data to the assignment file
                    data.to_csv('data/assignment.csv', index=False)

                    # Display a reset message
                    reset_msg = f'{len(data)} campers have been successfully reset.'
                    window['reset_msg'].update(reset_msg)
                    os.remove('data/assignment.csv')
                else:
                    # Display an error message if the assignment file doesn't exist
                    sg.popup_error('No assignments found to reset.')

            except Exception as e:
                # Display a generic error message for any other errors
                sg.popup_error(f'An error occurred: {str(e)}')

        # Define the function for modifying camper assignments
        def modify_button():
            assignment_file = 'data/assignment.csv'

            if not os.path.exists(assignment_file):
                sg.popup_error("No assignments found. Please assign campers first.")
                return

            data = pd.read_csv(assignment_file)

            while True:
                modify_layout = [
                    [sg.Text('Camper ID:'), sg.InputText('', key='camper_id')],
                    [sg.Text('Column to modify:'), sg.InputCombo(['Bunkhouse', 'Tribe'], key='column')],
                    [sg.Text('New value:'), sg.InputText('', key='new_value')],
                    [sg.Button('Modify')]
                ]

                modify_window = sg.Window('Modify Camper Assignments', modify_layout)

                event, values = modify_window.read()

                if event == 'Modify':
                    try:
                        camper_id = int(values['camper_id'])
                        column = values['column']
                        new_value = values['new_value']

                        if camper_id in data['CamperID'].values:
                            data.loc[data['CamperID'] == camper_id, column] = new_value
                            sg.popup(f"Successfully modified Camper ID {camper_id}'s {column} to {new_value}")
                        else:
                            sg.popup_error(f"Camper ID {camper_id} not found")
                    except ValueError:
                        sg.popup_error("Invalid input. Please enter a valid Camper ID.")
                    except Exception as e:
                        sg.popup_error(f"An error occurred: {str(e)}")
                elif event == sg.WIN_CLOSED:
                    modify_window.close()
                    break

            # Save the modified dataframe to the assignment.csv file
            data.to_csv(assignment_file, index=False)


        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Assign':
                assign_button()
            elif event == 'Reset':
                reset_button()
            elif event == 'Edit':
                modify_button()

        # Close the window when the loop ends
        window.close()


if __name__ == '__main__':
    AssignerFrame().run()
