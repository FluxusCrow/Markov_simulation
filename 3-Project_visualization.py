##### Markov simulation project: simulation of customers walking around in a supermarket
##### Part 3: Visualization (under construction)
##### 13th of June 2022

import numpy as np
import pandas as pd
from faker import Faker
import random
import time
import cv2

TILE_SIZE = 32

MARKET = """
##################
##..............##
##..QA..WP..DS..##
##..QA..WP..DS..##
##..QA..WP..DS..##
##..QA..WP..DS..##
##..QA..WP..DS..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


fake = Faker()

### Create class supermarket
class Supermarket:
    """Manages multiple Customer instances (adds new ones, moves them) over a time period of 07:00 to 22:00. Output in customers_overview.csv
    """

    def __init__(self):        
        """all initial attributes of the supermarket """
        self.customers = []         # List of customers at the current time in the market
        self.minutes = 1318          # Shop opens at 07:00 (420 minutes after 00:00)
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
        #self.df_customers.to_csv("customers_overview.csv")

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
            self.customers.append(Customer(new["name"], new["location"], marketmap=market))
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
    def __init__(self, name, state, marketmap):
        self.marketmap = marketmap
        self.name = name
        self.state = state
        self.transition_probs = pd.read_csv("transition_matrix_ilona_pascal.csv", index_col="location")
        self.tiles = tiles
        self.avatar = self.extract_tile(random.randint(4,8),15)
        self.row = 11
        self.col = 15

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

    def draw(self, frame):
        x = self.col * TILE_SIZE
        y = self.row * TILE_SIZE
        frame[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def move(self):
        if self.state == "entrance":
            new_row = 5
            new_col = 8
        elif self.state == "fruit":
            new_row = random.randint(2,6)
            new_col = 11
        elif self.state == "dairy":
            new_row = random.randint(2,6)
            new_col = 14
        elif self.state == "spices":
            new_row = random.randint(2,6)
            new_col = 5
        elif self.state == "drinks":
            new_row = random.randint(2,6)
            new_col = 3
        else:
            new_row = 8
            new_col = random.choice([3, 7, 11])

        
        if self.marketmap.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row
        else:
            self.col = self.col
            self.row = self.row


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        elif char == "S":
            return self.extract_tile(1, 5)
        elif char == "D":
            return self.extract_tile(1, 6)
        elif char == "P":
            return self.extract_tile(1, 7)
        elif char == "W":
            return self.extract_tile(1, 8)
        elif char == "A":
            return self.extract_tile(1, 9)
        elif char == "Q":
            return self.extract_tile(1,10)
        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":

    background = np.zeros((500, 700, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    market = SupermarketMap(MARKET, tiles)
    lidl = Supermarket()
    lidl.add_new_customers()



    while True:
        time.sleep(1)
        churned = []
        frame = background.copy()
        market.draw(frame)
        for i in lidl.customers:
            i.draw(frame)
            i.change_state()
            print(i.state)
            i.move()
            if i.is_active() == False:
                print("churned")
                churned.append(i)
        lidl.minutes +=1
        lidl.add_new_customers()

        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
       
        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
