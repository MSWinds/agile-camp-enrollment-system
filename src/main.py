import PySimpleGUI as sg
from application_input import ApplicationInputFrame
from assigner import AssignerFrame
from checkin import CheckinFrame


def main():
    # Set PySimpleGUI theme
    sg.theme('LightBlue2')
    # Define GUI layout with three buttons
    frame = [
        [sg.Text('Camp Gila Breath Management System', font=('Helvetica', 20), justification='center', size=(40, 1),
                 relief=sg.RELIEF_RIDGE)],
        [sg.Column([[sg.Button('Register', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Check-in', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Check Availability', size=(30, 2), font=('Helvetica', 14))],
                    [sg.Button('Quit', size=(30, 2), font=('Helvetica', 14))]])]]

    # Create PySimpleGUI window
    window = sg.Window('Camp Gila Breath Management System', frame, element_justification='c').Finalize()

    # Keep window open and responsive to button clicks
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        if event == 'Register':
            ApplicationInputFrame().run()

        if event == 'Check Availability':
            AssignerFrame().run()

        if event == 'Check-in':
            CheckinFrame().run()

    window.close()


if __name__ == '__main__':
    main()
