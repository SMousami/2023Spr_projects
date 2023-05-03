import random
import numpy as np
import matplotlib.pyplot as plt
import math



def mosquito_count(min_count, max_count):
    return random.randint(min_count, max_count)



def generate_mosquito_position(room_width, room_height, room_breadth):
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    z = random.uniform(0,room_breadth)
    position = [x,y,z]
    return position



def generate_nearby_position(position, max_distance=0.1):
    x, y,z = position
    new_x = x + random.uniform(-max_distance, max_distance)
    new_y = y + random.uniform(-max_distance, max_distance)
    new_z = z + random.uniform(-max_distance, max_distance)
    return [new_x, new_y, new_z]


def generate_vaporizer_position(room_width, room_height):
    x = random.uniform(0, room_width)
    y = random.uniform(0, room_height)
    return [x, y, 0]


#ceiling_fan_on = 0.05
#ceiling_fan_off = 0.01
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



if __name__ == "__main__":
        num = mosquito_count(20,50)
        room_width = 10
        room_height = 10
        room_breadth = 10
        v = generate_vaporizer_position(room_width,room_height)
        dead = 0
        for j in range(num):
            inhaled = 0

            y0 = generate_mosquito_position(room_width, room_height, room_breadth)
            for i in range(1,20):
                f = generate_nearby_position(y0,0.5)
                sec = determine_sections(room_breadth,f)
                vap = calculate_concentration_sections(i,sec)
                inhaled += 0.01 * vap
            if inhaled >= 40:
                dead += 1
            percentage_of_dead_m = dead*100/num
        print(percentage_of_dead_m)
