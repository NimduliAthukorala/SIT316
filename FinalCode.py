#!/usr/bin/env python
# coding: utf-8

# # Approach 1

# In[2]:


#import important libraries
from pulp import *
import pandas as pd
import numpy as np
import re

# read csv using pandas
# make sure the csv file is in the same folder as the code and adjest the name accordingly
df = pd.read_csv('WorkDistribution.csv')

# copy the break times to a seperate numpy array
breaks = df["breaks between works"].to_numpy()

# remove the columns that are not needed from the dataframe
df = df.drop(columns="Unnamed: 0")
df = df.drop(columns="breaks between works")

# define the size of the data used
num_works_index = len(df.columns)
num_machines_index = len(df)

# copy the fixed times to an array of list to make it easy to access 
pd.DataFrame(df)
fixed_times = []
for column_index in df:
    current_fixed = []
    for row in df[column_index]:
        current_fixed.append(row)
    fixed_times.append(current_fixed)
    
# define the problem as a minimization and name the problem
optimal_work_distribution = LpProblem("Optimal_Work_Distribution", LpMinimize)

# define variables in the form of a dict for each machine status for every work
all_works = []
for x in range(num_works_index):
    var = str("work_" + str(x+1))
    var = LpVariable.dicts(var, range(0, num_machines_index),cat='Binary')
    all_works.append(var)

# define variables for the number of breaks taken by each machine
all_breaks = []
for x in range(num_machines_index):
    var = str("break_" + str(x+1))
    var = LpVariable(var, cat='Integer', lowBound = 0)
    all_breaks.append(var)
    
# define the objective function
optimal_work_distribution += (lpSum([(all_works[i][j] * (fixed_times[i][j])) 
                                     for i in range (num_works_index) 
                                     for j in range(num_machines_index)]) + 
                              ((all_breaks[k]) * (breaks[k]) for k in range (num_machines_index)))

# define constraints to ensures each work is done exacly one time 
for x in range(num_works_index):
    optimal_work_distribution += lpSum([all_works[x][i] for i in range(0, num_machines_index)]) == 1
    
# define constraints to endure the total breaks is one less than the total works using each machine
for x in range(num_machines_index):
    optimal_work_distribution += all_breaks[x] + 1 == lpSum([all_works[i][x] 
                                                             for i in range(num_works_index)])

# solve the problem
status = optimal_work_distribution.solve()

# display status of the problem
print(f"Solution: {LpStatus[status]}")

# display the optimal time taken
print(f"\nMinimum time taken in minutes: {optimal_work_distribution.objective.value()}\n")

# loop throught the variables and display the important informatiom
for v in optimal_work_distribution.variables():
    if (f"{v.value()}") != '0.0':
        if not ("break" in v.name):
            display_work = re.search('work_(.*)_', v.name)
            display_machine = re.search('_(.*)', v.name)
            display_machine_1 = re.search('_(.*)',display_machine.group(1))
            print(f"\nWork {display_work.group(1)} : runs on machine {int(display_machine_1.group(1))+1}")
        else:
            display_break = re.search('break_(.*)', v.name) 
            print(f"Machine {display_break.group(1)} : took {int(v.value())} breaks")


# # Approach 2

# In[ ]:


#import important libraries
import pandas as pd
import numpy as np
import random

# read csv using pandas
# make sure the csv file is in the same folder as the code and adjest the name accordingly
df = pd.read_csv('WorkDistribution.csv')

# copy the break times to a seperate numpy array
breaks = df["breaks between works"].to_numpy()

# remove the columns that are not needed from the dataframe
df = df.drop(columns="breaks between works")
df = df.drop(columns="Unnamed: 0")

# define the size of the data used
rows = len(df)
cols = len(df.columns)

# initialize a numpy array to store 1s and 0s
work = pd.DataFrame(np.zeros((rows, cols),dtype=int))

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
        
# display the best solution obtained
best_sum

# display the machine activity for the best solution obtained
best_work


# In[ ]:




