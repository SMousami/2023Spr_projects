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
    >>>
    >>> a = mosquito_count(20,50)
    >>> a > 20
    True
    >>> a < 50
    True
    >>> isinstance(a,float)
    False
    """
    return random.randint(min_count, max_count)


def generate_initial_mosquito_position(room_length: int):
    """
    This function randomly generates an initial position of a single mosquito within the bounds of the room
    :param room_length: The length of the room
    :return: The x location of the mosquito and the section in which the mosquito is
    >>> b, c = generate_initial_mosquito_position(10)
    >>> isinstance(b, int)
    True
    >>> c <= 10
    True
    >>> c == 14
    False
    """
    initial_position_of_one_mosquito = random.uniform(0, room_length)
    section_of_the_position = math.floor(initial_position_of_one_mosquito)
    return section_of_the_position, initial_position_of_one_mosquito


def generate_nearby_position(previous_position: int, room_length: int, max_distance: float):
    """
    This function takes in the initial position of the mosquito, and generates the next position of the mosquito within the defined bounds
    :param previous_position: the existing position of the mosquito
    :param room_length: the length of the room
    :param max_distance: the maximum distance a mosquito can move at a time
    :return: the room section and new position
    >>> d, e = generate_nearby_position(2,10,0.9)
    >>> e <= 2.9
    True
    >>> e >= 1.1
    True
    >>> isinstance(d,int)
    True
    """
    max_distance_randomized = random.uniform(0, max_distance)

    new_position = previous_position + random.uniform(-max_distance_randomized, max_distance_randomized)

    if new_position >= room_length:
        new_position = new_position - random.uniform(new_position - (room_length-0.1), max_distance_randomized)

    elif new_position < 0:
        new_position = new_position + random.uniform(-new_position, max_distance_randomized)

    section = math.floor(new_position)

    return section, new_position


def mosquito_inhalation(inhalation_rate: float, inhalation_threshold: float, current_concentration: np.ndarray, mosquito_zone: int,
                        ingested_concentration: float, mosquito_status: int):
    """
    This function generates the concentration of chemicals absorbed by the mosquito and its current status as dead or alive.
    :param inhalation_rate: rate of ingestion of the liquid vapours in the air by the mosquito
    :param inhalation_threshold: the maximum ingestion a mosquito can have without dying, after which it will die
    :param current_concentration: the current concentration at the position of the mosquito
    :param mosquito_zone: the array with the section the mosquitoes are present in
    :param ingested_concentration: the ingested concentration of the liquid vaporizer by the mosquito
    :param mosquito_status: dead/alive status of mosquitoes with 0 representing death
    :return: the concentration and the mosquito status
    >>> f, h = mosquito_inhalation(0.02, 100, [80,70,60], 2, 10, 1)
    >>> f == 11.2
    True
    >>> h == 1
    True
    >>> f2, h2 = mosquito_inhalation(0.02, 10, [80,70,60], 2, 10, 1)
    >>> h2 == 1
    False
    >>> f2 == 11.2
    False
    """
    if ingested_concentration < inhalation_threshold:
        ingested_concentration = ingested_concentration + current_concentration[mosquito_zone] * inhalation_rate
        mosquito_status = 1
    else:
        mosquito_status = 0

    return ingested_concentration, mosquito_status


def starting_point_data_structure(number_of_sections, min_mosquito_count, max_mosquito_count):
    """
    This function provides a starting np arrays for all the mosquito related information.
    :param number_of_sections: The total number of sections in the room
    :param min_mosquito_count: The minimum mosquito count
    :param max_mosquito_count: The maximum mosquito count
    :return: the room concentration, numbers of mosquitoes in the room,location array, section array, concentration array and status array for mosquitoes
    >>> g, i, k, l, m, n = starting_point_data_structure(5,20,50)
    >>> g
    array([0., 0., 0., 0., 0.], dtype=float32)
    >>> i in range(20,50)
    True
    >>> len(k) == i
    True
    >>> isinstance(k, np.ndarray)
    True
    >>> l[0] > 5
    False
    >>> n[0] == 1
    True
    >>> n #doctest: +ELLIPSIS
    array([1, 1, ...
    """
    # initially, whole room has zero concentration, hence the below
    room_conc = np.zeros(shape=(number_of_sections,), dtype='float32')

    # find the number of mosquitoes in the room
    mosquito_count_in_room = mosquito_count(min_mosquito_count, max_mosquito_count)

    # creating an array to track the location of mosquitoes at each point in time and initialize the location
    mosquito_locations = np.zeros(shape=(mosquito_count_in_room,), dtype='float32')
    mosquito_section = np.zeros(shape=(mosquito_count_in_room,), dtype='int')

    # creating an array to track the concentration of chemicals ingested by each mosquito
    mosquito_ingested_conc = np.zeros(shape=(mosquito_count_in_room,), dtype='float32')

    # creating an array to track the status of the mosquito
    mosquito_status = np.ones(shape=(mosquito_count_in_room,), dtype='int')

    for i in range(0, mosquito_count_in_room):
        mosquito_section[i], mosquito_locations[i] = generate_initial_mosquito_position(number_of_sections)

    return room_conc, mosquito_count_in_room, mosquito_locations, mosquito_section, mosquito_ingested_conc, mosquito_status

def diffusion_and_mosquito_position(number_of_sections: int, time_intervals: int,vaporizer_locations: list = [0], emission_rate: float = 100, diffusion_rate=0.20,
                                    chemical_effective_duration: int = 30, fan_speed: float = 0.0, max_distance: int = 2,min_count: int = 20, max_count: int = 50,
                                    ingestion_coefficient: float = 0.001, ingestion_threshold: int = 100) -> float:
    """
    :param: number_of_sections: number of zones in room/size of the room (each zone is 1 unit measurement)
    :param time_intervals: number of intervals (in minutes) to simulate
    :param vaporizer_locations: which zones have emitters
    :param emission_rate: how much vapor is released per time interval
    :param diffusion_rate: air distribution rate caused by circulation
    :param chemical_effective_duration: number of minutes the chemical remains effective
    :param fan_speed: air distribution rate caused by a fan
    :param max_distance: maximum distance that can be travelled by a mosquito in unit time
    :param min_count: mininum count of mosquitos
    :param max_count: maximum count of mosquitos
    :param ingestion_coefficient: fraction of concentration that mosquitos can absorb
    :param ingestion_threshold: value of chemicals at which mosquitos die
    :return: A value of survival rate
    >>> p = diffusion_and_mosquito_position(number_of_sections=10, time_intervals=180,vaporizer_locations=[0,1],fan_speed=0.1)
    >>> isinstance(p, float)
    True
    >>> p <= 1
    True
    """
    room_concentration, mosquito_counts, mosquito_location, mosquito_in_section, mosquito_concentrations, mosquito_status = starting_point_data_structure(number_of_sections, min_count, max_count)
    for t in range(time_intervals):
        room_concentration[vaporizer_locations] += emission_rate
        for section in range(number_of_sections - 1):
            difference = room_concentration[section] - room_concentration[section + 1]
            flow = difference * (diffusion_rate + fan_speed)
            room_concentration[section] -= flow
            room_concentration[section + 1] += flow
        if t > chemical_effective_duration:
            weights = room_concentration / sum(room_concentration)
            expiry = emission_rate * len(vaporizer_locations) * weights * random.uniform(0.9, 1.1)
            room_concentration = room_concentration - expiry
        for i in range(0,mosquito_counts):
            mosquito_concentrations[i], mosquito_status[i] = mosquito_inhalation(ingestion_coefficient, ingestion_threshold, room_concentration, mosquito_in_section[i],
                                                                                 mosquito_concentrations[i], mosquito_status[i])
            mosquito_in_section[i], mosquito_location[i] = generate_nearby_position(mosquito_location[i], number_of_sections, max_distance)
    return sum(mosquito_status) / len(mosquito_status)




if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)



