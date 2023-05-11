"""
IS 597 PR Spring 2023
Project
Title: Monte Carlo simulation of the effectiveness of vaporizers in killing mosquitoes
Submitted by: Mousami Shinde
Date: April 2023
IDE: Pycharm 2022.3.1 Professional Edition
Python version 3.10.11
-------------------------------------------------------------
This project is a Monte Carlo simulation that studies how vaporizers are effective in killing mosquitoes.
File: Experiment Results
Purpose: To demonstrate the results
"""

import functions_file as sim1

s = sim1.VaporizerSimulation(size=10,time=180,vaporizer_locations=[0],fan_speed=0.2)
print(s)

s.validation_of_design(500)
s.experiment_3(10)


