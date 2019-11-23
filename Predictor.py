"""
Created on Tue Nov 12 21:47:58 2019

@author: nishant
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""Dropping the Title Column as there should not be any relation between the Title and the 
price of te book"""
dataset_train = pd.read_excel("Data_Train.xlsx").iloc[:,1:]
dataset_test = pd.read_excel("Data_Test.xlsx").iloc[:,1:]


""" Cleaning the Reviews Column. This can be done by only taking the 
1st word. The 1st Word contains the number like 4.0, 4.9. Thus making it
suitable to change to numbers"""
def convert_review(dataset):
    review_list = list(dataset["Reviews"])
    review = []
    for item in review_list:
        review.append(float(item.split()[0]))
    dataset["Reviews"] = review
    
convert_review(dataset_train)
convert_review(dataset_test)


""" Rating Column"""
def conver_rating(dataset):
    rating_list = list(dataset["Ratings"])
    rating = []
    for item in rating_list:
        rating.append(float((item.split()[0]).replace(",","")))
    dataset["Ratings"] = rating

conver_rating(dataset_train)
conver_rating(dataset_test)

dataset_train.describe()


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
#max_authors = get_max_authors()


"""def cleanup_authors(dataset,auth_index):
    authors_list = list(dataset["Author"])
    all_authors = []
    dataset["Author"] = [i.split(",") for i in authors_list]
    
    for index,row in dataset.iterrows():
        authors = row["Author"]
        len_auth = len(authors)
        for i in range(len_auth):
            dataset.iloc[index,auth_index+i] = authors[i]
            all_authors.append(authors[i].strip().lower())
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
cleanup_authors(dataset_test,7)"""


#There are total of 7797 books combined from Train and Test Data
#There are only 4710 Unique Authors present.
#1233 Authors have written atleast 2 or more books
#3477 Authors have written only 1 Book
'''df = pd.DataFrame(all_authors,columns = ['Author'])
duplicateRowsDF = df[df.duplicated(['Author'])]
authors_book_count = pd.DataFrame(columns=["Author", "Count"])
authors_book_count["Author"] = df.Author.unique()
authors_book_count["Count"] = df.Author.value_counts(sort=True).tolist()

dataset_train.value_counts()

dataset_train.describe()

#Price does not matter a lot on Reviews. High reviews can have low price as well as high price 
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter3D( dataset_train["Ratings"],dataset_train["Reviews"], dataset_train["Price"], c=dataset_train["Price"])
ax.set_xlabel("People")
ax.set_ylabel("Ratings")
ax.set_zlabel("Price")
plt.show()'''


""" Cleaning the Edition Columns by dividing it into 2 more Columns indicating Years and Months"""
def cleanup_edition(dataset):
    list_ = list(dataset_train["Edition"])
    month = ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'Oct', 'Nov', 'Dec']
    edition_list = []
    years = []
    months = []
    for items in list_:
        item_list = items.split(",– ")
        edition_list.append(item_list[0].split(",")[-1])
        date = item_list[1].split()
        #As the mean of Years is 2011, thus we are filling the missing details with mean, making model stable
        try:
            years.append(int(date[-1]))
        except:
            years.append(2011)

        months.append(month.index(date[-2]) if len(date) >=2 and date[-2] in month else 5)
        
    dataset["Binding"] = edition_list
    dataset["Years"] = years
    dataset["Months"] = months

cleanup_edition(dataset_train)

""" THere is no relation between Months and Price. Neither Months as Reviews. It seems worthless"""
""" There is no found relation between years and price. New Books are also low priced as new books"""
""" Synopsis is worthless too"""
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter3D(dataset_train["Years"],dataset_train["Reviews"],dataset_train["Price"], c = dataset_train["Price"])
ax.set_xlabel("Years")
ax.set_ylabel("Review")
ax.set_zlabel("Price")
plt.show()

def cleanup_synopsis(dataset):
    syn_count = []
    list_ = list(dataset["Synopsis"])
    for items in list_:
        syn_count.append( len(set(items.split())))    
    dataset["Synop_Count"] = syn_count

cleanup_synopsis(dataset_train)