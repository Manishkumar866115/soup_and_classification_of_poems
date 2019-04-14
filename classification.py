# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 23:34:20 2019

@author: Manish
"""

import numpy as np 
import pandas as pd

import os
print(os.listdir("../input"))

file_path="../input/poems.csv"
with open(file_path, 'rb') as f:
  contents = f.read()

contents=contents.decode(encoding='utf-8',errors='ignore')

from io import StringIO

TESTDATA = StringIO(contents)

dataset = pd.read_csv(TESTDATA, sep=",",error_bad_lines=False)

#turning categorial values to numeric value
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
dataset["category"]=le.fit_transform(dataset["category"])

#peeking the data
print(dataset.head())
print(dataset.describe())

#cleaning the data by removing the stopwords , word tokenizing, using porter stemmer to 
#stem the words and putting them in our corpus
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
corpus=[]
ps=PorterStemmer()
stopwords=set(stopwords.words("english"))
for i in range(394):
    review=dataset.iloc[i][1]
    review = re.sub('[^a-zA-Z]', ' ', dataset.iloc[i][1] )
    review = re.sub('[?&#@$%!_.|,-:;"]', ' ', dataset.iloc[i][1] )    
    review=review.lower()
    words=word_tokenize(review)
    d=list()
    for w in words:
        if w not in stopwords:
            d.append(ps.stem(w))
    review=" ".join(d)
    corpus.append(review)

#peeking the corpus
print(corpus[5:10])

#creating a bag of words
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=2000)
X=cv.fit_transform(corpus).toarray()
y=dataset.iloc[:,3].values

#spliting the data into training set and test set
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,y,test_size=0.40,random_state=0,shuffle=True)

#classification using XGBoost classifier
from xgboost import XGBClassifier
classifier = XGBClassifier()
classifier.fit(X_train, Y_train)
Y_pred = classifier.predict(X_test)

#comparing the result using confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred)
print(cm)

'''
 resulting confusion matrix
 [[36  0  3  5]
 [ 1 39  1  0]
 [ 1  2 29  5]
 [ 3  3  2 28]]
 accuracy = 84%
'''