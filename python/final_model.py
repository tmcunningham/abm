# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: Tom Cunningham
"""
# Set backend for matplotlib
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import random
import tkinter
import requests
import bs4
import sys
import timeit

"""
# Start time for reading in CSV
start_time_csv = timeit.default_timer()
"""

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

"""
# End time for reading in CSV
end_time_csv = timeit.default_timer()
print("Time taken to read CSV: " + str(end_time_csv - start_time_csv))
"""

# Set number of sheep, wolves, random movements and size of neighbourhood
# Use arguments given or use defaults if not all arguments provided as ints
try:
    num_of_sheeps = int(sys.argv[1])
    num_of_wolves = int(sys.argv[2])
    num_of_moves = int(sys.argv[3])
    sheep_neighbourhood = int(sys.argv[4])
    wolf_neighbourhood = int(sys.argv[5])
except IndexError:
    num_of_sheeps = 200
    num_of_wolves = 5
    num_of_moves = 1000
    sheep_neighbourhood = 20
    wolf_neighbourhood = 30
    print("Inputs not all provided. " +
          "Defaulting to 200 sheep, 5 wolves, 1,000 moves, " + 
          "20 sheep neighbourhood and 30 wolf neighbourhood.")
except ValueError:
    num_of_sheeps = 200
    num_of_wolves = 5
    num_of_moves = 1000
    sheep_neighbourhood = 20
    wolf_neighbourhood = 30
    print("Inputs not valid integers. " +
          "Defaulting to 200 sheep, 5 wolves, 1,000 moves, " + 
          "20 sheep neighbourhood and 30 wolf neighbourhood.")

# Set whether message should be printed when a sheep is eaten based on input
silent_input = str(input("Receive message when a sheep is eaten? (Y/N): "))

# Set silent based on input. If not recognised, default to silent = True
if silent_input.upper() == "Y":
    print("Messages will be printed.\n")
    silent = False
elif silent_input.upper() == "N":
    print("Messages will be muted.\n")
    silent = True
else:
    print("Could not recognise input. Messages will be muted.\n")
    silent = True
   
"""
# Start time for scraping web data
start_time_web = timeit.default_timer()
"""

try:
    # Get data from course website for first sheep xs and ys
    print("Obtaining web data...")
    r = requests.get("https://www.geog.leeds.ac.uk/courses/computing/"+
                     "practicals/python/agent-framework/part9/data.html")
    
    # Check response is 200
    # print(r)
    
    # Parse HTML and read ys and xs
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    td_ys = soup.find_all(attrs={"class" : "y"})
    td_xs = soup.find_all(attrs={"class" : "x"})
    
    """
    # End time for scraping web data
    end_time_web = timeit.default_timer()
    print("Time taken to scrape web data: " + str(end_time_web - start_time_web))
    """
except requests.exceptions.ConnectionError:
    print("Could not connect to internet. " + 
          "Defaulting to random sheep co-ordinates.")
    td_ys = []
    td_xs = []

# Create empty lists for sheep and wolves
sheeps = []
wolves = []

# Draw plot
fig = matplotlib.pyplot.figure(figsize = (7,7), frameon = False)

"""
# Start time for creating sheep and wolves
start_time_agents = timeit.default_timer()
"""

# Create sheeps
for i in range(num_of_sheeps):
    
    # Use data from web for xs and ys if it exists - after that use random int
    if i < len(td_ys):
        y = int(td_ys[i].text)
    else:
        y = None
    
    if i < len(td_xs):
        x = int(td_xs[i].text)
    else:
        x = None
    
    sheeps.append(agentframework.Sheep(id = i,
                                       x = x,
                                       y = y,
                                       environment = environment, 
                                       agents = sheeps,
                                       speed = 1))

# Create wolves
for i in range(num_of_wolves):
    wolves.append(agentframework.Wolf(id = i, 
                                      environment = environment, 
                                      agents = sheeps,
                                      speed = 3))
    
"""
# End time for creating sheep and wolves
end_time_agents = timeit.default_timer()
print("Time taken to create agents: " + 
      str(end_time_agents - start_time_agents))
