import pickle
import pandas as pd 
import numpy as np 
from decision_tree import DecisionTree
from random_forest import RandomForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score,roc_auc_score, classification_report,confusion_matrix

#loading  processed dataset
df = pd.read_csv("photels.csv")
X=df.drop('booking_status',axis=1)
y=df['booking_status']

#changing dataframes to numpy array
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test =  y_test.to_numpy()

#training model
clf = RandomForest(n_features = X.columns)
clf.fit(X_train, y_train)

#pickling the model
pickle.dump(clf,open("ml_model","wb"))

predictions = clf.predict(X_test, X.columns)

y_train_pred = clf.predict(X_train,X.columns)

print("Imbalance Accuracy: ",accuracy_score(y_test,predictions))
print("Balanced Accuracy: ",balanced_accuracy_score(y_test,predictions))
print("AUC Score: ",roc_auc_score(y_test,predictions))
print("Classification Report: ")
print("\n",classification_report(y_test, predictions))

print("Imbalance Accuracy: ",accuracy_score(y_train, y_train_pred))
print("Balanced Accuracy: ",balanced_accuracy_score(y_train, y_train_pred))
print("AUC Score: ",roc_auc_score(y_train, y_train_pred))
print("Classification Report: ")
print("\n",classification_report(y_train, y_train_pred))
