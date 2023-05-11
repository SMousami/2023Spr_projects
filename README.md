# Mosquitoes in a room 
## A monte carlo simulation of how to repell and kill mosquitoes in a room. 

Mosquitoes are small, flying insects that can cause significant harm to humans and animals. They are known to carry and transmit various diseases, such as malaria, dengue fever, and Zika virus, which can be life-threatening. Mosquito bites can also cause itching, swelling, and irritation, leading to discomfort and potential infection. In addition to their impact on human health, mosquitoes can also harm the environment by disrupting food chains and ecosystems. Despite efforts to control their populations through measures such as insecticide spraying and removing standing water sources, mosquitoes remain a persistent problem in many parts of the world.

In countries like India, there are many companies which advertize and sell machines that release vapours in the air to kill mosquitoes. They claim these liquid vaporizers to be an effective way of killing mosquitoes in an indoor settings. 

![[Source: Amazon.in]](https://github.com/SMousami/2023Spr_projects/assets/40067673/1f9dc5fa-49ce-4deb-8f49-2fcca7d367f1)
Image: A commonly advertized mosquito vaporizer from a famous brand. Source: Amazon.in

In India, the number of people who contract one of the diseases transmitted through mosquitoes runs in millions annually. Personally, I have found myself in a room full of mosquitoes, and really hoped that the vaporizer machine would work as it says. This project is one such work to understand the working of the vaporizer and if it would actually be beneficial. The Monte Carlo simulation utilized in the project aims to study in detail how effective vaporizers are in killing mosquitoes in an indoor room setting. 

# Information about the project files

Access the main_simulation_file.py to see the main code results and perform doctests. The experiments_file.py has the experiments and visualizations and imports the functions_file.py to run the experiments. 

1) main_simulation_file.py contains all the code that forms the design of the study. The file also contains doctest, and the study could be run to obtain statistics about of the design results. 
2) functions_file.py contains a class that has the design for the study and the experiments. This file will be imported into another file to run the experiments
3) experiments_file.py contains the visualizations and results of the experiments. 

# Design


#Validation


#Experiments

#Assumptions

#Hypothesis


### Setting

The experiment will see how effective vaporizers are in killing mosquitoes. 

### Parameters

1) Number of mosquitoes : randomly generated
2) Room orientation and size
3) mosquito positions and movement
4) Diffusion of vaporizer through the room

## Hypothesis

1) The orientation of the room matters for the vaporizer to be effective. The vaporizer works better in a square room instead of a rectangular room. 
2) The presence of a ceiling fan in the room will increase the diffusion rate of vaporizer and improve its effectiveness in killing mosquitoes.

## Monte Carlo simulation

Any experiment with a monte carlo simulation has three phases

1) Designing a simulation
2) Validating the simulation
3) Experiments and predictions
