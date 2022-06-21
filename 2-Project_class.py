##### Markov simulation project: simulation of customers walking around in a supermarket
##### Part 2: Defining the class customers and supermarket
##### 08th of June 2022

import numpy as np
import pandas as pd
from faker import Faker
import random
import time

fake = Faker()

### Create class supermarket
class Supermarket:
    """Manages multiple Customer instances (adds new ones, moves them) over a time period of 07:00 to 22:00. Output in customers_overview.csv
    """

    def __init__(self):        
        """all initial attributes of the supermarket """
        self.customers = []         # List of customers at the current time in the market
        self.minutes = 420          # Shop opens at 07:00 (420 minutes after 00:00)
        self.closing = 1320         # SHop closes at 22:00 (1320 minutes after 00:00)
        self.df_customers = pd.DataFrame(columns = ["minutes", "name", "location"])

    def __repr__(self):
        return ''

    def get_time(self):
        """ returns the current time in HH:MM format.
        """
        self.time = time.strftime("%H:%M", time.gmtime(self.minutes * 60))
        return self.time

    def print_customers(self):
        """print all customers with the current time, name and location in CSV format (Final output)
        """
        self.df_customers = self.df_customers.set_index("minutes")
        self.df_customers.to_csv("customers_overview.csv")

    def next_minute(self):
        """propagates all customers to the next state as long as the supermarket is open
        """
        self.minutes = self.minutes + 1
        churned =[]                         # Collects all customers who were at the checkout at the last time step 
        for i in self.customers:
            if i.is_active() == True:           # Is the customer not in checkout?
                if self.minutes == self.closing:        # Is the market closing at this time step?
                    i.state = "checkout"
                else:
                    i.change_state()            # If the customer was not in checkout and the market is not closing, move according to prob matrix
                update = {"minutes": self.get_time(), "name": i.name, "location": i.state}
                self.df_customers = self.df_customers.append(update, ignore_index=True)
            else:
                churned.append(i)
        for i in churned:
            self.remove_exitsting_customers(i)      # remove all customers who were at checkout last time step
        if self.minutes != self.closing:
            self.add_new_customers()
            self.next_minute()
        else:
            self.print_customers()          # If the market is closing at this time step, don't add customers but save the data into an csv
    
    def add_new_customers(self):
        """randomly creates new customers with the start location entrance
        """
        for i in range(0, random.randint(0,2)):
            new = {"minutes": self.get_time(), "name": fake.name(), "location": "entrance"}
            self.customers.append(Customer(new["name"], new["location"]))
            self.df_customers = self.df_customers.append(new, ignore_index=True)
        return self.df_customers

    def remove_exitsting_customers(self, customer):
        """removes every customer that is not active any more (who was at the checkout last time step)
        """
        self.customers.remove(customer)

    def open(self):
        """ Opens the supermarket at 07:00 and starts with initial number of customers
        """
        self.add_new_customers()
        self.next_minute()



### Create Class customer
class Customer:
    """Class of customers that have an id and can move to other sections with a probability according to the transition matrix
    """
    def __init__(self, name, state):
        self.name = name
        self.state = state
        self.transition_probs = pd.read_csv("transition_matrix_ilona_pascal.csv", index_col="location")

    def __repr__(self):
        return f"The customer {self.name} is currently at the location {self.state}"

    def change_state(self):
        """Customer moves with a certain probability to the next location
        """
        if self.is_active() == True:
            self.state = np.random.choice(a=["checkout", "dairy", "drinks", "fruit", "spices", "entrance"], p=self.transition_probs.loc[self.state])
            return f"The customer {self.name} is currently at the location {self.state}"
        else:
            return f"The customer {self.name} has already left"
        
    def is_active(self):
        """Returns True if the customer has not reached the checkout yet
        """
        if self.state == "checkout":
            return False
        else:
            return True

lidl = Supermarket()
lidl.open()