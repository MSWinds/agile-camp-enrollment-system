import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AssignerFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Assigner', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Graph(canvas_size=(400, 300), graph_bottom_left=(0, 0), graph_top_right=(400, 300), key='graph')],
            [sg.Button('Assign', font=('Helvetica', 14))]
        ]
        self.window = sg.Window('Assigner', self.layout).Finalize()

    def run(self):
        window = sg.Window('Assigner', self.layout).Finalize()
        checkin_data = pd.read_csv('checkin_info.csv')
        # plot the gender distribution of checked-in campers as a bar plot
        fig = plt.figure()
        # get the unique sessions from the checkin data
        sessions = checkin_data['Session'].unique()
        # loop through each session and create a subplot
        for i, session in enumerate(sessions):
            ax = fig.add_subplot(1, 3, i + 1)  # create a subplot with 1 rows and 3 columns
            # filter the checkin data by session
            session_data = checkin_data[checkin_data['Session'] == session]
            # plot the bar chart of gender counts for the session
            ax.bar(session_data['Gender'].unique(), session_data['Gender'].value_counts())
            ax.set_xlabel('Gender')
            ax.set_ylabel('Count')
            ax.set_title(f'Gender Distribution for Session {session}')

        # adjust the figure layout to avoid overlapping labels
        fig.tight_layout()
        # get the figure canvas from the figure object
        fig_canvas_agg = FigureCanvasTkAgg(fig, window['graph'].TKCanvas)

        # draw the figure canvas on the graph element
        fig_canvas_agg.draw()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Assign':
                # read the camper info data
                camper_info = pd.read_csv('camper_info.csv')
                # merge the checkin data with camper info based on CamperID
                merged_data = pd.merge(checkin_data, camper_info[['CamperID', 'Age', 'Session']], on='CamperID')
                # assign bunkhouses based on gender, age and session
                merged_data['Bunkhouse'] = merged_data.apply(self.assigning_bunkhouse, axis=1)
                # assign tribes based on gender, age and session
                merged_data['Tribe'] = merged_data.apply(self.assigning_tribe, axis=1)
                # save the assignment data as a csv file
                merged_data.to_csv('assignment.csv', index=False)

        window.close()

    def assigning_bunkhouse(self, row):
        # define some constants for bunkhouse assignment
        MAX_OCCUPANTS = 12  # maximum number of occupants per bunkhouse
        NUM_BUNKHOUSES = 3  # number of bunkhouses per gender per session

        # get the gender and session of the camper
        gender = row['Gender']
        session = row['Session']

        # create a list of possible bunkhouse names based on gender and session
        bunkhouses = [gender[0].lower() + str(i) + session for i in range(1, NUM_BUNKHOUSES + 1)]

        try:
            # read the existing assignment data if it exists
            assignment = pd.read_csv('assignment.csv')
        except FileNotFoundError:
            # otherwise create an empty dataframe with columns
            assignment = pd.DataFrame(
                columns=['CamperID', 'Last Name', 'Gender', 'Check-in Status', 'Medical Condition',
                         'Dietary Restriction', 'Age', 'Session', 'Bunkhouse', 'Tribe'])

        best_bh = None  # initialize the best bunkhouse name as None
        min_diff = float('inf')  # initialize the minimum difference in age distribution as infinity

        for bh in bunkhouses:
            # get the number of occupants in each bunkhouse
            num_occupants = len(assignment[(assignment['Bunkhouse'] == bh) & (assignment['Session'] == session)])

            if num_occupants < MAX_OCCUPANTS:
                # if there is space available in this bunkhouse

                # get the average age of occupants in this bunkhouse
                avg_age = assignment[assignment['Bunkhouse'] == bh]['Age'].mean() if num_occupants > 0 else row['Age']

                # calculate the difference between this average age and the camper's age
                diff_age = abs(avg_age - row['Age'])

                if diff_age < min_diff:
                    # if this difference is smaller than the current minimum difference
                    min_diff = diff_age  # update the minimum difference
                    best_bh = bh  # update the best bunkhouse name

        return best_bh

    def assigning_tribe(self, row):
        # define some constants for tribe assignment
        NUM_TRIBES = 6  # number of tribes per session
        MAX_CAMPERS = 12  # maximum number of campers per tribe

        # get the gender and session of the camper
        gender = row['Gender']
        session = row['Session']

        # create a list of possible tribe names based on session
        tribes = ['tribe' + str(i) + session for i in range(1, NUM_TRIBES + 1)]  # tribe1July

        try:
            # read the existing assignment data if it exists
            assignment = pd.read_csv('assignment.csv')
        except FileNotFoundError:
            # otherwise create an empty dataframe with columns
            assignment = pd.DataFrame(
                columns=['CamperID', 'Last Name', 'Gender', 'Check-in Status', 'Medical Condition',
                         'Dietary Restriction', 'Age', 'Session', 'Bunkhouse', 'Tribe'])

        for tr in tribes:
            # get the number and ratio of girls and boys in each tribe
            num_girls = len(assignment[(assignment['Tribe'] == tr) & (assignment['Gender'] == 'Girl')])
            num_boys = len(assignment[(assignment['Tribe'] == tr) & (assignment['Gender'] == 'Boy')])
            total_campers = num_girls + num_boys

            if total_campers < MAX_CAMPERS:
                # if there is space available in this tribe
                ratio_girls = num_girls / total_campers if total_campers > 0 else 0.5
                ratio_boys = num_boys / total_campers if total_campers > 0 else 0.5

                # get the average age of campers in this tribe
                avg_age = assignment[assignment['Tribe'] == tr]['Age'].mean() if total_campers > 0 else row['Age']

                # compare these values with the gender and age of the camper
                if gender == 'Girl' and abs(ratio_girls - 0.5) <= 0.1 and abs(avg_age - row['Age']) <= 2:
                    # if this is a girl camper and this tribe has a balanced ratio of girls to boys (within 10%)
                    # and a similar average age (within 2 years)
                    return tr

                elif gender == 'Boy' and abs(ratio_boys - 0.5) <= 0.1 and abs(avg_age - row['Age']) <= 2:
                    # if this is a boy camper and this tribe has a balanced ratio of boys to girls (within 10%)
                    # and a similar average age (within 2 years)
                    return tr

        return None


if __name__ == '__main__':
    AssignerFrame().run()
