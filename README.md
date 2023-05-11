# Mosquito Vaporizers: Buy or Pass? 
## A Monte Carlo Simulation of Mosquito Vaporizer effectiveness in a room full of mosquitoes. 

Mosquitoes are small, flying insects that can cause significant harm to humans and animals. They are known to carry and transmit various diseases, such as malaria, dengue fever, and Zika virus, which can be life-threatening. Mosquito bites can also cause itching, swelling, and irritation, leading to discomfort and potential infection. In addition to their impact on human health, mosquitoes can also harm the environment by disrupting food chains and ecosystems. Despite efforts to control their populations through measures such as insecticide spraying and removing standing water sources, mosquitoes remain a persistent problem in many parts of the world. (2)

In countries like India, there are many companies which advertize and sell machines that release vapours in the air to kill mosquitoes. They claim these liquid vaporizers to be an effective way of killing mosquitoes in an indoor settings. 

![[Source: Amazon.in]](https://github.com/SMousami/2023Spr_projects/assets/40067673/1f9dc5fa-49ce-4deb-8f49-2fcca7d367f1)
Image: A commonly advertized mosquito vaporizer from a famous brand. Source: Amazon.in

In India, the number of people who contract one of the diseases transmitted through mosquitoes runs annually in millions. Personally, I have often found myself in a room full of mosquitoes, and really prayed that the vaporizer machine would work as it claims. This project is one such work to understand the working of the vaporizer and if it would actually be beneficial. The Monte Carlo simulation utilized in the project aims to study in detail how effective vaporizers are in killing mosquitoes in an indoor room setting. 

# Information about the project files

Access the main_simulation_file.py to see the main code results and perform doctests. The experiments_file.py has the experiments and visualizations and imports the functions_file.py to run the experiments. 

1) main_simulation_file.py contains all the code that forms the design of the study. The file also contains doctest, and the study could be run to obtain statistics about of the design results. 
2) functions_file.py contains a class that has the design for the study and the experiments. This file will be imported into another file to run the experiments
3) experiments_file.py contains the visualizations and results of the experiments. 

## Design

#### Mosquito
A random number of mosquito is assumed to exist in the room for every simulation. The random number is between 20 to 50 to replicate real world situations.
These mosquitoes are spread through out the room and their initial position is also randomly determined. All the mosquitoes are randomly moved a distance (or not) such that they are not in the same position throughout the simulation run. The mosquitoes inhale the vapours that the vaporizer emits, and their position in the room determines how much vapours they have inhaled at any point of time. The mosquitoes have a threshold of inhalation of the vapours, after which they die due to having too much vapours in their system. 

#### Setting
The setting is that of an indoor room. The room is divided into sections along it's length. The vaporizer can be present in any of these sections and emits a steady flow of vapours into the air. The vapours diffuse through the air throughout the rooms. For the sake of simplicity, within each section the concentration is assumed to be uniform. The vapours also loose their effectiveness after 30 mins of being in the air. 

Variables

1) Time_intervals: the runtime of one simulation in minutes
2) vaporizer_location: A list of sections in which the vaporizer is plugged in
3) Emission_rate: how many units of vapour is the vaporizer emitting per minute
4) diffusion_rate: The flow of vapours from one section to the next per minute
5) chemical_duration: The effectiveness duration of the vapours
6) fan_speed: speed assigned for the fan on a scale of 0 to 0.5 with 0 denoting the fan is turned off
7) max_distance: the maximum distance a mosquito can travel
8) min_count: minimum possible number of mosquitoes
9) max_count: maximum possible number of mosquitoes
10) ingest_coefficient: the amount the mosquito inhales in a minute
11) threshold: the amount the mosquito can inhale without harming itself


## Validation

To validate the design, the following study was used to understand what the results should be in a room of dimensions 6.8 * 3.4 * 2.7. The study had gotten a knockout rate of 56.7% with an interal of 7.3%.(1) The Monte carlo simulation gives similar results when the room length is 7 units, the fan flow is really low and there is only one vaporizer in the room at the corner of the room. When this simulation is ran 1000 times, it gives a statistically convergent plot shown below. 

Note: The below figure shows the survival rate, which is 1 - knockout rate. Hence the average knockout rate should be around 57 %. 

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/9d26c8b1-3310-4f1c-8b9b-65041abc098b)


## Experiments

#### Hypothesis 1: The orientation of the room has an effect on the vaporizer diffusion 

