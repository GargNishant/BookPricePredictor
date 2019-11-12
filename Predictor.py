#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:47:58 2019

@author: nishant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def get_category_unique(column_str,dataset):
    """ 
    This function is used to return a list of unique values from given column string
    @param: A valid dataframe which contains required column, 
            Name of the column in string format
    @return: List of objects from the Dataframe for the given column name
    """
    col = dataset[column_str].unique()
    col_unique = []
    for data in col:
        col_unique.append(data)
    return col_unique


"""Dropping the Title Column as there should not be any relation between the Title and the 
price of te book"""
dataset = pd.read_excel("Data_Train.xlsx").iloc[:,1:]


""" Getting the uniques for each Feature"""
genre_unique = []
genre_unique = get_category_unique("Genre",dataset)
cat_unique = []
cat_unique = get_category_unique("BookCategory",dataset)

