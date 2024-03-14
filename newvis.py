#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the path to your file
file_path='/Users/owensun/game_data.csv'

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
ax = sns.histplot(level_data_custom['Level'], bins=range(1, 12), kde=True, color='skyblue', discrete=True)

# Set the ticks for x-axis to be at the integers
ax.set_xticks(range(1, 11))  # Including the last level

# Set title and labels
ax.set_title('Game Statistics - Custom Processing', fontsize=16)
ax.set_xlabel('Level', fontsize=12)
ax.set_ylabel('Density', fontsize=12)

# Remove the top and right spines
sns.despine()

# Show the plot
plt.show()

