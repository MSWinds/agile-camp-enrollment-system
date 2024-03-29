import pandas as pd
import PySimpleGUI as sg
import os
import uuid
import hashlib
import datetime
from algorithm.accpt_letter import create_acceptance_letter
from algorithm.rejct_letter import create_rejection_letter
from algorithm.arrival_form import create_arrival_form
from algorithm.equipment_checklist import create_equipment_checklist

class ApplicationInputFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Camper Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Session:'), sg.Combo(["June", "July", "August"], key="session_choice")],
            [sg.Text('First Name:'), sg.InputText(key='f_name')],
            [sg.Text('Last Name:'), sg.InputText(key='l_name')],
            [sg.Text('Gender:'), sg.Combo(['M', 'F'], key='gender')],
            [sg.Text('Birth Date:'),
             sg.CalendarButton('Select Date', target='birth_date', format='%m/%d/%Y'),
             sg.Input('', size=(10, 1), key='birth_date')],
            [sg.Text('Contact Information:'), sg.InputText(key='contact_info')],
            [sg.Text('Special Requests:'), sg.InputText(key='special_requests')],
            [sg.Button('Save and Go Payment Tab', font=('Helvetica', 14))],
            [sg.Button('Reject', font=('Helvetica', 14))]
            ]

    def calculate_age(self, birth_date):
        today = datetime.date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def run(self):
        window = sg.Window('Application Input', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED:
                break
            if event == 'Save and Go Payment Tab':
                # Check if names are not numeric
                if values['f_name'].isnumeric() or values['l_name'].isnumeric():
                    sg.Popup("Error: Names should not be numeric.")
                    continue

                # Calculate age based on the selected birth date
                birth_date = datetime.datetime.strptime(values['birth_date'], '%m/%d/%Y').date()
                age = self.calculate_age(birth_date)
                
                # Check if age is between 8 and 19 (inclusive)
                if age < 8 or age > 19:
                    sg.Popup("Error: Age must be between 8 and 19 years old.")
                    continue

                # Generate a unique id and convert it to a string and remove the hyphens
                str_uid = str(uuid.uuid4()).replace("-", "")
                # Use SHA-256 hashing and get the first 9 digits of the hexadecimal digest
                hash_uid = hashlib.sha256(str_uid.encode()).hexdigest()[:9]
                # Convert it to an integer base 16
                uid = int(hash_uid, 16)
                camper_data = pd.DataFrame({
                    'CamperID': [uid],
                    'First Name': [values['f_name']],
                    'Last Name': [values['l_name']],
                    'Birth Date': [values['birth_date']],
                    'Age': [age],
                    'Gender': [values['gender']],
                    'Session': [values['session_choice']],
                    'Contact Information': [values['contact_info']],
                    'Special Requests': [values['special_requests']]
                })
                
                # Load the existing camper information and count campers by gender and session
                if os.path.isfile('data/camper_info.csv'):
                    camper_info_raw = pd.read_csv('data/camper_info.csv')
                    campers_by_gender_and_session = camper_info_raw.groupby(['Session', 'Gender']).size().reset_index(name='Count')
                    # Check if the limit is reached for the camper's gender and session
                    campers_count = campers_by_gender_and_session.loc[
                                                                        (campers_by_gender_and_session['Session'] == values['session_choice']) &
                                                                        (campers_by_gender_and_session['Gender'] == values['gender']),
                                                                        'Count'].values

                    if campers_count.size > 0 and campers_count[0] >= 36:
                        sg.Popup("Error: The camp has reached the capacity limit for this session and gender.")
                        rejection_result = "Reach the Capacity Limit"
                        camper_data = pd.DataFrame({
                                                    'First Name': [values['f_name']],
                                                    'Last Name': [values['l_name']],
                                                    'Session': [values['session_choice']]
                                                    })
                        create_rejection_letter(camper_data, rejection_result)
                        continue


                PaymentInputFrame().run(camper_data)
                break
            
            if event == 'Reject':
                # check if the names and session are not empty
                if values['f_name'] == '' or values['l_name'] == '' or values['session_choice'] == '':
                    sg.Popup("Error: Please fill the name and session choice.")
                    continue

                rejection_result = sg.PopupGetText('Enter Rejection Result:', title='Rejection Result Input')
                if sg.PopupYesNo('Do you want to create letters?') == 'Yes':
                        camper_data = pd.DataFrame({
                                        'First Name': [values['f_name']],
                                        'Last Name': [values['l_name']],
                                        'Session': [values['session_choice']]                        
                                    })
                        create_rejection_letter(camper_data, rejection_result)
                        break
                else:
                    continue
        window.close()


class PaymentInputFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Payment Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Check Number:'), sg.InputText(key='check_num')],
            [sg.Text('Payee Name:'), sg.InputText(key='check_name')],
            [sg.Text('Amount:'), sg.InputText(key='check_amount')],
            [sg.Checkbox('Check is Valid', key='check_valid')],
            [sg.Button('Submit and Print', font=('Helvetica', 14))],
            [sg.Button('Reject', font=('Helvetica', 14))]
            ]

    def run(self, camper_data):
        window = sg.Window('Payment Input', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED:
                break

            if event == 'Reject':
                # check if the names and session from ApplicationInputFrame are not empty
                if camper_data['First Name'].values[0] == '' or camper_data['Last Name'].values[0] == '' or camper_data['Session'].values[0] == '':
                    sg.Popup("Error: Please fill the name and session choice.")
                    continue

                rejection_result = sg.PopupGetText('Enter Rejection Result:', title='Rejection Result Input')
                if sg.PopupYesNo('Do you want to create letters?') == 'Yes':
                        create_rejection_letter(camper_data, rejection_result)
                        break
                else:
                    continue

            if event == 'Submit and Print':
                # Check if the check number is not numeric and also not 4 digits
                if not values['check_num'].isnumeric() or len(values['check_num']) != 4:
                    sg.Popup("Error: Check number is invalid.")
                    continue

                # Check if the payee name is not numeric
                if values['check_name'].isnumeric():
                    sg.Popup("Error: Payee name is invalid.")
                    continue

                # check if the amount is not 1000
                if values['check_amount'] != '1000':
                    sg.Popup("Error: Check amount is invalid.")
                    continue

                check_valid = 'Yes' if values['check_valid'] else 'No'
                # save input into the data frame
                payment_data = pd.DataFrame({
                    'Check Number': [values['check_num']],
                    'Payee Name': [values['check_name']],
                    'Amount': [values['check_amount']],
                    'Valid': [check_valid],
                    'Date': [datetime.datetime.now().strftime('%Y-%m-%d')]
                })
                camper_info = pd.concat([camper_data, payment_data], axis=1)

                create_acceptance_letter(camper_info)
                create_arrival_form(camper_info)
                create_equipment_checklist(camper_info)

                # save the dataframe into a csv file
                if not os.path.isfile('data/camper_info.csv'):
                    camper_info.to_csv('data/camper_info.csv', index=False)
                else:
                    camper_info.to_csv('data/camper_info.csv', mode='a', header=False, index=False)

                # We can call a notification system here to print out the paper.
                sg.Popup('Successful!')
                break
        window.close()


if __name__ == '__main__':
    ApplicationInputFrame().run()
