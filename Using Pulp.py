#!/usr/bin/env python
# coding: utf-8

# # World Problems solved using Python pulp

# ### Import and setup data

# In[ ]:


#import important libraries
from pulp import *
import pandas as pd
import numpy as np
import re


# In[2]:


# read csv using pandas
# make sure the csv file is in the same folder as the code and adjest the name accordingly
df = pd.read_csv('WorkDistribution.csv')


# In[3]:


# copy the break times to a seperate numpy array
breaks = df["breaks between works"].to_numpy()


# In[4]:


# remove the columns that are not needed from the dataframe
df = df.drop(columns="Unnamed: 0")
df = df.drop(columns="breaks between works")


# In[5]:


# define the size of the data used
num_works_index = len(df.columns)
num_machines_index = len(df)


# In[6]:


# copy the fixed times to an array of list to make it easy to access 
pd.DataFrame(df)
fixed_times = []
for column_index in df:
    current_fixed = []
    for row in df[column_index]:
        current_fixed.append(row)
    fixed_times.append(current_fixed)


# ### Define problem and variables

# In[7]:


# define the problem as a minimization and name the problem
optimal_work_distribution = LpProblem("Optimal_Work_Distribution", LpMinimize)


# In[8]:


# define variables in the form of a dict for each machine status for every work
all_works = []
for x in range(num_works_index):
    var = str("work_" + str(x+1))
    var = LpVariable.dicts(var, range(0, num_machines_index),cat='Binary')
    all_works.append(var)


# In[9]:


# define variables for the number of breaks taken by each machine
all_breaks = []
for x in range(num_machines_index):
    var = str("break_" + str(x+1))
    var = LpVariable(var, cat='Integer', lowBound = 0)
    all_breaks.append(var)


# ### Define Objective Function

# In[10]:


# define the objective function
optimal_work_distribution += (lpSum([(all_works[i][j] * (fixed_times[i][j])) 
                                     for i in range (num_works_index) 
                                     for j in range(num_machines_index)]) + 
                              ((all_breaks[k]) * (breaks[k]) for k in range (num_machines_index)))


# ### Define Constraints

# In[11]:


# define constraints to ensures each work is done exacly one time 
for x in range(num_works_index):
    optimal_work_distribution += lpSum([all_works[x][i] for i in range(0, num_machines_index)]) == 1


# In[12]:


# define constraints to endure the total breaks is one less than the total works using each machine
for x in range(num_machines_index):
    optimal_work_distribution += all_breaks[x] + 1 == lpSum([all_works[i][x] 
                                                             for i in range(num_works_index)])


# ### Solve problem and display information

# In[32]:


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
            


# In[ ]:




