#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#here I am changing the code for testing 
#now i'm changing the code on a text editor on my local machine
"""
Michaella Schaszberger
mls2290
Professor Bauer
ENGIE E1006
Homework 4, Project 1--Epidemiology
"""
import random 
import math
from matplotlib import pyplot as plt
def normpdf(x, mean, sd):     
    """     
    Return the value of the normal distribution     
    with the specified mean and standard deviation (sd) at     
    position x.     
    You do not have to understand how this function works exactly.     
    """     
    hello = 180
	var = float(sd)**2     
    denom = (2*math.pi*var)**.5     
    num = math.exp(-(float(x)-float(mean))**2/(2*var))     
    return num/denom
recovery_time = 2
practice_github = 100 #this is a change for practice with git hub
virality = 2
mean = 3
sd = 4
    # recovery time in time-steps  
    # probability that a neighbor cell is infected in                   
    # each time step                                             
class Cell(object):
    def __init__(self,x, y):         
        self.x = x         
        self.y = y         
        self.state = "S"
        # can be "S" (susceptible), "R" (resistant = dead), or "I" (infected)
        self.counter = 0

    def infect(self):
        self.state = "I"
        self.counter = 0
    
    def process(self, adjacent_cells):
#this method first checks whether the cell is infected and if it is it first checks if it dies
#before the counter equals the recovery time
#then it checks when the counter is equal to or greater than the recovery time and if the
#cell's mortality is less than the mortality probabiltiy, then the cell dies and the counter is
#reset to zero so that the next cell can use the counter
#otherwise, the cell recovers 
#if the cell neither dies nor recovers, it infects other cells
#order matters (check if it dies, recovers, or infects)
        mortality = random.random()
        mortality_probability = normpdf(self.counter,mean,sd)
        if self.state == "I": #only care about how the infected cells are behaving
            if mortality <= mortality_probability: #can die at any step irregardless of recovery_time
                self.state = "R"
                self.counter = 0
            else: #if the cell doesn't die, then it could recover
                if self.counter >= recovery_time: #cell only recovers after recovery_time
                    self.state = "S" #recovers after counter is equal or greater to recovery_time
                    self.counter = 0
 #0 because reset for next cell to use counter because dead cell does not need
 #a counter anymore, which is only used for checking mortality and recovery
        if self.state != "R" and self.state != "S":
             for cell in adjacent_cells:
                 probability = random.random()
                 if probability <= virality and cell.state != "R":#can't infect dead cells
                     cell.infect()
             self.counter+=1 #add one to counter for each time time_step is called
                
class Map(object):
    def __init__(self):         
        self.height = 150         
        self.width = 150                   
        self.cells = {}

    def add_cell(self, cell):
        cell_tuple = (cell.x, cell.y)
        self.cells[cell_tuple] = cell

    def display(self): 
        coordinate_list = []
        image = []
        black = (0.0,0.0,0.0) 
        red = (1.0, 0.0, 0.0) 
        green = (0.0, 1.0, 0.0)
        gray = (0.5, 0.5, 0.5) 
        for r in range(0,150): #r represents rows
            coordinate_row = []
            for c in range(0,150): #c represents columns
                coordinate = (r,c)
                coordinate_row.append(coordinate) #each row has 150 coordinates (think of 150 columns)
            coordinate_list.append(coordinate_row)
   #loop executes 150 times for each row (150 of them) which contains 150 columns
        for row in coordinate_list: #coordinate_list contains 150 items, each item rep. a row
            row_list = [] #temp list to contain all the corresponding color tuples of the coordinates
            for coordinate in row:
                if coordinate in self.cells:
   #self.cells contains all of the green cell coordinates
   #all the coordinates not in self.cells are black
                    cell = self.cells[coordinate] #getting the cell instance
                    if cell.state == "S":
                        color = green
                    elif cell.state == "I":
                        color = red
                    elif cell.state == "R":
                        color = gray
                else:
                    color = black
                row_list.append(color)
            image.append(row_list)
        plt.imshow(image) #image can only be processed if it is a list of lists (list of rows containing a list of color tuples)

    def adjacent_cells(self, x,y):         
        adjacent = []
        for i in [-1,1]:#only need -1 and 1 because only looking for cells next to current cell
            if (x,y+i) in self.cells:#checking for adjacent cells above and below
                adjacent.append(self.cells[(x,y+i)])
            if(x+i,y) in self.cells: #checking for adjacent cells to the left and right
                adjacent.append(self.cells[(x+i,y)])
        return adjacent #returns a list of cell instances
    
    #i want to have a disease spread from one point
    def time_step(self):
        for cell in self.cells:
            cell_instance = self.cells[cell] #retrieving the cell instance
            cell = list(cell) #need to cast the list type because tuple types does not work
            adj_cells = self.adjacent_cells(x=cell[0],y=cell[1])
            cell_instance.process(adjacent_cells = adj_cells)
        self.display()

def read_map(filename):         
    m = Map()       
    f = open(filename, 'r')
    coordinates_temp = []
    list_of_coordinates = []
    counter = 0
    for line in f:
        coordinates_temp = line.split(",") #splitting the coordinates and putting them in a list
        coordinates = []
        for coordinate in coordinates_temp:
            coordinates.append(int(coordinate.strip())) #stripping the whitespace
        list_of_coordinates.append(tuple(coordinates)) #contains a list of coordiantes in tuple form (hashable type for dictionaries)
    for coordinate in list_of_coordinates:#creating an instance of each cell using the given set of coordinates from the text
        cell_instance = Cell(x = list_of_coordinates[counter][0], y = list_of_coordinates[counter][1])
        m.add_cell(cell = cell_instance)
        counter = counter + 1
    return m
