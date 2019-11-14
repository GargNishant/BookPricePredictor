#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:47:58 2019

@author: nishant
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Dropping the Title Column as there should not be any relation between the Title and the 
price of te book"""
dataset_train = pd.read_excel("Data_Train.xlsx").iloc[:,1:]
dataset_test = pd.read_excel("Data_Test.xlsx").iloc[:,1:]


""" Cleaning the Reviews Column. This can be done by only taking the 
1st word. The 1st Word contains the number like 4.0, 4.9. Thus making it
suitable to change to numbers"""
def convert_ratings(dataset):
    ratings_list = list(dataset["Reviews"])
    rating = []
    for item in ratings_list:
        rating.append(float(item.split()[0]))
    dataset["Reviews"] = rating
    
convert_ratings(dataset_train)
convert_ratings(dataset_test)


def get_max_authors():
    """ Returns the maximum number of Authors worked on a Single Book Combining Train, Test""" 
    # Making a List which will contain all the authors for each book. Combining Test and Train
    authors_all = list(dataset_train["Author"])
    author_test = list(dataset_test["Author"])
    authors_all.extend(author_test)
    
    # A book can be written by multiple Authors. Thus we are converting the Authors for each book from String into list
    #authorslis will be a nested List. A list containing 'List of Authors for each book' for all books
    authorslis = []
    for i in authors_all:
        authorslis.append(i.split(","))
    #max_authors will denote the maximum number of Authors worked on a single book from all records    
    max_authors = 1
    for item in authorslis:
        if len(item) > max_authors:
            max_authors = len(item)
    return max_authors


""" Cleaning the Authors column. Multiple Authors may work on Single Book.
First we would find the maximum number of Authors that can work on Single book
combining Train and Test. The we will add Columns. After adding the columns
we would fill them by splitting from original Authors Column """

#Finding the maximum number of Authors worked on 1 book
max_authors = get_max_authors()

def cleanup_authors(dataset,auth_index):
    authors_list = list(dataset["Author"])
    
    dataset["Author"] = [i.split(",") for i in authors_list]
    
    for index,row in dataset.iterrows():
        authors = row["Author"]
        len_auth = len(authors)
        
        for i in range(len_auth):
            dataset.iloc[index,auth_index+i] = authors[i]
    dataset.drop(["Author"],axis = 1, inplace = True)


dataset_train["Author1"] = None
dataset_train["Author2"] = None
dataset_train["Author3"] = None
dataset_train["Author4"] = None
dataset_train["Author5"] = None
dataset_train["Author6"] = None
dataset_train["Author7"] = None
dataset_test["Author1"] = None
dataset_test["Author2"] = None
dataset_test["Author3"] = None
dataset_test["Author4"] = None
dataset_test["Author5"] = None
dataset_test["Author6"] = None
dataset_test["Author7"] = None

cleanup_authors(dataset_train,8)
cleanup_authors(dataset_test,7)