import PySimpleGUI as sg

class CheckinFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Check In', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Last Name:'), sg.InputText(key='last_name')],
            [sg.Text('Camper ID:'), sg.InputText(key='camper_id')],
            [sg.Text('Gender:'), sg.Listbox(values=('M', 'F', 'Other'), key='gender')],
            [sg.Text('Medical Condition:'), sg.InputText(key='med_condition')],
            [sg.Text('Dietary Restriction:'), sg.InputText(key='dietary_restrict')],
            [sg.Button('Check In', font=('Helvetica', 14))]]

    def run(self):

                    sg.Popup('Error: No matching record found. Please check your input.')
        window.close()


if __name__ == '__main__':
    CheckinFrame().run()