import pandas as pd
import PySimpleGUI as sg
import os
import uuid
import hashlib


class ApplicationInputFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Camper Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Session:'), sg.Combo(["June", "July", "August"], key="session_choice")],
            [sg.Text('First Name:'), sg.InputText(key='f_name')],
            [sg.Text('Last Name:'), sg.InputText(key='l_name')],
            [sg.Text('Age:'), sg.InputText(key='age')],
            [sg.Text('Gender:'), sg.Listbox(values=('M', 'F', 'Other'), key='gender')],
            [sg.Text('Birth Date:'),
             sg.CalendarButton('Select Date', target='birth_date', format='%m/%d/%Y'),
             sg.Input('', size=(10, 1), key='birth_date')],
            [sg.Text('Contact Information:'), sg.InputText(key='contact_info')],
            [sg.Text('Special Requests:'), sg.InputText(key='special_requests')],
            [sg.Button('Save and Go Payment Tab', font=('Helvetica', 14))]]

    def run(self):
        window = sg.Window('Application Input', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED:
                break
            if event == 'Save and Go Payment Tab':
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
                    'Age': [values['age']],
                    'Gender': [values['gender']],
                    'Session': [values['session_choice']],
                    'Contact Information': [values['contact_info']],
                    'Special Requests': [values['special_requests']]
                })
                PaymentInputFrame().run(camper_data)
                break
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
            [sg.Button('Submit', font=('Helvetica', 14))]]

    def run(self, camper_data):
        window = sg.Window('Payment Input', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
                check_valid = 'Yes' if values['check_valid'] else 'No'
                # save input into the data frame
                payment_data = pd.DataFrame({
                    'Check Number': [values['check_num']],
                    'Payee Name': [values['check_name']],
                    'Amount': [values['check_amount']],
                    'Valid': [check_valid],
                    'Date': [current_date]
                })
                camper_info = pd.concat([camper_data, payment_data], axis=1)
                # save the dataframe into a csv file
                if not os.path.isfile('data/camper_info.csv'):
                    camper_info.to_csv('data/camper_info.csv', index=False)
                else:
                    camper_info.to_csv('data/camper_info.csv', mode='a', header=False, index=False)

                # We can call a notification system here to print out the paper.
                sg.Popup('Submit Successful!')
                break
        window.close()


if __name__ == '__main__':
    ApplicationInputFrame().run()
