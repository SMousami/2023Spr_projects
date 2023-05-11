"""
IS 597 PR Spring 2023
Project
Title: Monte Carlo simulation of the effectiveness of vaporizers in killing mosquitoes
Submitted by: Mousami Shinde
Date: May 10, 2023
IDE: Pycharm 2022.3.1 Professional Edition
Python version 3.10.11
File: Design
Purpose: This file is for the design of the simulation
-------------------------------------------------------------
This project is a Monte Carlo simulation that studies how vaporizers are effective in killing mosquitoes.
"""

import random
import numpy as np
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
                        ingested_concentration: float, mosquitoes_status: int):
    """
    This function generates the concentration of chemicals absorbed by the mosquito and its current status as dead or alive.
    :param inhalation_rate: rate of ingestion of the liquid vapours in the air by the mosquito
    :param inhalation_threshold: the maximum ingestion a mosquito can have without dying, after which it will die
    :param current_concentration: the current concentration at the position of the mosquito
    :param mosquito_zone: the array with the section the mosquitoes are present in
    :param ingested_concentration: the ingested concentration of the liquid vaporizer by the mosquito
    :param mosquitoes_status: dead/alive status of mosquitoes with 0 representing death
    :return: the concentration and the mosquito status
    >>> f, h = mosquito_inhalation(0.02, 100, np.array([80,70,60]), 2, 10, 1)
    >>> f == 11.2
    True
    >>> h == 1
    True
    >>> f2, h2 = mosquito_inhalation(0.02, 10, np.array([80,70,60]), 2, 10, 1)
    >>> h2 == 1
    False
    >>> f2 == 11.2
    False
    """
    if ingested_concentration < inhalation_threshold:
        ingested_concentration = ingested_concentration + current_concentration[mosquito_zone] * inhalation_rate
        mosquitoes_status = 1
    else:
        mosquitoes_status = 0

    return ingested_concentration, mosquitoes_status


def starting_point_data_structure(number_of_sections, min_mosquito_count, max_mosquito_count):
    """
    This function provides a starting np arrays for all the mosquito related information.
    :param number_of_sections: The total number of sections in the room
    :param min_mosquito_count: The minimum mosquito count
    :param max_mosquito_count: The maximum mosquito count
    :return: the room concentration, numbers of mosquitoes in the room,location array, section array, concentration array and status array for mosquitoes
    >>> g, z, k, l, m, n = starting_point_data_structure(5,20,50)
    >>> g
    array([0., 0., 0., 0., 0.], dtype=float32)
    >>> z in range(20,50)
    True
    >>> len(k) == z
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
    mosquito_statuses = np.ones(shape=(mosquito_count_in_room,), dtype='int')

    for v in range(0, mosquito_count_in_room):
        mosquito_section[v], mosquito_locations[v] = generate_initial_mosquito_position(number_of_sections)

    return room_conc, mosquito_count_in_room, mosquito_locations, mosquito_section, mosquito_ingested_conc, mosquito_statuses


def diffusion_and_mosquito_position(number_of_sections: int, time_intervals: int, vaporizer_locations: list = None, emission_rate: float = 100, diffusion_rate: float = 0.30,
                                    chemical_effective_duration: int = 30, fan_speed: float = 0.0, max_distance: int = 2, min_count: int = 20, max_count: int = 50,
                                    ingestion_coefficient: float = 0.001, ingestion_threshold: int = 50) -> float:
    """
    :param number_of_sections: number of zones in room/size of the room (each zone is 1 unit measurement)
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
    for t2 in range(time_intervals):
        room_concentration[vaporizer_locations] += emission_rate
        for section in range(number_of_sections - 1):
            difference = room_concentration[section] - room_concentration[section + 1]
            flow = difference * (diffusion_rate + fan_speed)
            room_concentration[section] -= flow
            room_concentration[section + 1] += flow
        if t2 > chemical_effective_duration:
            weights = room_concentration / sum(room_concentration)
            expiry = emission_rate * len(vaporizer_locations) * weights * random.uniform(0.9, 1.1)
            room_concentration = room_concentration - expiry
        for j in range(0,mosquito_counts):
            mosquito_concentrations[j], mosquito_status[j] = mosquito_inhalation(ingestion_coefficient, ingestion_threshold, room_concentration, mosquito_in_section[j],
                                                                                 mosquito_concentrations[j], mosquito_status[j])
            mosquito_in_section[j], mosquito_location[j] = generate_nearby_position(mosquito_location[j], number_of_sections, max_distance)
    return sum(mosquito_status) / len(mosquito_status)


