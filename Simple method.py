#!/usr/bin/env python
# coding: utf-8

# # World Problems solved using Single States Heuristic

# ### Import and setup data

# In[1]:


#import important libraries
import pandas as pd
import numpy as np
import random


# In[2]:


# read csv using pandas
# make sure the csv file is in the same folder as the code and adjest the name accordingly
df = pd.read_csv('WorkDistribution.csv')


# In[3]:


# copy the break times to a seperate numpy array
breaks = df["breaks between works"].to_numpy()


# In[4]:


# remove the columns that are not needed from the dataframe
df = df.drop(columns="breaks between works")
df = df.drop(columns="Unnamed: 0")


# In[5]:


# define the size of the data used
rows = len(df)
cols = len(df.columns)

# initialize a numpy array to store 1s and 0s
work = pd.DataFrame(np.zeros((rows, cols),dtype=int))


# ### Solving problem using Random

# In[6]:



best_sum = 10000000
best_work = pd.DataFrame(np.zeros((rows, cols),dtype=int))

# loop x times for different random solutions
for x in range(10000):
    col_count = 0
    current_sum = 0
    current_work = work.copy()
    # loop through each column(work)
    for column in df.columns:
        # randomly generate a machine to work on
        index = random.randint(0, 8)
        # for the selected machine add to the sum the time it takes
        current_time = df.loc[index].iat[col_count]
        current_sum += current_time
        # update the empty array with a 1
        current_work.loc[index].iat[col_count] = 1
        
        col_count+=1
        
    total_breaks_sum = 0
    row_count = 0
    # check if breaks are needed and add breaks to total
    for index, breaks_row in current_work.iterrows():
        try:
            values_count = breaks_row.value_counts()
            num_breaks = values_count[1] - 1
            total_breaks_sum = num_breaks * breaks[row_count]
            current_sum += total_breaks_sum
            
        except:
            pass
        row_count += 1
    # obtain the best solution so far    
    if current_sum <= best_sum:
        best_sum = current_sum
        best_work = current_work.copy()


# In[7]:


# display the best solution obtained
best_sum


# In[8]:


# display the machine activity for the best solution obtained
best_work

