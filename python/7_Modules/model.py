# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import matplotlib.pyplot
import agentframework
import csv
import random
import sys
import distutils.util

# Create empty list for environment raster data
environment = []

# Read in CSV raster data
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row: 
            rowlist.append(value)
        environment.append(rowlist)

# Convert string input for whether to have visual output to boolean
try:
    visual_output = bool(distutils.util.strtobool(sys.argv[4]))
except:
    visual_output = True
    

# Plot environment data
if visual_output:
    matplotlib.pyplot.imshow(environment)
    matplotlib.pyplot.show()

# Set number of agents and number, random movements and size of neighbourhood
try:
    num_of_agents = int(sys.argv[1])
    num_of_moves = int(sys.argv[2])
    neighbourhood = int(sys.argv[3])
except IndexError:
    num_of_agents = 10
    num_of_moves = 100
    neighbourhood = 20
    print("Inputs not all provided. " +
          "Defaulting to 10 agents, 100 moves, 20 neighbourhood.")
except ValueError:
    num_of_agents = 10
    num_of_moves = 100
    neighbourhood = 20
    print("Inputs not valid. " +
          "Defaulting to 10 agents, 100 moves, 20 neighbourhood.")

# Create empty list for agents
agents = []

# Create agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))

# Move agents.
for j in range(num_of_moves):
    random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)

# Plot the agents and environment
if visual_output:
    matplotlib.pyplot.imshow(environment)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
    matplotlib.pyplot.show()

# Write new environment
with open("out.txt", "w", newline = "") as f2:
    writer = csv.writer(f2, delimiter = ",")
    for row in environment:
        writer.writerow(row)

# Get list of agents current stores
agent_stores = []
for agent in agents:
    agent_stores.append(agent.store)

# Write agents current stores to a file
with open("agent stores.txt", "a", newline = "") as f3:
    writer = csv.writer(f3, delimiter = ",")
    writer.writerow(agent_stores)

print("agents=" + str(num_of_agents) + 
      ", total_store=" + str(sum(agent_stores)))
# Check agent creation is including other agents
# print(agents[0].agents[1].x, agents[1].x, agents[0].x)
