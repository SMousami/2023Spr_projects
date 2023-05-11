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
Purpose: Experimentation
File: This file contains the functions necessary to run the experiments and will be imported to the experiments file
"""

import math
import numpy as np
import random
import matplotlib.pyplot as plt


class VaporizerSimulation:

    def __init__(self, size, time, vaporizer_locations, fan_speed, threshold, emission_rate):
        self.size = size
        self.time_intervals = time
        self.vaporizer_locations = vaporizer_locations
        self.emission_rate = emission_rate
        self.diffusion_rate = 0.20
        self.chemical_duration = 30
        self.fan_speed = fan_speed
        self.max_distance = 2
        self.min_count = 20
        self.max_count = 50
        self.ingest_coefficient = 0.001
        self.threshold = threshold
        self.survival_rate = 0

    def mosquito_count(self):

        return random.randint(self.min_count, self.max_count)

    def generate_initial_mosquito_position(self):

        x = random.uniform(0, self.size)
        zone = math.floor(x)
        return zone, x

    def generate_nearby_position(self, position):

        x = position
        max_distance1 = random.randint(0, self.max_distance)

        new_x = x + random.uniform(-max_distance1, max_distance1)

        if new_x >= self.size:
            new_x = new_x - random.uniform(new_x - self.size + 0.1, max_distance1)

        elif new_x < 0:
            new_x = new_x + random.uniform(-new_x, max_distance1)

        zone = math.floor(new_x)

        return zone, new_x

    def mosquito_inhalation(self, state, mosquito_zone, mosquito_conc, mosquito_stat):

        if mosquito_conc < self.threshold:

            mosquito_conc = mosquito_conc + state[mosquito_zone] * self.ingest_coefficient
            mosquito_stat = 1

        else:
            mosquito_stat = 0

        return mosquito_conc, mosquito_stat

    def simulation(self):

        state = np.zeros(shape=(self.size,), dtype='float32')
        mosquito_count = self.mosquito_count()
        mosquito_loc = np.zeros(shape=(mosquito_count,), dtype='float32')
        mosquito_zone = np.zeros(shape=(mosquito_count,), dtype='int')
        mosquito_conc = np.zeros(shape=(mosquito_count,), dtype='float32')
        mosquito_stat = np.ones(shape=(mosquito_count,), dtype='float32')

        for i in range(mosquito_count):
            mosquito_zone[i], mosquito_loc[i] = self.generate_initial_mosquito_position()

        for t in range(self.time_intervals):

            for v in self.vaporizer_locations:
                state[v] += self.emission_rate

            for region in range(self.size - 1):
                difference = state[region] - state[region + 1]
                flow = difference * (self.diffusion_rate + self.fan_speed)
                state[region] -= flow
                state[region + 1] += flow

            if t > self.chemical_duration:
                weights = state / sum(state)
                expiry = self.emission_rate * len(self.vaporizer_locations) * weights * random.uniform(0.9, 1.1)
                state = state - expiry

            for i in range(mosquito_count):

                mosquito_conc[i], mosquito_stat[i] = self.mosquito_inhalation(state, mosquito_zone[i], mosquito_conc[i], mosquito_stat[i])

                mosquito_zone[i], mosquito_loc[i] = self.generate_nearby_position(mosquito_loc[i])

        self.survival_rate = sum(mosquito_stat) / len(mosquito_stat)

        return self.survival_rate

    @staticmethod
    def draw_histogram(incoming_list, simu_runs):
        bins = np.arange(min(incoming_list), max(incoming_list) + 0.05, 0.05)
        plt.figure(figsize=(12, 6))
        plt.hist(incoming_list, bins=bins, alpha=0.5)
        plt.xticks(np.arange(min(incoming_list), max(incoming_list) + 0.05, 0.05))
        plt.xlabel("The Survival Rate")
        plt.ylabel("Frequency")
        plt.title('Average Survival Rate is ' + str(round((sum(incoming_list) / simu_runs), 2)))
        plt.show()

    def experiment(self, runs):
        list_of_survival = []
        for i in range(runs):
            self.simulation()
            list_of_survival.append(self.survival_rate)
        self.draw_histogram(incoming_list=list_of_survival, simu_runs=runs)

    def experiment_2(self, runs):
        fan_list = {}
        for speed in np.arange(0.0, 0.6, 0.1):
            fan_list[speed] = []
            for i in range(runs):
                self.simulation()
                fan_list[speed].append(self.survival_rate)
        for i in fan_list:
            self.draw_histogram(incoming_list=fan_list[i],simu_runs=runs)

    def experiment_3(self,runs):
        vap_list = {}
        locs = []
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in locs and i != j:
                    locs.append((i, j))
                    locs.append((j, i))
                    locs.append((i, i))
                    locs.append((j, j))
                    vap_list[str(i) + ',' + str(j)] = []
                    for p in range(runs):
                        self.simulation()
                        vap_list[str(i) + ',' + str(j)].append(self.survival_rate)

        sorted_dict = dict(sorted(vap_list.items(), key=lambda x: sum(x[1])))
        iteration = 0
        for i in sorted_dict:
            bins = np.arange(min(sorted_dict[i]), max(sorted_dict[i]) + 0.05, 0.05)

            plt.figure(figsize=(12, 6))
            plt.hist(sorted_dict[i], bins=bins, alpha=0.5)
            plt.xticks(np.arange(min(sorted_dict[i]), max(sorted_dict[i]) + 0.05, 0.05))
            plt.title(
                'Avg Survival is ' + str(round((sum(sorted_dict[i]) / runs), 2)) + ' in vaporizer position ' + str(i))
            iteration = iteration + 1
            if iteration == 5:
                break
            plt.show()