Assumptions: 
1) Fan speed will be kept at a minimum speed of 0 (0 is the lowest and 0.5 is highest)
2) There will be only one vaporizer in the corner most section of the room.
3) The experiment will run for 180 minute
4) The diffusion rate of the vaporizer is 0.2 units per minute.
5) The mosquito inhalation threshold will be 70 
6) We are placing vaporizers on one of the walls of the room. In this experiment, we will consider volume into account and try to factor it into diffusion values to work with the current structure. 

How assumption (6) will work:

Assuming a 8 (L) * 6 (W)* 10 (H), we can consider two orientations: 

  a) 8 sections where the vaporizer is place on the shorter side (6 width wall) 
  b) 6 sections where the vaporizer is placed on the longer wall (8 length wall)
  
In case a), the diffuser emits to a volume of 6 * 1 * 1 in each section (8 sections), in case b), the vaporizer emits to a volume of 8 * 1 * 1 in 6 sections. 
The adjusted concentrations in section a) will be normalized to a factor of 1/6 and 1/8 for section b).
Taking this into account, our normalized emission rates for a) 8 sections is 100 (baseline) and b) 6 sections is 100*6/8 = 75
  
Room Size = 6, average survival rate = 72%
  
  ![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/a0d83a28-652d-4903-b8b7-b282312d0fee)
  
Room Size = 8, average survival rate = 68%
 
![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/ceadace0-312d-413e-9834-f00166d7893e)

Conclusion: The difference between the mean values is within 5% and the histograms show a similar frequency trend for the rest of the values. Based on this results, the difference can be termed as negligent. 


#### Hypothesis 2: The presence of a ceiling fan in the room will improve vaporizer's effectiveness in killing mosquitoes.

Assumptions: 
1) The length of the room is 10 units
2) The fan speed will be vaired for each experiment run
3) There will be two vaporizers at either end of the room
4) The time interval for the simulations will be 180 min

Fan speed = 0, average survival rate = 46%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/67d969b1-8265-4a1f-8f13-0de1a6b1e5c7)

Fan Speed = 0.1, average survival rate = 43%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/6583354a-fad9-471c-826b-3e9f732ecfcc)

Fan Speed = 0.2, average Survival rate = 42%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/22459e78-a731-4f75-af03-db40d8d01528)

Fan Speed = 0.3, average survival rate = 39%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/7aa0f73c-61f6-4725-bf84-74b0522758a4)

Fan speed = 0.4, average survival rate = 39%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/dcc3eb53-acce-42b7-a64e-8133d30bf002)

Fan Speed = 0.5, average survival rate = 38%

![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/29616961-f57e-412b-9163-80f000ae0a2a)

Conclusion: Fan speed decreases the survival rate at first, however as the fan speed approaches maximum speed, the drop off gets smaller for the survival rate. 

#### Hypothesis 3: The best vaporizer position would be when it is kept at the either ends of the room. 

Assumptions:

1) The size of the room is 10
2) The time interval of the experiment would be 180 minutes
3) Fan speed is kept at the middle (0.3) speed.

The top best vaporizer positions are:

36% survival rate at position 2 and 4
![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/60444230-4c7e-4140-bf0d-7bf81b1aaf41)

36% survival rate at position 1 and 3
![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/1f9d15b7-15df-464a-8709-c5d648260700)

37% survival rate at position 0 and 5
![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/70cfc574-51b2-4291-a990-3084ca9a682f)

37% for position 3 and 9
![image](https://github.com/SMousami/2023Spr_projects/assets/40067673/eb7f3d3f-1e1d-495e-8bf8-0d7b07b18e49)

Conclusion: Positions closer to each other and one position in the middle seems to be much effective at having a lower surivival rate. 

## References

1) Validation: Hun Jung, Huijun An, Minjin Lee, Jieun Lee, Jun-Hyung Tak, Comparative Efficacy of Commercial Liquid and Mat-Type Electric Vaporizer Insecticides Against Asian Tiger Mosquito (Diptera: Culicidae), Journal of Medical Entomology, Volume 58, Issue 6, November 2021, Pages 2274–2283, https://doi-org.proxy2.library.illinois.edu/10.1093/jme/tjab087
2) https://www.who.int/docs/default-source/searo/india/health-topic-pdf/vbd-fact-sheets.pdf?sfvrsn=c1908b04_2
