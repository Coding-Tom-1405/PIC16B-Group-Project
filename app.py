from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import csv
import plotly.express as px
from plotly.io import to_html



import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which is non-interactive and works well with saving files.


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')


# @app.route("/select", methods=['GET', 'POST'])
# def select():
#     if request.method == 'POST':
#         selected_level = request.form.get("level")
#         selected_challenge = request.form.get("challenge")
#         return "Game started with Level: {} and Challenge: {}".format(selected_level, selected_challenge)
#     return render_template('select.html')



def write_to_csv(level, challenge):
    with open('game_setting.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([level, challenge])

@app.route("/select", methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_level = request.form.get("level")
        selected_challenge = request.form.get("challenge")
        write_to_csv(selected_level, selected_challenge) 
        return redirect('http://localhost:8000')
    return render_template('select.html')



@app.route("/play")
def play():
    # Render a template for the web game
    return render_template("play.html")



# Directory to save plots for page stats
PLOTS_DIR = 'static/plots'
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

# @app.route('/stats')
# def stats():
#     file_path='game_data.csv'

#     df = pd.read_csv(file_path)

#     print(df.head())

#     # Print information about the DataFrame
#     print(df.info())

#     # Ensure your game data file exists
#     if not os.path.exists(file_path):
#         return "Game data file not found", 404

#     # Load and process your game data
#     with open(file_path, 'r') as file:
#         # Assuming each row in your CSV has the format: level,result,time_spent
#         df = pd.read_csv(file, names=['Level', 'Result', 'Time Spent'])

#     # Calculate maximum levels for custom processing
#     level_data_custom = pd.DataFrame({'Level': df['Level'].max()})

#     # Plot 1: Histogram of Levels
#     fig1 = px.histogram(df, x='Level', nbins=19, color_discrete_sequence=['skyblue'])
#     fig1.update_layout(title_text='Game Statistics - Custom Processing')

#     # Convert the Plotly figure to an HTML div string
#     plot1_div = to_html(fig1, full_html=False)

#     # Print the generated HTML div string
#     print(plot1_div)

#     # Calculation for avg_time_spent and success_rate needed for Plot 2 and 3
#     avg_time_spent = df.groupby(['Level', 'Result'])['Time Spent'].mean().reset_index()
#     success_rate = df.groupby('Level')['Result'].apply(lambda x: (x == 'correct').mean() * 100).reset_index(name='Success Rate')

#     # Plot 2: Average Time Spent per Level for Correct vs Incorrect Attempts
#     fig2 = px.bar(avg_time_spent, x='Level', y='Time Spent', color='Result',
#                   labels={'Time Spent':'Average Time Spent (seconds)'})
#     fig2.update_layout(title_text='Average Time Spent per Level')

#     # Plot 3: Success Rate per Level
#     fig3 = px.bar(success_rate, x='Level', y='Success Rate',
#                   labels={'Success Rate':'Success Rate (%)'})
#     fig3.update_layout(title_text='Success Rate per Level')

#     # Convert Plotly figures to HTML divs
#     plot1_div = to_html(fig1, full_html=False)
#     plot2_div = to_html(fig2, full_html=False)
#     plot3_div = to_html(fig3, full_html=False)

#     # Pass the divs to the template
#     return render_template('stats.html', plot1_div=plot1_div, plot2_div=plot2_div, plot3_div=plot3_div)

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




#     # Create the histogram plot with KDE for the custom-processed data
#     plt.figure(figsize=(10, 6))
#     ax = sns.histplot(level_data_custom['Level'], bins=range(1, 20), kde=True, color='skyblue', discrete=True)

#     # Set the ticks for x-axis to be at the integers
#     ax.set_xticks(range(1, 11))  # Including the last level

#     # Set title and labels
#     ax.set_title('Game Statistics - Custom Processing', fontsize=16)
#     ax.set_xlabel('Level', fontsize=12)
#     ax.set_ylabel('Density', fontsize=12)

#     # Remove the top and right spines
#     sns.despine()

#     # Save the fig
#     plt.savefig(f'{PLOTS_DIR}/plot1.png')

#     # Load and process the game data

#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     parsed_data = []
#     for line in lines:
#         elements = line.strip().split(',')
#         for i in range(0, len(elements), 3):
#             level = int(elements[i])
#             result = elements[i+1]
#             time_spent = float(elements[i+2])
#             parsed_data.append([level, result, time_spent])

#     df = pd.DataFrame(parsed_data, columns=['Level', 'Result', 'Time Spent'])

#     # Visualization 1: Average Time Spent per Level for Correct vs Incorrect Attempts
#     avg_time_spent = df.groupby(['Level', 'Result'])['Time Spent'].mean().unstack()
#     avg_time_spent.plot(kind='bar', figsize=(10, 6))
#     plt.title('Average Time Spent per Level')
#     plt.ylabel('Average Time Spent (seconds)')
#     plt.xlabel('Level')
#     plt.xticks(rotation=0)
#     plt.legend(title='Result')
#     plt.tight_layout()

#     plt.savefig(f'{PLOTS_DIR}/plot2.png')

#     # Visualization 2: Success Rate per Level
#     plt.clf()

#     # First, calculate the success rates as before
#     success_rate = df.pivot_table(index='Level', columns='Result', aggfunc='size', fill_value=0)
#     success_rate['Success Rate'] = success_rate['correct'] / (success_rate['correct'] + success_rate['incorrect']) * 100

#     # Now, plot only the 'Success Rate' column, without showing the 'incorrect' data
#     success_rate['Success Rate'].plot(kind='bar', figsize=(10, 6), color='blue', legend=False)
#     plt.title('Success Rate per Level')
#     plt.ylabel('Success Rate (%)')
#     plt.xlabel('Level')
#     plt.xticks(rotation=0)
#     plt.tight_layout()

   

#    #plt.savefig(f'{PLOTS_DIR}/plot3.png')
#     plt.savefig(f'{PLOTS_DIR}/plot3_modified.png')

    


if __name__ == "__main__":
    app.run(debug=True)
