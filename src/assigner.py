import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def assigning_bunkhouse(merged_data):
    # Define the bunkhouse names and number of beds
    bunkhouses = {f'BH{i}_{gender}_{session}': 12 for i in range(1, 4) for gender in ['M', 'F'] for session in
                  ['June', 'July', 'August']}

    # Create a dictionary to store the assigned bunkhouses
    assigned_bunkhouses = {bunkhouse: [] for bunkhouse in bunkhouses}

    # Assign bunkhouses for each session and gender
    for session in ['June', 'July', 'August']:
        for gender in ['M', 'F']:
            # Get the subset of the data for the current session and gender
            subset = merged_data[(merged_data['Session'] == session) & (merged_data['Gender'] == gender)]
            # Shuffle the subset to ensure random assignment of bunkhouses
            subset = subset.sample(frac=1)
            # Calculate the number of campers in the subset
            num_campers = len(subset)
            # Check if there are more campers than beds available in the bunkhouses
            if num_campers > (len(bunkhouses) * 12):
                raise ValueError(
                    f"There are too many campers for the available bunkhouse capacity in session {session} and gender {gender}.")
            # Sort the subset by age
            subset = subset.sort_values('Age')
            # Split the subset into groups of 12
            groups = [subset.iloc[i:i + 12] for i in range(0, num_campers, 12)]
            # Assign the groups to bunkhouses
            for i, group in enumerate(groups):
                bunkhouse = f'BH{i + 1}_{gender}_{session}'
                assigned_bunkhouses[bunkhouse] = list(group['CamperID'])
                merged_data.loc[group.index, 'Bunkhouse'] = bunkhouse

    return merged_data


def assigning_tribes(df):
    sessions = ['June', 'July', 'August']
    tribes = {}

    for session in sessions:
        session_data = df[df['Session'] == session]
        boys = session_data[session_data['Gender'] == 'M']
        girls = session_data[session_data['Gender'] == 'F']

        for i in range(1, 7):
            tribe_name = f'Tribe{i}_{session}'
            tribe_boys = boys.iloc[(i - 1) * 6:i * 6]
            tribe_girls = girls.iloc[(i - 1) * 6:i * 6]

            tribe_members = pd.concat([tribe_boys, tribe_girls])
            tribes[tribe_name] = tribe_members['CamperID'].tolist()

    tribe_assignments = []

    for index, row in df.iterrows():
        for tribe_name, members in tribes.items():
            if row['CamperID'] in members:
                tribe_assignments.append(tribe_name)
                break

    df['Tribe'] = tribe_assignments
    return df


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
                merged_data['Bunkhouse'] = assigning_bunkhouse(merged_data)['Bunkhouse']
                # assign tribes based on gender, age and session
                merged_data['Tribe'] = assigning_tribes(merged_data)['Tribe']
                # save the assignment data as a csv file
                merged_data.to_csv('assignment.csv', index=False)

        window.close()


if __name__ == '__main__':
    AssignerFrame().run()
