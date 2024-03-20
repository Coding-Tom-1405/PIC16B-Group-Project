from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import csv
import plotly.express as px
from plotly.io import to_html
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which works well with saving files.


def write_to_csv(level, challenge):
    """
    Save the selected game level and timer option to a CSV file.
    """
    with open('game_setting.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([level, challenge])

difficulty_file = "game_setting.csv"

def read_from_csv():
    """
    Read the most recent game setting (level and timer) from the CSV file.
    """
    with open(difficulty_file, 'r') as file:
        last_line = file.readlines()[-1]
        difficulty, time = last_line.strip().split(',')
        return int(difficulty), time


app = Flask(__name__)

@app.route("/")
def homepage():
    """
    Render the homepage of the web.
    """
    return render_template('homepage.html')

@app.route("/select", methods=['GET', 'POST'])
def select():
    """
    Get and store the game level and challenge options.
    """
    if request.method == 'POST':
        selected_level = request.form.get("level")
        selected_challenge = request.form.get("challenge")
        write_to_csv(selected_level, selected_challenge) 
        return redirect('/confirm')
    return render_template('select.html')

@app.route("/confirm")
def confirm():
    """
    Render the confirm page with the last selected game settings.
    """
    selected_level, selected_challenge = read_from_csv()
    return render_template("confirm.html", level=selected_level, challenge=selected_challenge)



# Directory to save plots for page stats
PLOTS_DIR = 'static/plots'
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

@app.route('/stats')
def stats():
    """
    A Flask route that generates statistics from a CSV file containing game data.
    It processes the data to produce plots showing different statistics, such as
    level progression, average time spent per level based on result, and success rate per level.
    These plots are saved as images and also displayed on a webpage.
    """
    file_path = 'game_data.csv'  # Path to the CSV file containing game data

    # Read the file line by line as a list of strings
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize a list to store parsed CSV data
    parsed_data = []
    # Read the CSV file again to parse its content
    with open(file_path, 'r') as file:
        for line in file:
            elements = line.strip().split(',')
            # Process every three elements (assuming level, result, time_spent format)
            for i in range(0, len(elements), 3):
                try:
                    level = int(elements[i])  # Convert the first of every three elements to an integer
                    result = elements[i+1]  # The second element is the result (e.g., win/lose)
                    time_spent = float(elements[i+2])  # The third element is time spent, converted to float
                    parsed_data.append([level, result, time_spent])
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")
    
    max_levels = []  # List to store maximum levels reached in each game
    
    # Process each line to extract maximum levels
    for line in lines:
        fields = line.strip().split(',')
        levels = [int(field) for i, field in enumerate(fields) if i % 3 == 0 and field.isdigit()]
        if levels:
            max_levels.append(max(levels))

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(parsed_data, columns=['Level', 'Result', 'Time Spent'])
    level_data_custom = pd.DataFrame({'Level': max_levels})
    # Plot 1: Histogram of levels reached
    fig1 = px.histogram(level_data_custom, x='Level',
                    nbins=19,  # Sets the number of bins for the histogram, aligning with the range of levels.
                    color_discrete_sequence=['skyblue'])  # Defines the color of the histogram bars.
    # Updates the traces to configure the bin sizes and ranges to ensure they cover integer values of levels correctly.
    fig1.update_traces(xbins=dict(start=0.5, end=20.5, size=1))
    # Sets the layout of the plot, including title and axis labels. Also adjusts the gap between histogram bars for clarity.
    fig1.update_layout(title_text='Game Statistics - Custom Processing',
                  xaxis_title_text='Level',
                  yaxis_title_text='Count',
                  bargap=0.2)
    # fig1.write_image(f"{PLOTS_DIR}/plot1_plotly.png")  # Saves the histogram as an image file in a specified directory.
    fig1.show()  # Displays the plot in the Flask web application interface.

    # Plot 2: Average Time Spent per Level for Correct vs Incorrect Attempts
    avg_time_spent = df.groupby(['Level', 'Result'])['Time Spent'].mean().reset_index()  # Calculates the average time spent per level and result.
    fig2 = go.Figure()  # Initializes an empty figure for plotting.
    # Loops through each unique result (e.g., 'correct', 'incorrect') to add a bar for each level and result combination.
    for result in avg_time_spent['Result'].unique():
        df_filtered = avg_time_spent[avg_time_spent['Result'] == result]  # Filters the data for the current result.
        # Adds a bar trace to the figure for each result with the average time spent per level.
        fig2.add_trace(go.Bar(x=df_filtered['Level'], y=df_filtered['Time Spent'], name=result))
    # Configures the layout of the plot, including the title, axis labels, and setting the bar mode to group for comparison.
    fig2.update_layout(title_text='Average Time Spent per Level',
                   xaxis_title='Level',
                   yaxis_title='Average Time Spent (seconds)',
                   barmode='group')
    fig2.show()  # Displays the plot.
    # fig2.write_image(f"{PLOTS_DIR}/plot2_plotly.png")  # Saves the plot as an image file.

    # Plot 3: Success Rate per Level
    # Calculates the success rate per level by dividing the number of correct results by the total number of attempts.
    success_rate = df[df['Result'] == 'correct'].groupby('Level')['Result'].count() / df.groupby('Level')['Result'].count() * 100
    success_rate = success_rate.reset_index(name='Success Rate')  # Resets index to turn the Series into a DataFrame.
    fig3 = go.Figure(data=go.Bar(x=success_rate['Level'], y=success_rate['Success Rate'], marker_color='blue'))  # Creates a bar plot for success rate.
    # Sets the layout of the plot, including the title and axis labels.
    fig3.update_layout(title_text='Success Rate per Level',
                   xaxis_title='Level',
                   yaxis_title='Success Rate (%)')
    fig3.show()  # Displays the plot.
    # fig3.write_image(f"{PLOTS_DIR}/plot3_plotly.png")  # Saves the plot as an image file.


    return render_template('stats.html')


if __name__ == "__main__":
    app.run(debug=True)
