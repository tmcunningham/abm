# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import matplotlib
import agentframework
import csv
import random
import tkinter

matplotlib.use("TkAgg")

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

# Set number of sheep, random movements and size of neighbourhood
num_of_sheeps = 100
num_of_wolves = 5
num_of_moves = 100
sheep_neighbourhood = 20
wolf_neighbourhood = 20

# Create empty list for sheep
sheeps = []
wolves = []

# Get list of tableau colour palette
colors = list(matplotlib.colors.TABLEAU_COLORS.values())

# Draw plot
fig = matplotlib.pyplot.figure(figsize = (7,7))
ax = fig.add_axes([0, 0, 1, 1])

# Create sheeps
for i in range(num_of_sheeps):
    sheeps.append(agentframework.Sheep(id = i, 
                                       environment = environment, 
                                       agents = sheeps,
                                       speed = 1))

for i in range(num_of_wolves):
    wolves.append(agentframework.Wolf(id = i, 
                                      environment = environment, 
                                      agents = sheeps,
                                      speed = 5))

# Create stopping condition for animation
carry_on = True

# Define update function for animation
def update(frame_number):
      
    global carry_on
    fig.clear()
    
    # Move sheeps.
    for i in range(len(sheeps)):
        #print(sheeps[i])
        random.shuffle(sheeps)
        
        sheeps[i].move()
        sheeps[i].eat()
        sheeps[i].throw_up()
        sheeps[i].share_with_neighbours(sheep_neighbourhood)
        
    for i in range(len(wolves)):
        #print(wolves[i])
        random.shuffle(wolves)
        
        wolves[i].move()
        wolves[i].eat(wolf_neighbourhood)

    # Plot sheeps
    matplotlib.pyplot.imshow(environment)
    for i in range(len(sheeps)):
        matplotlib.pyplot.scatter(x = sheeps[i].x, y = sheeps[i].y,
                                  color = "white"
                                  #color = colors[sheeps[i].id % len(colors)]
                                  )
    
    for i in range(len(wolves)):
        matplotlib.pyplot.scatter(x = wolves[i].x, y = wolves[i].y,
                                  color = "black"
                                  #color = colors[wolves[i].id % len(colors)]
                                  )
    
    
    # Create list of all sheeps stores
    #stores = [int(sheep.store) for sheep in sheeps]
    #print(stores)
    
    # Update stopping condition if all sheeps have over 70 store
    if (all(i > 70 for i in [sheep.store for sheep in sheeps])):
        carry_on = False
        print("stopping condition - all sheeps have over 70 store")

# Stop animation before max number of moves or if stopping condition met
def gen_function():
    global carry_on
    i = 0
    while (i < num_of_moves) & (carry_on):
        yield i
        i += 1
    else:
        carry_on = False
        print("Sheep left: " + str(len(sheeps)) + "\n" +
                  "Survival rate: " + str(len(sheeps)/num_of_sheeps))
        
        # Write new environment
        with open("out.txt", "w", newline = "") as f2:
            writer = csv.writer(f2, delimiter = ",")
            for row in environment:
                writer.writerow(row)
                
        # Get list of sheeps current stores
        sheep_stores = []
        for sheep in sheeps:
            sheep_stores.append(sheep.store)
            
        print(sheep_stores)
        
        # Write sheeps current stores to a file
        with open("sheep stores.txt", "a", newline = "") as f3:
            writer = csv.writer(f3, delimiter = ",")
            writer.writerow(sheep_stores)


# Animate plot of sheeps on environment
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                               repeat = False, 
                                               frames = gen_function())
    canvas.draw()

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master = root)
canvas._tkcanvas.pack(side = tkinter.TOP, fill = tkinter.BOTH, expand = 1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop()