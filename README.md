# Programming for Social Science Assessment 1: Sheep and Wolves Agent Based Model

This repository contains code to run an agent based model that simulates sheep eating grass in a field, while wolves hunt the sheep. This code was produced following the practical exercises for the GEOG5995 module run by the University of Leeds.

## Contents

Within the **python** folder, this repository contains the following:
- **final_model.py:** file to be run to run the model
- **agentframework.py:** file containing the agent class and sheep and wolf subclasses used in the model
- **in.txt:** text file containing the raster data for the sheeps' environment
- **other folders:** one folder per chapter of the module (except chapter 3), containing earlier versions of the model and agent framework.

## About the Model

### What the model does

This model simulates, for each iteration, and for each sheep and wolf:
- sheep moving in a field 1 space in a random diagonal direction (if they move off the edge of the field, they will loop to the other side)
- sheep eating 10 units of the environment, which is removed from the environment and added to their store
- sheep throwing up if they have eaten over 100 units (this amount will be added to the environment at the sheep's position)
- sheep sharing their current store with any agent within their neighbourhood with less than them
- wolves moving in the field 3 spaces in a random diagonal direction (if they move off the edge of the field, they will loop to the other side)
- wolves eating a sheep if there is one within their defined neighbourhood and adding 1 to their store - the wolf moves to the sheep's position and the sheep is removed from the model

The user will be able to run an animation of the model in a GUI. See below for an example animation of the first 100 iterations of one run of the model: ![sheep_and_wolves_animation](https://github.com/tmcunningham/tmcunningham.github.io/blob/main/images/sheep_and_wolves.gif)

### Running the model

To run the model from the command line, the user should run the following in the directory where the model, agent framework and input files are saved:

	python final_model.py [num_of_sheeps] [num_of_wolves] [num_of_moves] [sheep_neighbourhood] [wolf_neighbourhood]

Where the arguments are (default values given after argument names):
- ```[num_of_sheeps] = 200```: initial number of sheep in the model
- ```[num_of_wolves] = 5```: initial number of wolves in the model
- ```[num_of_moves] = 1000```: number of iterations the model will run for, assuming some sheep survive this long
- ```[sheep_neighbourhood] = 20```: the distance sheep will look for another sheep to share their store with
- ```[wolf_neighbourhood] = 30```: distance wolves will be able to see (and eat) sheep from.

Please note, **all** of the arguments must be specified. If arguments are missing, or if they are not provided as integers, the default values will be used in the model.

When the above code is run, the user will be asked if they want to receive a message every time a sheep is eaten by a wolf in the model (this message includes the sheep's ID, x and y co-ordinates, and store when it was eaten). These messages will be printed to the console. A GUI will then be launched with a "Model" dropdown icon in the menu bar. The "Model" dropdown has three options:
- **Run model:** initiate the model. An animation will begin to play in the current window.
- **Pause:** when the model is running, pause the animation. Select "Run model" again to resume.
- **Quit:** exit the programme.

Once the model has been started, it cannot be re-run without restarting the programme.

### Stopping conditions

Unless the user quits the programme, the model will continue to run until either of the following stopping conditions are met:
- the defined number of moves has been reached, or
- all of the sheep have been eaten by the wolves.

A message will then be printed to the console either displaying the survival rate of the sheep or the number of moves it took the wolves to eat all of the sheep, depending on the stopping condition.

### Outputs

In addition to the animation run in the GUI and the messages printed to the console, the final_model.py script produces two text file outputs:
- **out.txt:** raster data of the sheep's environment after the model has been run - will be affected by sheep eating and throwing up.
- **sheep stores.txt:** list of all sheep's stores, ordered by sheeps' id numbers, as of the end of the model. If a sheep has been eaten, the value in the corresponding position of the list will be ```X```.

Both of these outputs will be overwritten each time the model is run.
