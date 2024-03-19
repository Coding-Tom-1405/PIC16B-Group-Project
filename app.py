from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import csv

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
    with open('/Users/gimdong-gyu/Desktop/newProject16B/game_setting.csv', 'a', newline='') as file:
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
PLOTS_DIR = '/Users/gimdong-gyu/Desktop/newProject16B/static/plots'
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

@app.route('/stats')
def stats():
    file_path='/Users/gimdong-gyu/Desktop/newProject16B/game_data.csv'

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

    # Create the histogram plot with KDE for the custom-processed data
    plt.figure(figsize=(10, 6))
    ax = sns.histplot(level_data_custom['Level'], bins=range(1, 20), kde=True, color='skyblue', discrete=True)

    # Set the ticks for x-axis to be at the integers
    ax.set_xticks(range(1, 11))  # Including the last level

    # Set title and labels
    ax.set_title('Game Statistics - Custom Processing', fontsize=16)
    ax.set_xlabel('Level', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)

    # Remove the top and right spines
    sns.despine()

    # Save the fig
    plt.savefig(f'{PLOTS_DIR}/plot1.png')

    # Load and process the game data

    with open(file_path, 'r') as file:
        lines = file.readlines()

    parsed_data = []
    for line in lines:
        elements = line.strip().split(',')
        for i in range(0, len(elements), 3):
            level = int(elements[i])
            result = elements[i+1]
            time_spent = float(elements[i+2])
            parsed_data.append([level, result, time_spent])

    df = pd.DataFrame(parsed_data, columns=['Level', 'Result', 'Time Spent'])

    # Visualization 1: Average Time Spent per Level for Correct vs Incorrect Attempts
    avg_time_spent = df.groupby(['Level', 'Result'])['Time Spent'].mean().unstack()
    avg_time_spent.plot(kind='bar', figsize=(10, 6))
    plt.title('Average Time Spent per Level')
    plt.ylabel('Average Time Spent (seconds)')
    plt.xlabel('Level')
    plt.xticks(rotation=0)
    plt.legend(title='Result')
    plt.tight_layout()

    plt.savefig(f'{PLOTS_DIR}/plot2.png')

    # Visualization 2: Success Rate per Level
    success_rate = df.pivot_table(index='Level', columns='Result', aggfunc='size', fill_value=0)
    success_rate['Success Rate'] = success_rate['correct'] / (success_rate['correct'] + success_rate['incorrect']) * 100
    success_rate['Success Rate'].plot(kind='bar', figsize=(10, 6), color='green')
    plt.title('Success Rate per Level')
    plt.ylabel('Success Rate (%)')
    plt.xlabel('Level')
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(f'{PLOTS_DIR}/plot3.png')

    return render_template('stats.html')


if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import os
# import csv

# import matplotlib
# matplotlib.use('Agg')

# app = Flask(__name__)

# def write_to_csv(level, challenge):
#     with open('Users/nguye/PIC16B-Group-Project/game_setting.csv', 'a', newline = '') as file:
#         writer = csv.writer(file)
#         writer.writerow([level, challenge])      

# @app.route("/")
# def homepage():
#     return render_template('homepage.html')     

# @app.route("/select", methods=['GET', 'POST'])
# def select():
#     if request.method == 'POST':
#         selected_level = request.form.get("level")
#         selected_challenge = request.form.get("challenge")
#         write_to_csv(selected_level, selected_challenge)
#         return redirect('http://localhost:8000')
#     return render_template('select.html')
# @app.route("/play")
# def play():
#     return render_template("play.html")

# PLOTS_DIR = '/Users/nguye/PIC16B-Group-Project/static/plots'
# if not os.path.exists(PLOTS_DIR):
#     os.makedirs(PLOTS_DIR)
# @app.route('/stats')
# def stats():
#     file_path='/Users/nguye/PIC16B-Group-Project/game_data.csv'
    
#     # Read the file line by line as a list of strings
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     # Initialize a list to hold the maximum level for each trial
#     max_levels = []
    
#     # Parse each line
#     for line in lines:
#         # Split the line into components based on the CSV format (assuming comma-separated here)
#         fields = line.strip().split(',')
        
#         # Assuming every third value might represent a level, and it's an integer
#         levels = [int(field) for i, field in enumerate(fields) if i % 3 == 0 and field.isdigit()]
        
#         # Find the maximum level in this trial and append it to the list
#         if levels:  # Ensure the list is not empty
#             max_levels.append(max(levels))
    
#     # Create a DataFrame from the maximum levels
#     level_data_custom = pd.DataFrame({'Level': max_levels})
    
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
    
#     # Show the plot
#     plt.savefig(f'{PLOTS_DIR}/plot1.png')

    
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
#     success_rate = df.pivot_table(index='Level', columns='Result', aggfunc='size', fill_value=0)
#     success_rate['Success Rate'] = success_rate['correct'] / (success_rate['correct'] + success_rate['incorrect']) * 100
#     success_rate['Success Rate'].plot(kind='bar', figsize=(10, 6), color='green')
#     plt.title('Success Rate per Level')
#     plt.ylabel('Success Rate (%)')
#     plt.xlabel('Level')
#     plt.xticks(rotation=0)
#     plt.tight_layout()
    
#     plt.savefig(f'{PLOTS_DIR}/plot3.png')
#     return render_template('stats.html') 


# if __name__ == "__main__":
#     app.run(debug=True)