"""

# Create stopping variable for animation - runs if true
carry_on = True

# Define update function for animation
def update(frame_number):
    """
    Function used in animation to move sheep and wolves, make them eat, make 
    sheep throw up and make sheep share with neighbours. Plots sheep and
    wolves and updates stopping variable if all sheeps have been eaten.

    Parameters
    ----------
    frame_number : int
        Iteration of the model.

    Returns
    -------
    None.

    """
    global carry_on
    fig.clear()
    
    # Move sheeps
    for i in range(len(sheeps)):
        #print(sheeps[i])
        # Shuffle order of sheeps so priority changes
        random.shuffle(sheeps)
        
        sheeps[i].eat()
        sheeps[i].throw_up()
        sheeps[i].move()
        sheeps[i].share_with_neighbours(sheep_neighbourhood)
    
    # Move wolves
    for i in range(len(wolves)):
        #print(wolves[i])
        # Shuffle order of wolves so priority changes
        random.shuffle(wolves)
        
        wolves[i].eat(wolf_neighbourhood, silent)
        wolves[i].move()
        

    # Plot environment
    matplotlib.pyplot.imshow(environment)
    matplotlib.pyplot.tick_params(left = False, right = False , 
                                  labelleft = False, labelbottom = False, 
                                  bottom = False)
    
    # Plot sheeps
    for i in range(len(sheeps)):
        matplotlib.pyplot.scatter(x = sheeps[i].x, y = sheeps[i].y,
                                  color = "white"
                                  )
    
    # Plot wolves
    for i in range(len(wolves)):
        matplotlib.pyplot.scatter(x = wolves[i].x, y = wolves[i].y,
                                  color = "black"
                                  )
        matplotlib.pyplot.xlim(0, len(environment[0]))
        matplotlib.pyplot.ylim(0, len(environment))
    
    # Update stopping variable if all the sheep have been eaten
    if (len(sheeps) == 0):
        carry_on = False
        print("The wolves have won! All the sheep have been eaten!")
    
        with open("out.txt", "w", newline = "") as f2:
            writer = csv.writer(f2, delimiter = ",")
            for row in environment:
                writer.writerow(row)
                
        # Set sheep stores to just be "EATEN" for output file
        sheep_stores = ["X"] * num_of_sheeps
        
        # print(sheep_stores)
        
        # Write sheeps current stores to a file
        with open("sheep stores.txt", "w", newline = "") as f3:
            writer = csv.writer(f3, delimiter = ",")
            writer.writerow(sheep_stores)

# Stop animation before max number of moves or if stopping condition met
def gen_function():
    """
    Generator function to continue animation. Will stop yielding if all sheep
    have been eaten (so carry_on = False) or if num_of_moves has been reached.

    Yields
    ------
    i : int
        Iteration of the model.

    """
    global carry_on
    i = 0
    while (i < num_of_moves) & (carry_on):
        yield i
        i += 1
    else:
        # Update stopping variable and print sheep survival rate
        carry_on = False
        print("Sheep left: " + str(len(sheeps)) + "\n" +
              "Survival rate: " + str(len(sheeps)/num_of_sheeps))
        
        # Write new environment
        with open("out.txt", "w", newline = "") as f2:
            writer = csv.writer(f2, delimiter = ",")
            for row in environment:
                writer.writerow(row)
                
        # Get list of sheeps current stores by ID
        # Set this to be "X" if they have been eaten
        sheep_stores = []
        for i in range(num_of_sheeps):
            if len([sheep.store for sheep in sheeps if sheep.id == i]) == 0:
                sheep_stores.append("X")
            else:
                sheep_stores.append([sheep.store for \
                                     sheep in sheeps if sheep.id == i][0])
            
        # print(sheep_stores)
        
        # Write sheeps current stores to a file
        with open("sheep stores.txt", "w", newline = "") as f3:
            writer = csv.writer(f3, delimiter = ",")
            writer.writerow(sheep_stores)
            
"""
# Save animation as GIF
animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                               repeat = False,
                                               frames = gen_function(),
                                               save_count = 100)
print("Saving animation...\n")

animation.save("sheep_and_wolves.gif", 
               writer = matplotlib.animation.PillowWriter(fps = 4))

print("Animation saved.")
"""

# Define function to pass to tkinter to run animation
def run():
    """
    Runs the sheep and wolves animation and draws it. Can also be used to
    unpause.

    Returns
    -------
    None.

    """
    global animation
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                                   repeat = False, 
                                                   frames = gen_function())
    canvas.draw()

# Define function to pause the animation in tkinter    
def pause():
    """
    Pauses sheep and wolves animation.

    Returns
    -------
    None.

    """
    try:
        animation.event_source.stop()
    except:
        print("No animation")

# Define function to quit the programme
def exit_model():
    """
    Destroys tkinter window, exits the mainloop and also closes extra figure
    which is created when running code through IDE.

    Returns
    -------
    None.

    """
    global root
    root.destroy()
    matplotlib.pyplot.close("all")
    
# Build main window of GUI and call it model
root = tkinter.Tk()
root.wm_title("Model")

# Create canvas in window
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, 
                                                             master = root)
canvas._tkcanvas.pack(side = tkinter.TOP, fill = tkinter.BOTH, expand = 1)

# Create model menu in window
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label = "Model", menu=model_menu)

# Add command to run model
model_menu.add_command(label= "Run model", command = run)

# Add command to pause model
model_menu.add_command(label = "Pause", command = pause)

# Add command to quit tkinter
model_menu.add_command(label = "Quit", command = exit_model)

# Ready GUI
tkinter.mainloop()


