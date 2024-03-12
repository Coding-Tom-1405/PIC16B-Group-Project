#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load the data again to ensure it's up-to-date
# Need to change the path
data = pd.read_csv("/Users/owensun/Downloads/fake_game_data.csv")

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))
ax = sns.histplot(data['Level'], bins=30, kde=True, color='skyblue')

# Overlaying the KDE plot
sns.kdeplot(data['Level'], color='blue', ax=ax)

# Enhancing the plot with markers for each bin
for p in ax.patches:
    if p.get_height() > 0:
        plt.plot((p.get_x() + p.get_width() / 2, p.get_x() + p.get_width() / 2), (0, p.get_height()), color='blue', marker='o')

# Set title and labels
ax.set_title('Statistics', fontsize=16)
ax.set_xlabel('Level', fontsize=12)
ax.set_ylabel('Density', fontsize=12)

# Remove the top and right spines
sns.despine()

# Show the plot
plt.show()


# In[20]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming data has already been loaded and is in a pandas DataFrame
# Let's define bins based on the minimum and maximum levels in the data
level_min = data['Level'].min()
level_max = data['Level'].max()
bins = range(level_min, level_max + 2)  # +2 to include the right edge for the last bin

# Create the histogram plot with KDE
plt.figure(figsize=(10, 6))
ax = sns.histplot(data['Level'], bins=bins, kde=True, color='skyblue', discrete=True)



# Overlaying the KDE plot
# Using bw_adjust to smooth the kde curve
#sns.kdeplot(data['Level'], color='blue', ax=ax, bw_adjust=0.3)

# Set the ticks for x-axis to be at the integers
ax.set_xticks(range(level_min, level_max + 1))  # +1 to include the last level

# Enhancing the plot with markers for each bin
bin_centers = [x + 0.5 for x in range(level_min, level_max + 1)]
bin_heights, _ = np.histogram(data['Level'], bins=bins, range=(level_min, level_max + 1))
#for x, y in zip(bin_centers, bin_heights):
    #if y > 0:
        #ax.plot(x, y, color='blue', marker='o')

# Set title and labels
ax.set_title('Game Statistics', fontsize=16)
ax.set_xlabel('Level', fontsize=12)
ax.set_ylabel('Density', fontsize=12)

# Remove the top and right spines
sns.despine()

# Show the plot
plt.show()


# In[ ]:




