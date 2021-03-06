# -*- coding: utf-8 -*-
"""Predictive_maintenance.ipynb



Original file is located at
    https://colab.research.google.com/drive/1kAn-xUj0285NSQIpofDSDuH7pyu_1kvG
Author: Supriyo Roy Banerjee
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
#import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_curve, auc
import json

df=pd.read_csv('Data/predictive_maintenance.csv')

df.head(5)

df['Failure Type'].value_counts()

df['Target'].value_counts()

df.info()

df_numeric = df.loc[:,['Air temperature [K]','Process temperature [K]','Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']]
df_cat    = df.loc[:,['Type']]

df_cat.head(5)

df_cat.value_counts()

df.describe()


fig = plt.figure(figsize = (15,15))
ax  = fig.gca()
df_numeric.loc[:,['Air temperature [K]','Process temperature [K]','Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']].hist(ax = ax)
plt.savefig('machine_histogram.png')

"""#If the skewness is between -0.5 & 0.5, the data are nearly symmetrical.
#If the skewness is between -1 & -0.5 (negative skewed) or between 0.5 & 1(positive skewed), the data are slightly skewed.
# If the skewness is lower than -1 (negative skewed) or greater than 1 (positive skewed), the data are extremely skewed **bold text**
"""

df_numeric.skew()

"""# A pie chart below shows the distribution of the Failure Types"""

#!pip install -U kaleido

# Observe distrubution of failures
df.groupby(['Type']).sum().plot(kind='pie', y='Target',autopct='%1.0f%%')
plt.savefig('Machine_type.png')



"""Data Preprocessing 1: Encoding Categorical Features"""



le = LabelEncoder()
df['Type']         = le.fit_transform(df.loc[:,["Type"]].values)
df['Failure Type'] = le.fit_transform(df.loc[:,["Failure Type"]].values)

"""Data Preprocessing 2: Drop Unwanted Features"""

df = df.drop(["UDI","Product ID"],axis = 1)
df.head(2)


"""Data Preprocessing 3: Split Training and Testing"""

X  = df.iloc[:, :-2].values
y  = df.loc[:,['Target']].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#scaling data
scaler       = StandardScaler()
X_train_sc   = scaler.fit_transform(X_train)                # Fit and transform the training set 
X_test_sc    = scaler.transform(X_test)

#Modeling

xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)
print("Multi-Output Training Accuracy: ", xgb_clf.score(X_train, y_train)*100, "%")

# Test the Model 
y_pred_xgb   = xgb_clf.predict(X_test)



# Performance Metrics
print("Test Accuracy (Target)       : ",accuracy_score(y_test, y_pred_xgb)*100,"%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_xgb)
cm

plot_confusion_matrix(xgb_clf, X_test, y_test)  
plt.savefig('Confusion_matrix.png')

test_fpr, test_tpr, te_thresholds = roc_curve(y_test, y_pred_xgb)
print(test_fpr)
print(test_tpr)

accuracy=accuracy_score(y_test, y_pred_xgb)*100
print(accuracy)

data = {'accuracy':accuracy,'fpr':test_fpr.tolist(),'tpr':test_tpr.tolist()}


with open('Output/Accuracy.json', 'w') as f:
	json.dump(data,f, sort_keys=True, indent=4, separators=(',', ': '))
