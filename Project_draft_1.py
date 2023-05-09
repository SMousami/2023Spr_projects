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
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


def mosquito_count(min_count: int, max_count: int) -> int:
    """
    This function randomly generates a mosquito count which is between the two numbers passed as arguments.
    :param min_count: minimum number of mosquitoes
    :param max_count: maximum number of mosquitoes
    :return: a number that denotes the mosquito population

    >>>
    >>> a = mosquito_count(20,50)
    >>> a > 20
    True
    >>> a < 50
    True
    """
    return random.randint(min_count, max_count)

# class room:
#     def __init__(self, breadth, length, width):
#         self.breadth: int
#         self.length: length
#         self.width: width

def generate_mosquito_position(room_width: int, room_height: int, room_breadth: int) -> list:
    """
    This function randomly generates an initial position of a single mosquito within the bounds of the room
    :param room_width: The width of the room
    :param room_height: the height of the room
    :param room_breadth: the breadth of the room
    :return: a list containing the x, y and z coordinate of the mosquito
    >>> b = generate_mosquito_position(11,10,11)
    >>> b[0] < 11
    True
    >>> b[1] < 10
    True
    """
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    z = random.uniform(0,room_breadth)
    return [x,y,z]



def generate_nearby_position(position: list,room_breadth,room_width, room_height, max_distance1) -> list:
    """
    This function takes in the initial position of the mosquito, and generates the next position of the mosquito within the defined bounds
    :param position: the existing position of the mosquito
    :param max_distance: the maximum distance a mosquito can move at a time
    :return: a list with the new coordinates
    >>> random.seed(111)
    >>> generate_nearby_position([2,4,5],0.5)
    [2.4,3.7,5]
    """
    x, y, z = position
    max_distance = random.randint(0,max_distance1)
    new_x = x + random.uniform(-max_distance, max_distance)
    if new_x > room_width:
        new_x = new_x - random.uniform(new_x-room_width,max_distance1)
    elif new_x < 0:
        new_x = new_x + random.uniform(-new_x,max_distance1)

    new_y = y + random.uniform(-max_distance, max_distance)
    if new_y > room_height:
        new_y = new_y - random.uniform(new_y-room_height,max_distance1)
    elif new_y < 0:
        new_y = new_y + random.uniform(-new_y,max_distance1)

    new_z = z + random.uniform(-max_distance, max_distance)
    if new_z > room_breadth:
        new_z = new_x - random.uniform(new_z-room_breadth,max_distance1)
    elif new_z < 0:
        new_z = new_z + random.uniform(-new_z,max_distance1)
    return [new_x, new_y, new_z]

print(generate_nearby_position([1,1,1],10,11,11,4))
def generate_vaporizer_position(room_width: int, room_height: int) -> list:
    """
    This function randomly generates the vaporizer location on the wall. The location is on a 2D axis
    :param room_width: width of the room
    :param room_height: height of the room
    :return: returns a list of coordinates
    """
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    z = random.choice([0,1])
    return [x, y, z]



# def calculate_vaporizer_concentration(position, vaporizer_position, vaporizer_rate, time_passed,
#                                       initial_concentration):
#     distance = math.sqrt((position[0] - vaporizer_position[0]) ** 2 + (position[1] - vaporizer_position[1]) ** 2 +(position[2] - vaporizer_position[2]) ** 2) #using distance
#     concentration = vaporizer_rate / (distance ** 3)
#     final_concentration = concentration * (1 - math.exp(-vaporizer_rate * time_passed))
#     total_concentration = final_concentration + initial_concentration
#     return total_concentration
#
# print(calculate_vaporizer_concentration(position, [4.1394139201594795, 2.722154392380809, 0], 0.05, 10,0))





# def determine_sections(room_breadth, mosquito_position):
#     """
#     This function takes in the breadth of the room and divides it into 5 sections. The mosquito position is then run through this function
#     to get the section of the room at that point
#     :param room_breadth: breadth of the room
#     :param mosquito_position: mosquito position in a list
#     :return: the section the mosquito is in
#     """
#     part = 0
#     x = room_breadth/5
#     if mosquito_position[2] <= x:
#         part = 1
#     elif mosquito_position[2] <= 2*x:
#         part = 2
#     elif mosquito_position[2] <= 3*x:
#         part = 3
#     elif mosquito_position[2] <= 4*x:
#         part = 4
#     elif mosquito_position[2] < 5*x:
#         part = 5
#     return part

