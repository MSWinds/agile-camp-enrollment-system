# a refund system based on the payment system which has the date
# If a request for cancellation and refund is received, the registration clerk must process it. Cancellation of enrollment and refund of payment is allowed as follows: 90% within 3 weeks of mailing of notice of acceptance and arrival instructions; 45% within 6 weeks of mailing; 0% after this. 
# The total amount is 1000 dollars.
# The refund system should be able to calculate the refund amount based on the date of the request.
# The refund system should be able to print out the refund amount and the date of the request.

# build a RefundFrame class with pySimpleGUI.
# The RefundFrame class should have a layout with:
# input the camper id and a button to submit
# then a window will pop up to show the refund amount based on the date of the original payment in previous data set and the date of the original payment.
# output the refund amount, the date of the original payment, and the date of the request in a csv file called refund_info.csv
# The refund_info.csv should have the following columns:
# CamperID, Refund Amount, Date of Original Payment, Date of Request
# The refund_info.csv should be saved in the data folder.

import PySimpleGUI as sg
import pandas as pd
import os
import datetime


class RefundFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Refund Information', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('Camper ID:'), sg.InputText(key='camper_id')],
            [sg.Button('Submit', font=('Helvetica', 14))]]

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

                # Find the original payment date for the camper
                original_payment_date = camper_data.loc[camper_data['CamperID'] == camper_id, 'Date of Original Payment']
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

