import pickle
import pandas as pd 
import numpy as np 
from decision_tree import DecisionTree
from random_forest import RandomForest
from sklearn.model_selection import train_test_split

#loading  processed dataset
df = pd.read_csv("model/fprocessed_data.csv")
X=df.drop('booking_status',axis=1)
y=df['booking_status']

#changing dataframes to numpy array
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test =  y_test.to_numpy()

#training model
clf = RandomForest(n_features = X.columns)
clf.train_model(X_train, y_train)

#pickling the model
pickle.dump(clf,open("ml_model","wb"))
