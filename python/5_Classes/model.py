# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import matplotlib.pyplot
import agentframework

def distance_between(agents_row_a, agents_row_b):
    return ((agents_row_a.x-agents_row_b.x)**2 + 
            (agents_row_a.y-agents_row_b.y)**2)**0.5

# Set number of agents and number of random movements
num_of_agents = 10
num_of_moves = 100

# Create empty list for co-ords.
agents = []

# Create agents.
for i in range(num_of_agents):
    agents.append(agentframework.Agent())

# Move agents.
for j in range(num_of_moves):
    for i in range(num_of_agents):
        agents[i].move()

# Create empty list to capture distance measurements
all_distances = []

# Calculate distance between all pairs of agents excluding themselves
for i in range(len(agents)-1):
    distances_from_agent_i = []
    for j in range(len(agents)):
        if j > i:
            distances_from_agent_i.append(distance_between(agents[i], agents[j]))
    all_distances.append(distances_from_agent_i)

# Plot the agents
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
matplotlib.pyplot.show()