# def calculate_concentration_sections(time_passed, section):
#     concentration = int()
#
#     if time_passed == 0:
#         concentration[0] = 100
#     if section == 1:
#         concentration = 100 + 40*time_passed
#     elif section  == 2:
#         if time_passed == 0:
#             concentration = 0
#         else:
#             concentration = 60 + (time_passed-1)*20
#     elif section == 3:
#         if time_passed < 2:
#             concentration = 0
#         else:
#             concentration = 40 + (time_passed-2)*20
#     elif section == 4:
#         if time_passed < 3:
#             concentration = 0
#         else:
#             concentration = 20 + (time_passed-3)*10
#     elif section == 5:
#         if time_passed < 4:
#             concentration = 0
#         else:
#             concentration = 10 + (time_passed-4)*10
#     return concentration

def code_with_window_with_fan(size, time, flowin, factor, window=0, window_flow=0, fan=0, fan_speed=0):
    state = np.zeros((size, time))
    flowout = np.zeros((size, time))
    for t in range(1, time):
        state[0][t] = (state[0][t - 1] + flowin - factor * (state[0][t - 1] + flowin))
        flowout[0][t] = (factor * (state[0][t - 1] + flowin))

    # natural ventilation?

    for s in range(1, size):
        for t in range(1, time):

            # window placement
            # if there is a window, it reduces the concentration at the section, however doesnt impact the flow to later sections
            residual = 0

            if s == window:
                state[s][t] = (state[s][t - 1] + flowout[s - 1][t] - (factor + window_flow) * (
                            state[s][t - 1] + flowout[s - 1][t])) - residual
                flowout[s][t] = (factor * (state[s][t - 1] + flowout[s - 1][t]))
            else:
                state[s][t] = (state[s][t - 1] + flowout[s - 1][t] - factor * (
                            state[s][t - 1] + flowout[s - 1][t])) - residual
                flowout[s][t] = (factor * (state[s][t - 1] + flowout[s - 1][t]))



            if s == fan:
                state[s][t] = (state[s][t - 1] + flowout[s - 1][t] - (factor + fan_speed) * (
                            state[s][t - 1] + flowout[s - 1][t])) - residual
                flowout[s][t] = (factor + fan_speed) * (state[s][t - 1] + flowout[s - 1][t])
            else:
                state[s][t] = (state[s][t - 1] + flowout[s - 1][t] - factor * (
                            state[s][t - 1] + flowout[s - 1][t])) - residual
                flowout[s][t] = (factor * (state[s][t - 1] + flowout[s - 1][t]))



    state[state < 0] = 0

    return state



def mosquito_inhalation(inh_coeff, thres, global_time, mos_pos):
    mosq_ind = {}
    k = code_with_window_with_fan(5,60,100,0.2,0,0,0,0)
    for j in range(len(mos_pos)):

        mos_sec = [] * global_time
        loc_conc = [] * global_time
        absorb = 0

        for t in range(global_time):

            mos_sec[t] = floor(mos_pos[j][t])
            loc_conc[t] = k[mos_sec[t], t]

            if absorb < thres:
                absorb = absorb + loc_conc[t] * inh_coeff

            else:
                mosq_ind[j] = t
                print("mosquito ", j, " dies after ", t, " time periods")
def main_simulation_function(room_width, room_height, room_breadth, time):
    num = mosquito_count(20, 50)
    v = generate_vaporizer_position(room_width, room_height)
    dead = 0
    mos = np.zeros(num)
    for i in range(1,time):
        for j in range(num):
            f = generate_nearby_position(v,4)
            v = f
            mos[j] = code_with_window_with_fan(5,20, 100, 0.2, 0,0,0,0,4,i)
    print(mos)
print(main_simulation_function(10,11,10,60))

for j in range(num):
    inhaled = 0
    y0 = generate_mosquito_position(room_width, room_height, room_breadth)
    for i in range(1, time):
        f = generate_nearby_position(y0, 0.5)
        y0 = f
        sec = determine_sections(room_breadth, f)
        vap = calculate_concentration_sections(i, sec)
        inhaled += 0.01 * vap
    if inhaled >= 40:
        dead += 1
percentage_of_dead_m = dead * 100 / num
return percentage_of_dead_m

if __name__ == "__main__":
        room_width = 10
        room_height = 20
        room_breadth = 15
        list_of_percent_dead = list()



