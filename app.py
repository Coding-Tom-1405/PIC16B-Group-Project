from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import seaborn as sns
import plotly.express as px
import os
import csv

app = Flask(__name__)

def write_to_csv(level, challenge):
    with open('game_setting.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([level, challenge])

difficulty_file = "game_setting.csv"

def read_from_csv():
    with open(difficulty_file, 'r') as file:
        last_line = file.readlines()[-1]
        difficulty, time = last_line.strip().split(',')
        return int(difficulty), time
        
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/select", methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_level = request.form.get("level")
        selected_challenge = request.form.get("challenge")
        write_to_csv(selected_level, selected_challenge) 
        return redirect('/confirm')
    return render_template('select.html')

@app.route("/confirm")
def confirm():
    selected_level, selected_challenge = read_from_csv()
    return render_template("confirm.html", level=selected_level, challenge=selected_challenge)

# Directory to save plots for page stats
PLOTS_DIR = 'static/plots'
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

@app.route('/stats')
def stats():
    file_path='game_data.csv'

    # Read the file line by line as a list of strings
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize a list to hold the maximum level for each trial
    max_levels = []

    # Parse each line
    for line in lines:
        # Split the line into components based on the CSV format (assuming comma-separated here)
        fields = line.strip().split(',')

        # Assuming every third value might represent a level, and it's an integer
        levels = [int(field) for i, field in enumerate(fields) if i % 3 == 0 and field.isdigit()]

        # Find the maximum level in this trial and append it to the list
        if levels:  # Ensure the list is not empty
            max_levels.append(max(levels))

    # Create a DataFrame from the maximum levels
    level_data_custom = pd.DataFrame({'Level': max_levels})

    import plotly.express as px

    # Assuming level_data_custom is already defined as in your snippet
    fig = px.histogram(level_data_custom, x='Level',
                        nbins=19, # Number of bins
                        color_discrete_sequence=['skyblue']) # Color
    fig.update_traces(xbins=dict(start=0.5, end=20.5, size=1)) # Ensuring bins cover integer values correctly
    fig.update_layout(title_text='Game Statistics - Custom Processing',
                  xaxis_title_text='Level',
                  yaxis_title_text='Count',
                  bargap=0.2) # Adjust the gap between bars if needed
    fig.show()

    # For saving the figure
    fig.write_image(f"{PLOTS_DIR}/plot1_plotly.png")



    # Assuming avg_time_spent is already calculated as in your snippet
    avg_time_spent = df.groupby(['Level', 'Result'])['Time Spent'].mean().reset_index()
    fig = px.bar(avg_time_spent.reset_index(), x='Level', y=['correct', 'incorrect'],
             labels={'value':'Average Time Spent (seconds)', 'variable':'Result'})
    fig.update_layout(title_text='Average Time Spent per Level',
                  xaxis_title_text='Level',
                  yaxis_title_text='Average Time Spent (seconds)',
                  barmode='group')
    fig.show()

    # For saving the figure
    fig.write_image(f"{PLOTS_DIR}/plot2_plotly.png")


    # Assuming success_rate is already calculated as in your snippet
    fig = px.bar(success_rate, x=success_rate.index, y='Success Rate',
             labels={'Success Rate':'Success Rate (%)'})
    fig.update_layout(title_text='Success Rate per Level',
                  xaxis_title_text='Level',
                  yaxis_title_text='Success Rate (%)')
    fig.show()

    # For saving the figure
    fig.write_image(f"{PLOTS_DIR}/plot3_modified_plotly.png")
    return render_template('stats.html')


if __name__ == "__main__":
    app.run(debug=True)
