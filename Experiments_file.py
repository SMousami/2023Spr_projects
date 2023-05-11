"""
IS 597 PR Spring 2023
Project
Title: Monte Carlo simulation of the effectiveness of vaporizers in killing mosquitoes
Submitted by: Mousami Shinde
Date: May 2023
IDE: Pycharm 2022.3.1 Professional Edition
Python version 3.10.11
-------------------------------------------------------------
This project is a Monte Carlo simulation that studies how vaporizers are effective in killing mosquitoes.
File: Experiment Results
Purpose: To demonstrate the results
"""
import functions_file as sim

# To run the class in which all the functions are stored:
s = sim.VaporizerSimulation(size=10, time=180, vaporizer_locations=[0], fan_speed=0.3, threshold=100, emission_rate=100)

# The experiments will be conducted using the function experiment. Feel free to comment out the codes below as per usage.

# The function experiment runs the simulation and allows finer control. The parameters can be changed in the function above before running the below code
s.experiment(runs=1000)

# Experiment 2 tests hypothesis 2 by creating a list of different fan speeds.
# This same experiment can also be done with the above code (s.experiment) by manually changing the fan speed
# s.experiment_2(runs=100)

# Experiment 3 tries a combination of all the vaporizer positions and gives the top most vaporizer positions.
# s.experiment_3(runs=100)
