#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Michaella Schaszberger
mls2290
Professor Bauer
ENGIE E1006
Homework 5
"""
import numpy as np 
from matplotlib import pyplot as plt

def euclidean_distance(a,b):     
    diff = a - b     
    return np.sqrt(np.dot(diff, diff))
    
def load_data(csv_filename):    
    f = open(csv_filename, 'r')
    for i in f:
        f.readline().strip()
    data = np.genfromtxt(csv_filename, delimiter = ';', skip_header = 1, usecols=range(0,11)) #header unnecessary, excluding 12th column
    return data
    """
    Returns a numpy ndarray in which each row repersents     
    a wine and each column represents a measurement. There should be 11     
    columns (the "quality" column cannot be used for classificaiton).     
    """     
   
def split_data(dataset, ratio=0.9):
    rows= len(dataset)
    training= ratio*float(rows) #determining number of rows for training
    train = dataset[0:int(training):1] #train set includes all data up until the value of training
    test = dataset[int(training)::] #includes value of training
    train_test_tuple = (train, test)
    return train_test_tuple

    """     
    Return a (train, test) tuple of numpy ndarrays.     
    The ratio parameter determines how much of the data should be used for     
    training. For example, 0.9 means that the training portion should contain     
    90% of the data. You do not have to randomize the rows. Make sure that     
    there is no overlap.     
    """
     
def compute_centroid(data):
    return sum(data[:]) / len(data)
    """     
    Returns a 1D array (a vector), representing the centroid of the data     
    set.     
    """
  
def experiment(ww_train, rw_train, ww_test, rw_test):
    white_wine_data = compute_centroid(data = ww_train)
    red_wine_data = compute_centroid(data = rw_train)
    ww_prediction_correct = 0
    white_wine_counter = 0
    rw_prediction_correct = 0
    red_wine_counter = 0
    for data_point in ww_test:
        white_wine_counter+=1
        rw_euclidean_dist = euclidean_distance(data_point, red_wine_data)
        ww_euclidean_dist = euclidean_distance(data_point, white_wine_data)
        #if the distance to the white wine data point is smaller, that means the data set is more like the white wine data points
        if ww_euclidean_dist <= rw_euclidean_dist:
            ww_prediction_correct+=1
    for data_point in rw_test:
        red_wine_counter+=1
        #distances determine whether data point is closer to the red wine or white wine data
        rw_euclidean_dist = euclidean_distance(data_point, red_wine_data)
        ww_euclidean_dist = euclidean_distance(data_point, white_wine_data)
        if rw_euclidean_dist <= ww_euclidean_dist:
            rw_prediction_correct+=1
    correct = ww_prediction_correct + rw_prediction_correct
    total = white_wine_counter + red_wine_counter
    accuracy = correct/total
    
    print("The total number of predictions is ", total)
    print("The total number of correct predictions is ", correct)
    print("The accuracy of this model is ", accuracy)
    
    return accuracy
    """     
    Train a model on the training data by creating a centroid for each class.     
    Then test the model on the test data. Prints the number of total     
    predictions and correct predictions. Returns the accuracy.     
    """
def learning_curve(ww_training, rw_training, ww_test, rw_test):    
    np.random.shuffle(ww_training)
    np.random.shuffle(rw_training)
    experiment_findings = []
    y_coordinates = []
    ww_length = len(ww_test)
    rw_length = len(rw_test)
    n = 0
    #n is the size of the smaller training set
    if ww_length < rw_length:
        n = ww_length
    if rw_length <= ww_length:
        n = rw_length
    for point in range(n):
        counter = point + 1 
        test_accuracy = experiment(ww_train = ww_training[0:counter], rw_train = rw_training[0:counter], ww_test= ww_test, rw_test = rw_test)
        tuple_answer = (counter, test_accuracy)
        experiment_findings.append(tuple_answer)
        y_coordinates.append(test_accuracy)
    plt.plot(range(1,n+1),y_coordinates)
    plt.ylabel("Accuracy")
    plt.xlabel("Size of the Training Set")
    plt.show()
    return experiment_findings
            
    """     
    Perform a series of experiments to compute and plot a learning curve.     
    """  
 
def cross_validation(ww_data, rw_data, k):
    #taking smaller sets of data, finding the accuracy of those smaller sets of data, summing them together, then finding
    #the average of those accuracies
    ww_partitions = int(len(ww_data)/k) #creating the k partitions
    counter = 0
    for count in range(ww_partitions):
        if count==0:
            rw_testing = rw_data[0:k]
            rw_training = rw_data[k:ww_partitions] #training is the rest of the set
            ww_testing = ww_data[0:k]
            ww_training = ww_data[k:ww_partitions]
        else:
            rw_training = rw_data[0:count*k]
            rw_testing = rw_data[k*count: k*(count+1)] #range of data points within a partition
            ww_training = ww_data[0:k*count]
            ww_testing = ww_data[k*count: k*(count+1)]
        if count < (ww_partitions - 1):
            training = rw_data[(count+1)*k:ww_partitions]
            rw_training = np.concatenate((rw_training, training), axis = 0)
            training = ww_data[(count+1)*k:ww_partitions]
            ww_training = np.concatenate((ww_training, training), axis = 0)
        accuracy= experiment(ww_train = ww_training, rw_train = rw_training,ww_test = ww_testing, rw_test = rw_testing)
        counter += accuracy
    average = counter/ww_partitions
    return average

    """     
    Perform k-fold crossvalidation on the data and print the accuracy for each     
    fold.     
    """

if __name__ == "__main__":         
    ww_data = load_data('whitewine.csv')     
    rw_data = load_data('redwine.csv')
        
    ww_train, ww_test = split_data(ww_data, 0.9)    
    rw_train, rw_test = split_data(rw_data, 0.9)

    experiment(ww_train, rw_train, ww_test, rw_test) 

    ww_train, ww_test = split_data(ww_data, 0.9)     
    rw_train, rw_test = split_data(rw_data, 0.9)     
    learning_curve(ww_train, rw_train, ww_test, rw_test)   
          
    k = 10     
    acc = cross_validation(ww_data, rw_data, k)     
    print("{}-fold cross-validation accuracy: {}".format(k,acc))
