import PySimpleGUI as sg
import pandas as pd
import os
import datetime
from algorithm.refund_letter import create_refund_letter

class RefundFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Refund Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Camper ID:'), sg.InputText(key='camper_id')],
            [sg.Button('Submit', font=('Helvetica', 14))]]

    # Calculate the refund amount based on the original payment date and the date of request
    def calculate_refund(self, original_payment_date, request_date):
        date_difference = (request_date - original_payment_date).days
        if date_difference <= 21:
            return 1000 * 0.9
        elif date_difference <= 42:
            return 1000 * 0.45
        else:
            return 0

    def run(self):
        window = sg.Window('Refund Input', self.layout, element_justification='c').Finalize()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                camper_id = values['camper_id']
                camper_data = pd.read_csv('data/camper_data.csv')

                # check if Camper ID is not in the camper data
                if int(camper_id) not in camper_data['CamperID'].values:
                    sg.Popup('Error: Camper ID does not exist.')
                    continue

                # Find the original payment date for the camper
                original_payment_date = camper_data.loc[camper_data['CamperID'] == camper_id, 'Date']
                original_payment_date = datetime.datetime.strptime(original_payment_date.values[0], '%Y-%m-%d').date()

                # Calculate the refund amount
                request_date = datetime.date.today()
                refund_amount = self.calculate_refund(original_payment_date, request_date)

                # Show refund amount and original payment date in a new window
                refund_layout = [
                    [sg.Text(f"Refund Amount: ${refund_amount:.2f}")],
                    [sg.Text(f"Date of Original Payment: {original_payment_date}")],
                    [sg.Button("OK")]]
                refund_window = sg.Window("Refund Details", refund_layout)
                refund_window.read(close=True)

                # Save input into a data frame
                refund_data = pd.DataFrame({
                    'CamperID': [camper_id],
                    'Refund Amount': [refund_amount],
                    'Date of Original Payment': [original_payment_date.strftime('%Y-%m-%d')],
                    'Date of Request': [request_date.strftime('%Y-%m-%d')]
                })

                create_refund_letter(refund_data) # Create a refund letter for the camper

                # Save the data frame into a CSV file
                if not os.path.isfile('data/refund_info.csv'):
                    refund_data.to_csv('data/refund_info.csv', index=False)
                else:
                    refund_data.to_csv('data/refund_info.csv', mode='a', header=False, index=False)

                sg.Popup('Submit Successful!')
                break
        window.close()


if __name__ == '__main__':
    RefundFrame().run()

