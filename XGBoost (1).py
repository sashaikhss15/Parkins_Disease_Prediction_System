#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


#Reading the data set
symptoms=pd.read_csv(r"C:\Users\Aqueed\Desktop\revised-cleaned-data.csv")


# In[3]:


import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


# In[4]:


X=symptoms.drop(['status','name'],axis=1)
y=symptoms['status']


# In[5]:


#splitting dataset
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=123)
X_train = np.ascontiguousarray(X_train)
y_train = np.ascontiguousarray(y_train)
X_test = np.ascontiguousarray(X_test)
y_test = np.ascontiguousarray(y_test)


# In[6]:


#Traininf the model
from xgboost import XGBClassifier
model=XGBClassifier(use_label_encoder=False,eval_metric='mlogloss')
model.fit(X_train,y_train)


# In[7]:


import pickle


# In[8]:


filename = 'finalized_model.pkl'
pickle.dump(model, open(filename, 'wb'))


# In[9]:


model_path = '/home/coda/aq_project/disease-prediction-system'
classifier = pickle.load(open(model_path, 'rb'))
prediction = classifier.predict(np.array([[199.228,209.512,192.091,0.00241,1.00E-05,0.00134,0.00138,0.00402,0.01015,0.089,0.00504,0.00641,0.00762,0.01513,0.00167,30.94,0.432439,0.742055,-7.682587,0.173319,2.103106,0.068501]]))[0]
print(prediction)


# In[ ]:




