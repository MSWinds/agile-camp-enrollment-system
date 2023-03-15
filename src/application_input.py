
import PySimpleGUI as sg

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

                sg.Popup('Submit Successful!')
                break
        window.close()


if __name__ == '__main__':
    ApplicationInputFrame().run()
