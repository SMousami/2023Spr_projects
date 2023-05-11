"""
IS 597 PR Spring 2023
Project
Title: Monte Carlo simulation of the effectiveness of vaporizers in killing mosquitoes
Submitted by: Mousami Shinde
Date: May 10, 2023
IDE: Pycharm 2022.3.1 Professional Edition
Python version 3.10.11
-------------------------------------------------------------
This project is a Monte Carlo simulation that studies how vaporizers are effective in killing mosquitoes.
Purpose: Experimentation
File: This file contains the functions necessary to run the experiments
"""

import math
import numpy as np
import random
import matplotlib.pyplot as plt


class VaporizerSimulation:

    def __init__(self, size, time, vaporizer_locations, fan_speed):
        self.size = size
        self.time_intervals = time
        self.vaporizer_locations = vaporizer_locations
        self.emission_rate = 75
        self.diffusion_rate = 0.20
        self.chemical_duration = 30
        self.fan_speed = fan_speed
        self.max_distance = 2
        self.min_count = 20
        self.max_count = 50
        self.ingest_coeff = 0.001
        self.threshold = 70
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

    def mosquito_inhalation(self, state, mosq_zone, mosq_conc, mosq_stat):

        if mosq_conc < self.threshold:

            mosq_conc = mosq_conc + state[mosq_zone] * self.ingest_coeff
            mosq_stat = 1

        else:
            mosq_stat = 0

        return mosq_conc, mosq_stat

    def simulation(self):

        state = np.zeros(shape=(self.size,), dtype='float32')
        mosq_count = self.mosquito_count()
        mosq_loc = np.zeros(shape=(mosq_count,), dtype='float32')
        mosq_zone = np.zeros(shape=(mosq_count,), dtype='int')
        mosq_conc = np.zeros(shape=(mosq_count,), dtype='float32')
        mosq_stat = np.ones(shape=(mosq_count,), dtype='float32')

        for i in range(mosq_count):
            mosq_zone[i], mosq_loc[i] = self.generate_initial_mosquito_position()

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

            for i in range(mosq_count):

                mosq_conc[i], mosq_stat[i] = self.mosquito_inhalation(state, mosq_zone[i], mosq_conc[i], mosq_stat[i])

                mosq_zone[i], mosq_loc[i] = self.generate_nearby_position(mosq_loc[i])

        self.survival_rate = sum(mosq_stat) / len(mosq_stat)

        return self.survival_rate

    def validation_of_design(self, runs):

        list_of_survival = []
        for i in range(runs):
            self.simulation()
            list_of_survival.append(self.survival_rate)

        bins = np.arange(min(list_of_survival), max(list_of_survival) + 0.05, 0.05)
        plt.figure(figsize=(12, 6))
        plt.hist(list_of_survival, bins=bins, alpha=0.5)
        plt.xticks(np.arange(min(list_of_survival), max(list_of_survival) + 0.05, 0.05))
        plt.xlabel("The Survival Rate")
        plt.ylabel("Frequency")
        plt.title('Avg Survival is ' + str(round((sum(list_of_survival) / runs), 2)))
        plt.show()

    def experiment_2(self, runs):
        fan_list = {}
        for speed in np.arange(0.0, 0.6, 0.1):
            fan_list[speed] = []
            for i in range(runs):
                self.simulation()
                fan_list[speed].append(self.survival_rate)
        for i in fan_list:
            bins = np.arange(min(fan_list[i]), max(fan_list[i]) + 0.05, 0.05)
            plt.figure(figsize=(12, 6))
            plt.hist(fan_list[i], bins=bins, alpha=0.5)
            plt.xticks(np.arange(min(fan_list[i]), max(fan_list[i]) + 0.05, 0.05))
            plt.xlabel("The Survival Rate")
            plt.ylabel("Frequency")
            plt.title('Average Survival Rate is ' + str(round((sum(fan_list[i]) / runs), 2)))
            plt.show()

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
                'Avg Survival is ' + str(round((sum(sorted_dict[i]) / runs), 2)) + ' in vapourizer position ' + str(i))
            iteration = iteration + 1
            if iteration == 5:
                break
            plt.show()


