# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import random
import operator
import matplotlib.pyplot

# Set number of agents and number of random movements
num_of_agents = 10
num_of_moves = 2

# Create empty list for co-ords.
agents = []

# Create random starting co-ords for a 100x100 grid.
for i in range(num_of_agents):
    agents.append([random.randint(0, 99),
                   random.randint(0, 99)])

# Change starting co-ords twice based on random numbers.
for i in range(num_of_agents):
    for j in range(num_of_moves):
        for k in (0,1):
            if random.random() < 0.5:
                agents[i][k] = (agents[i][k] + 1) % 100
            else:
                agents[i][k] = (agents[i][k] - 1) % 100

'''
# Work out the distance between the two sets of co-ords.
distance = ((agents[1][0]-agents[0][0])**2 + (agents[1][1]-agents[0][1])**2)**0.5
print(distance)
'''

# Get the co-ords of the agent furthest east.
east_agent = max(agents, key = operator.itemgetter(1))

# Plot of agents
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i][1],agents[i][0])
matplotlib.pyplot.show()

print(agents)