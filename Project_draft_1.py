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
from dataclasses import dataclass
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
    >>> isinstance(a,int)
    True
    """
    return random.randint(min_count, max_count)


def generate_initial_mosquito_position(room_length: int):
    """
    This function randomly generates an initial position of a single mosquito within the bounds of the room
    :param room_length: The length of the room
    :return: The x location of the mosquito and the section in which the mosquito is
    >>> b, c = generate_initial_mosquito_position(10)
    >>> isintance(b, int)
    True
    >>> c <= 10
    True
    >>> c = 14
    False
    """
    initial_position_of_one_mosquito = random.uniform(0, room_length)
    section_of_the_position = math.floor(initial_position_of_one_mosquito)
    return section_of_the_position, initial_position_of_one_mosquito


def generate_nearby_position(previous_position: int, room_length: int, max_distance: float):
    """
    This function takes in the initial position of the mosquito, and generates the next position of the mosquito within the defined bounds
    :param position: the existing position of the mosquito
    :param max_distance: the maximum distance a mosquito can move at a time
    :return: the room section and new position
    >>> d, e = generate_nearby_position(2,10,0.9)
    >>> e <= 2.9
    True
    >>> e>= 1.1
    True
    >>> isinstance(d,int)
    True
    """
    max_distance_randomized = random.randint(0, max_distance)

    new_position = previous_position + random.uniform(-max_distance_randomized, max_distance_randomized)

    if new_position >= room_length:
        new_position = new_position - random.uniform(new_position - room_length, max_distance_randomized)

    elif new_position < 0:
        new_position = new_position + random.uniform(-new_position, max_distance_randomized)

    section = math.floor(new_position)

    return section, new_position


def mosquito_inhalation(ing_coeff, threshold, state, mosq_zone, mosq_conc, mosq_stat):
    if mosq_conc < threshold:

        mosq_conc = mosq_conc + state[mosq_zone] * ing_coeff
        mosq_stat = 1

    else:
        mosq_stat = 0

    return mosq_conc, mosq_stat


def simulation(size: int, time_intervals: int,
               vaporizer_locations: list = [0], emission_rate: float = 100,
               diffusion_rate=0.20, chemical_duration: int = 30,
               fan_speed: float = 0.0, max_distance: int = 2,
               min_count: int = 20, max_count: int = 50,
               ingest_coeff: float = 0.001, threshold: int = 100):
    """

    :param size: number of zones in room/size of the room (each zone is 1 unit measurement)
    :param time_intervals: number of intervals (in minutes) to simulate
    :param vaporizer_locations: which zones have emitters
    :param emission_rate: how much vapor is released per time interval
    :param diffusion_rate: air distribution rate caused by circulation
    :param chemical_duration: number of minutes the chemical remains effective
    :param fan_speed: air distribution rate caused by a fan
    :param max_distance: maximum distance that can be travelled by a mosquito in unit time
    :param min_count: mininum count of mosquitos
    :param max_count: maximum count of mosquitos
    :param ingest_coeff: fraction of concentration that mosquitos can absorb
    :param threshold: value of chemicals at which mosquitos die
    :return:
    """
    # array of regions in the room, assume rectangle

    # initially, whole room has zero concentration
    state = np.zeros(shape=(size,), dtype='float32')

    # find the number of mosquitos in the room
    mosq_count = mosquito_count(min_count, max_count)

    # create an array to track the location of mosquitos at each point in time and initialize the location
    mosq_loc = np.zeros(shape=(mosq_count,), dtype='float32')
    mosq_zone = np.zeros(shape=(mosq_count,), dtype='int')

    # create an array to track the concentration of chemicals ingested by each mosquito
    mosq_conc = np.zeros(shape=(mosq_count,), dtype='float32')

    # create an array to track the status of the mosquito
    mosq_stat = np.ones(shape=(mosq_count,), dtype='float32')

    for i in range(mosq_count):
        mosq_zone[i], mosq_loc[i] = generate_initial_mosquito_position(size)

    for t in range(time_intervals):

        # add new chemical vapor from all vaporizers:
        for v in vaporizer_locations:
            state[v] += emission_rate

        for region in range(size - 1):
            difference = state[region] - state[region + 1]
            flow = difference * (diffusion_rate + fan_speed)
            state[region] -= flow
            state[region + 1] += flow

            # remove chemicals that have expired:
            # remove a randomized portion approximately equal to emission_rate
            # that is based on the
            # proportion of ALL chemicals that are in this region

        if t > chemical_duration:
            weights = state / sum(state)
            expiry = emission_rate * len(vaporizer_locations) * weights * random.uniform(0.9, 1.1)
            state = state - expiry

        # update each mosquito's position & ingested chemicals

        for i in range(mosq_count):
            # amount of chemical ingested at the current location
            mosq_conc[i], mosq_stat[i] = mosquito_inhalation(ingest_coeff, threshold, state, mosq_zone[i], mosq_conc[i],
                                                             mosq_stat[i])

            # update the location of the mosquito
            mosq_zone[i], mosq_loc[i] = generate_nearby_position(mosq_loc[i], size, max_distance)

    return sum(mosq_stat) / len(mosq_stat)




if __name__ == "__main__":
    lista = list()
    for i in range(1000):
        k = simulation(size=10, time_intervals=180, vaporizer_locations=[0, 9], fan_speed=0)
        lista.append(k)
    print(sum(lista) / 1000)



