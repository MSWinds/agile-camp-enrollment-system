import PySimpleGUI as sg
import pandas as pd
import os

from algorithm.accpt_letter import create_acceptance_letters

class MailingFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Mailing Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Column([[sg.Button('Acceptance Letter', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Rejection Letter', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Cancelation Letter', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Quit', size=(30, 2), font=('Helvetica', 14))]])]]

    def run(self):  
        window = sg.Window('Mailing Information', self.layout, element_justification='c').Finalize()

        while True:
            event, values = window.read()
            print(event, values)  # debug
            if event == sg.WIN_CLOSED or event == 'Quit':
                break
            if event == 'Acceptance Letter':
                if not os.path.isfile('files/mailing_accpt.csv'):
                    camper_data = pd.read_csv('data/camper_info.csv')
                    mailing_accpt = camper_data[['CamperID', 'First Name', 'Last Name', 'Session', 'Date']]
                    mailing_accpt['Mailing Status'] = 'neg'
             
                session_popup = sg.PopupGetText('Enter session (June, July, August):', title='Session Selection')
                if session_popup:
                    pending_count = mailing_accpt[(mailing_accpt['Mailing Status'] == 'neg') & (mailing_accpt['Session'] == session_popup)].shape[0]
                    sg.Popup(f'There are {pending_count} acceptance letters needed to be sent')

                    if sg.PopupYesNo('Do you want to create letters?') == 'Yes':
                        create_acceptance_letters(mailing_accpt)
                        mailing_accpt.to_csv('mailing_accpt.csv', index=False)

            if event == 'Rejection Letter':
                self.rejection_letter()
            if event == 'Cancelation Letter':
                self.cancelation_letter()

        window.close()
       

