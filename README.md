# Markov simulation

## General info
Class based simulation of customers moving in a supermarket between different aisles. Movement is based on a Markov model. Including simple visualization. The project consists of three parts:
1. *1-Project_transition_matrix.ipynb* contains data exploration and calculates the transition matrix, which will be saved as transition_matrix.csv
2. *2-Project_class.py* contains the classes supermarkt and customer. The supermarket opens and customers randomly enter the supermarket until it closes. At closing time the programm will save customer_overview.csv including all customers that visited the supermarket on that day and at which time they were at the single aisles.
3. *3-Project_class.py* runs a simple visualization of the process described in 2.

## Technologies
* Python 3.9.7
* libraries and its versions are listed in requirements.txt and can be installed with:
```
$ conda install --name <environment_name> --file requirements.txt
```

## Setup
1. To have a look at the data exploration, run jupyter notebook and open *1-Project_transition_matrix.ipynb*

2. To create a csv of the customers of that day, run in the terminal:
```
$ python 2-Project_class.py
```

3. To be entertained by the simple visualization, run in the terminal:
```
$ python 3-Project_visualization.py
```
To stop the visualization press *q*