if __name__ == "__main__":
    import time

    print("--------------------------------------------------------------------")
    print("THIS IS A SIMULATION DEMO FILE FOR VAPORIZER EFFECTIVENESS IN A ROOM")
    print("--------------------------------------------------------------------")
    print(
        "Sample values that can be used for demo are size = 10, time = 180, location 1 = 0, location 2 = 9, fan speed = 0.3 ")
    print("                                                                    ")

    while True:
        try:
            size = int(input("Please enter size of 1D section of the room : "))
            if size <= 0:
                raise ValueError
            break
        except ValueError:
            print("Input must be a positive, non-zero integer. Please try again. ")

    while True:
        try:
            t = int(input("Please enter minutes to run the vaporizer for : "))
            if t <= 0:
                raise ValueError
            break
        except ValueError:
            print("Input must be a positive, non-zero integer. Please try again.")

    while True:
        try:
            vap_num = int(input("Please enter the number of vaporizers that will be placed in the room : "))
            if vap_num <= 0:
                raise ValueError
            elif vap_num > int(size)-1:
                raise ValueError
            break
        except ValueError:
            print("Input must be a positive, non-zero integer applicable to the room size. Please try again.")

    vap_list = []
    for i in range(int(vap_num)):
        while True:
            try:
                vaporizer_loc = int(input("Please enter the location to place the vaporizer " + str(int(i) + 1) + " (Between 0 and " + str(int(size) - 1) + " ) : "))
                if vaporizer_loc > int(size)-1:
                    raise ValueError
                break
            except ValueError:
                print("Input must be an integer between 0 and " + str(int(size) - 1) + ". Please try again.")
        vap_list.append(int(vaporizer_loc))
    while True:
        try:
            fan_speed_no = float(input("Please enter the fan speed between 0 to 5 : "))
            if fan_speed_no < 0:
                raise ValueError
            elif fan_speed_no > 5:
                raise ValueError
            break
        except ValueError:
            print("Fans have only limited speeds available. Choose between 0 to 5, with 0 being fan off.")
    print("                                                                    ")
    print("=====================================================")
    print("...........Loading the results for 1 run.............")
    print("=====================================================")
    print("                                                                    ")
    sim = diffusion_and_mosquito_position(number_of_sections=int(size), time_intervals=int(t), vaporizer_locations=vap_list,fan_speed=float(fan_speed_no/10))
    print("Survival rate of mosquitoes at the end of the time period is " + str(round(sim, 2)))
    print("                                                                    ")
    selection = input("Do you want the average results and statistics over a specified amount of runs (y/n) ? : ")
    print("                                                                    ")
    if selection == 'y' or selection == 'Y':
        no_runs = input("Please enter the number of runs : ")
        print("                                                                    ")
        print("Expect 35 seconds runtime for 1000 iterations on 12th Gen Intel(R) Core(TM) i7-1255U - 1.70 GHz 16 GB as benchmark")
        print("                                                                    ")
        print("=====================================================")
        print("..................Loading Statistics.................")
        print("=====================================================")

        t0 = time.time()

        results = []
        for i in range(int(no_runs)):
            sim = diffusion_and_mosquito_position(number_of_sections=int(size), time_intervals=int(t), vaporizer_locations=vap_list, fan_speed=float(fan_speed_no/10))
            results.append(round(sim, 2))

        runtime = time.time() - t0
        max_value = max(results)
        min_value = min(results)
        mean_value = round(sum(results) / len(results), 2)
        print("                                                                    ")
        print("The maximum survival rate of mosquitoes in " + str(no_runs) + " runs is " + str(max_value))
        print("The minimum survival rate of mosquitoes in " + str(no_runs) + " runs is " + str(min_value))
        print("The mean survival rate of mosquitoes in " + str(no_runs) + " runs is " + str(mean_value))
        print("                                                                    ")
        print("The simulation runtime for " + str(no_runs) + " iterations was " + str(round(runtime, 2)) + " seconds")
        print("                                                                    ")
