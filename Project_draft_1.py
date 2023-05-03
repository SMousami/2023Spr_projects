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



def mosquito_count(min_count: int, max_count: int) -> int:
    """
    This function randomly generates a mosquito count which is between the two numbers passed as arguments.
    :param min_count: minimum number of mosquitoes
    :param max_count: maximum number of mosquitoes
    :return: a number that denotes the mosquito population

    >>> random.seed(111)
    >>> mosquito_count(20,50)
    25
    >>> mosquito_count(100,200)
    147
    """
    return random.randint(min_count, max_count)



def generate_mosquito_position(room_width: int, room_height: int, room_breadth: int) -> list:
    """
    This function randomly generates an initial position of a single mosquito within the bounds of the room
    :param room_width: The width of the room
    :param room_height: the height of the room
    :param room_breadth: the breadth of the room
    :return: a list containing the x, y and z coordinate of the mosquito
    >>>random.seed(111)
    generate_mosquito_position(11,10,11)
    [5,6,2]
    """
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    z = random.uniform(0,room_breadth)
    return [x,y,z]



def generate_nearby_position(position: list, max_distance=random.randint(0,2)) -> list:
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
    new_x = x + random.uniform(-max_distance, max_distance)
    new_y = y + random.uniform(-max_distance, max_distance)
    new_z = z + random.uniform(-max_distance, max_distance)
    return [new_x, new_y, new_z]


def generate_vaporizer_position(room_width: int, room_height: int) -> list:
    """
    This function randomly generates the vaporizer location on the wall. The location is on a 2D axis
    :param room_width: width of the room
    :param room_height: height of the room
    :return: returns a list of coordinates
    """
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    return [x, y, 0]



# def calculate_vaporizer_concentration(position, vaporizer_position, vaporizer_rate, time_passed,
#                                       initial_concentration):
#     distance = math.sqrt((position[0] - vaporizer_position[0]) ** 2 + (position[1] - vaporizer_position[1]) ** 2 +(position[2] - vaporizer_position[2]) ** 2) #using distance
#     concentration = vaporizer_rate / (distance ** 3)
#     final_concentration = concentration * (1 - math.exp(-vaporizer_rate * time_passed))
#     total_concentration = final_concentration + initial_concentration
#     return total_concentration
#
# print(calculate_vaporizer_concentration(position, [4.1394139201594795, 2.722154392380809, 0], 0.05, 10,0))





def determine_sections(room_breadth, mosquito_position):
    """
    This function takes in the breadth of the room and divides it into 5 sections. The mosquito position is then run through this function
    to get the section of the room at that point
    :param room_breadth: breadth of the room
    :param mosquito_position: mosquito position in a list
    :return: the section the mosquito is in
    """
    part = 0
    x = room_breadth/5
    if mosquito_position[2] <= x:
        part = 1
    elif mosquito_position[2] <= 2*x:
        part = 2
    elif mosquito_position[2] <= 3*x:
        part = 3
    elif mosquito_position[2] <= 4*x:
        part = 4
    elif mosquito_position[2] < 5*x:
        part = 5
    return part

def calculate_concentration_sections(time_passed, section):
    concentration = int()

    if time_passed == 0:
        concentration[0] = 100
    if section == 1:
        concentration = 100 + 40*time_passed
    elif section  == 2:
        if time_passed == 0:
            concentration = 0
        else:
            concentration = 60 + (time_passed-1)*20
    elif section == 3:
        if time_passed < 2:
            concentration = 0
        else:
            concentration = 40 + (time_passed-2)*20
    elif section == 4:
        if time_passed < 3:
            concentration = 0
        else:
            concentration = 20 + (time_passed-3)*10
    elif section == 5:
        if time_passed < 4:
            concentration = 0
        else:
            concentration = 10 + (time_passed-4)*10
    return concentration

def main_simulation_function(room_width, room_height, room_breadth, time):
    num = mosquito_count(20, 50)
    v = generate_vaporizer_position(room_width, room_height)
    dead = 0
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
        for i in range(500):
            percent_dead_mosquito = main_simulation_function(room_width, room_height, room_breadth, 20)
            list_of_percent_dead.append(percent_dead_mosquito)
        print(np.average(list_of_percent_dead))


















