import PySimpleGUI as sg
import pandas as pd
import os

def create_table_element(df):
    data = df.values.tolist()
    header_list = list(df.columns)
    col_widths = [(len(max(df[col].astype(str), key=len)) + 1) for col in df.columns]
    return sg.Table(values=data, headings=header_list, col_widths=col_widths,
                    display_row_numbers=False, auto_size_columns=False, num_rows=min(25, len(data)), key='table')

layout = [
    [sg.Text('Select a CSV file from the folder:')],
    [sg.Listbox(values=[], size=(40, 10), key='file_list')],
    [sg.Button('Load Folder'), sg.Button('Load CSV')]
]

window = sg.Window('CSV Viewer', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Load Folder':
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # specify the parent folder of the CSV files
        folder_path = os.path.join(parent_dir, 'data')  # specify the folder containing the CSV files
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        window['file_list'].update(csv_files)

    if event == 'Load CSV':
        if not values['file_list']:
            sg.Popup("Error: Please select a CSV file.")
            continue
        csv_file = values['file_list'][0]
        csv_file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(csv_file_path)

        table_layout = [
            [create_table_element(df)],
            [sg.Button('Close')]
        ]
        table_window = sg.Window('CSV Table', table_layout)
        while True:
            table_event, _ = table_window.read()
            if table_event == 'Close' or table_event == sg.WIN_CLOSED:
                table_window.close()
                break

window.close()




