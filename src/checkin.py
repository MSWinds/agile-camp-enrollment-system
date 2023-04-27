import PySimpleGUI as sg
import pandas as pd
import os
import datetime

class CheckinFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Check In', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Last Name:'), sg.InputText(key='last_name')],
            [sg.Text('Camper ID:'), sg.InputText(key='camper_id')],
            [sg.Text('Gender:'), sg.Combo(['M', 'F'], key='gender')],
            [sg.Text('Medical Condition:'), sg.InputText(key='med_condition')],
            [sg.Text('Dietary Restriction:'), sg.InputText(key='dietary_restrict')],
            [sg.Text('Emergency Contact Information:'), sg.InputText(key='emergency_contact')],
            [sg.Checkbox('Equipment', key='eq_valid')],
            [sg.Button('Check In', font=('Helvetica', 14))]]
        

    def run(self):
        window = sg.Window('Check In', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED:
                break
            if event == 'Check In':
                # check if Last Name is not numeric
                if values['last_name'].isnumeric():
                    sg.Popup('Error: Last Name cannot be numeric.')
                    continue

                # check if Camper ID is not numeric
                if not values['camper_id'].isnumeric():
                    sg.Popup('Error: Camper ID must be numeric.')
                    continue

                camper_info = pd.read_csv('data/camper_info.csv')
                if str(values['last_name']) in camper_info['Last Name'].values \
                        or int(values['camper_id']) in camper_info['CamperID'].values:
                    # set the check-in status to True
                    values['Check-in Status'] = True
                    # add the medical condition and dietary restriction to the record
                    checkin_data = pd.DataFrame({
                        'Last Name': [values['Last Name']],
                        'CamperID': [values['CamperId']],
                        'Gender': [values['Gender']],
                        'Check-in Status': [values['Check-in Status']],
                        'Check-in Time': [datetime.datetime.now().strftime('%Y-%m-%d')],  # current date and time
                        'Equipment Valid': [values['Eq_Valid']],
                        'Medical Condition': [values['Med_Condition']], # arrivial form
                        'Dietary Restriction': [values['Dietary_Restrict']],
                        'Emergency Contact Information:': [values['Emergency_Contact']]
                    })
                    # save the dataframe into a csv file
                    if not os.path.isfile('data/checkin_info.csv'):
                        checkin_data.to_csv('data/checkin_info.csv', index=False)
                    else:
                        checkin_data.to_csv('data/checkin_info.csv', mode='a', header=False, index=False)
                    sg.Popup('Check-in Successful!')
                    break
                else:
                    sg.Popup('Error: No matching record found. Please check your input.')
        window.close()


if __name__ == '__main__':
    CheckinFrame().run()


