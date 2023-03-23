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
    # Define the session names and initialize an empty dictionary for tribes
    sessions = ['June', 'July', 'August']
    tribes = {}

    # Loop through each session
    for session in sessions:
        # Filter the DataFrame to get data for the current session
        session_data = df[df['Session'] == session]

        # Filter the session data by gender and sort by age
        boys = session_data[session_data['Gender'] == 'M'].sort_values('Age')
        girls = session_data[session_data['Gender'] == 'F'].sort_values('Age')

        # Loop through the numbers 1 to 6 to create six tribes per session
        for i in range(1, 7):
            # Create a tribe name using the current number and session name
            tribe_name = f'Tribe{i}_{session}'

            # Slice the boys and girls DataFrames to get the members for the current tribe
            tribe_boys = boys.iloc[(i - 1) * 6:i * 6]
            tribe_girls = girls.iloc[(i - 1) * 6:i * 6]

            # Concatenate the boys and girls DataFrames to create a combined DataFrame
            tribe_members = pd.concat([tribe_boys, tribe_girls])

            # Add the tribe name and the list of camper IDs in the tribe to the tribes dictionary
            tribes[tribe_name] = tribe_members['CamperID'].tolist()

    # Initialize an empty list to store tribe assignments
    tribe_assignments = []

    # Loop through each row in the original DataFrame
    for index, row in df.iterrows():
        # Loop through the tribes dictionary to find the tribe that the current camper belongs to
        for tribe_name, members in tribes.items():
            if row['CamperID'] in members:
                # Append the tribe name to the tribe_assignments list
                tribe_assignments.append(tribe_name)
                break

    # Add a new column 'Tribe' to the DataFrame with the values from tribe_assignments
    df['Tribe'] = tribe_assignments

    # Return the modified DataFrame
    return df


def plot_gender_distribution(checkin_data):
    fig = plt.figure()
    sessions = checkin_data['Session'].unique()

    for i, session in enumerate(sessions):
        ax = fig.add_subplot(1, 3, i + 1)
        session_data = checkin_data[checkin_data['Session'] == session]
        ax.bar(session_data['Gender'].unique(), session_data['Gender'].value_counts())
        ax.set_xlabel('Gender')
        ax.set_ylabel('Count')
        ax.set_title(f'Gender Distribution for Session {session}')

    fig.tight_layout()
    return fig


class AssignerFrame:
    def __init__(self):
        self.layout = [
            [sg.Text('Assigner', font=('Helvetica', 20), justification='center', size=(40, 1),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Canvas(size=(400, 300), key='graph')],
            [sg.Button('Assign', font=('Helvetica', 14))]
        ]

    def run(self):
        window = sg.Window('Assigner', self.layout)
        checkin_data = pd.read_csv('checkin_info.csv')
        fig = plot_gender_distribution(checkin_data)

        # Draw the plot using the sg.Canvas element
        fig_canvas_agg = FigureCanvasTkAgg(fig, window['graph'].Widget)
        fig_canvas_agg.draw()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Assign':
                camper_info = pd.read_csv('camper_info.csv')
                merged_data = pd.merge(checkin_data, camper_info[['CamperID', 'Age', 'Session']], on='CamperID')
                merged_data['Bunkhouse'] = assigning_bunkhouse(merged_data)['Bunkhouse']
                merged_data['Tribe'] = assigning_tribes(merged_data)['Tribe']
                merged_data.to_csv('assignment.csv', index=False)

        window.close()


if __name__ == '__main__':
    AssignerFrame().run()
