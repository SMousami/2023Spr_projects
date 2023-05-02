"""
PR Project

This file is still a working directory. I will be adding each and every function once it is functional here. In the meanwhile,
I will be using a local python file to work on my code.

"""

import random
import numpy as np
import matplotlib.pyplot as plt
import math

#Define the room dimensions; have to change the orientation
room_width = 11
room_breadth = 11
room_height = 10
ceiling_fan_on = False
min_count = 10
max_count = 200 #i think there can be 200 mosq. in a small room - i think there can be more infact. Proof??

def mosquito_count(min_count, max_count):
    return random.randint(min_count, max_count)

print(mosquito_count(10,100))

def generate_mosquito_position(room_width, room_height, room_breadth):
    position = (random.uniform(0, room_width), random.uniform(0, room_height), random.uniform(0,room_breadth))

    return position
position = generate_mosquito_position(11,10,10)

#assume
def generate_nearby_position(position, max_distance=0.1):
    x, y,z = position
    new_x = x + random.uniform(-max_distance, max_distance)
    new_y = y + random.uniform(-max_distance, max_distance)
    new_z = z + random.uniform(-max_distance, max_distance)
    return (new_x, new_y, new_z)
print(generate_nearby_position(position, 0.1))
def generate_vaporizer_position(room_width, room_height):
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    return [x, y,0]
print(generate_vaporizer_position(11,10))

#ceiling_fan_on = 0.05
#ceiling_fan_off = 0.01
def calculate_vaporizer_concentration(position, vaporizer_position, vaporizer_rate, time_passed,
                                      initial_concentration):
    distance = math.sqrt((position[0] - vaporizer_position[0]) ** 2 + (position[1] - vaporizer_position[1]) ** 2 +(position[2] - vaporizer_position[2]) ** 2) #using distance
    concentration = vaporizer_rate / (distance ** 3)
    final_concentration = concentration * (1 - math.exp(-vaporizer_rate * time_passed))
    total_concentration = final_concentration + initial_concentration
    return total_concentration

#work in progress under
concentration = np.zeros(5) #setting all the conc = 0
concentration[0] = 100

for i in range(1, 5):
    print(i)
    diffused_vaporizer = 0.50 * 20
    print(diffused_vaporizer,"d")
    new_concentration = concentration[i - 1] - diffused_vaporizer
    print(new_concentration,"n")
    if new_concentration < 0:
        new_concentration = 0



def calculate_vapor_inhaled(concentration, total_inhaled):
    amount_inhaled = 0.1 * concentration #10% for now, what if the mosquitoes are more or less resilient?
    total_inhaled += amount_inhaled
    return total_inhaled

# below code is still work in progress and hence might not make sense at the moment.
vap = {}
for i, k in enumerate(position):
    x, y, z = k
    c = total_con  # get concentration at mosquito location using function
    inh = c * 0.1 * time  # calculate amount inhaled by mosquito


