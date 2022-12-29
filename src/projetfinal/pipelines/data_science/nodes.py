"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""
#import os
import pandas as pd
import numpy as np
#from pyexpat import model
import cv2
from sklearn.model_selection import train_test_split
from typing import Any, Tuple, Dict
#import sys
#from sklearn.decomposition import PCA
from sklearn.svm import SVC
import mlflow
import logging


###################Split data#######################  
def split_train_test_data(data: pd.DataFrame, test_size : float) -> Tuple:
    
    x = []
    y = []

    for i, row in data.iterrows():
        x.append(row['feature'])
        y.append(row['target'])
    x = np.array(x)
        #x = np.append(x)
    y = np.array(y)
        #x = np.append(y)
    pd.Series(y).value_counts()
    x_updated = x.reshape(len(x), -1)
    #split data
    x_train, x_test, y_train, y_test = train_test_split(x_updated, y, test_size=test_size, shuffle=True)
    return  pd.DataFrame(data=x_train, columns=['values']),  pd.DataFrame(data=x_test, columns=['values']),  pd.DataFrame(data=y_train, columns=['values']),  pd.DataFrame(data=y_test, columns=['values'])

###################Train model SVM#######################  
def normalize_array(df: pd.DataFrame):
    for i, row in df.iterrows():
        df.iloc[i]["values"] = np.array(np.matrix(row.values[0].replace("array(","").replace(")","").replace(", dtype=uint8","")).reshape(-1, 3).A)
    return df
    

def support_vector_machine(x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame):
    #Model initialization
    # x_train['values'] = x_train['values'].apply(np.array)
    # x_test['values'] = x_test['values'].apply(np.array)
    y_train['values'] = y_train['values'].apply(np.array)
    x_train = normalize_array(x_train)
    x_test = normalize_array(x_test)
    print("== The type is", x_train.dtypes, x_test.dtypes, y_train.dtypes)
    model =  SVC(C=0.1)
    #Save the model with mlflow
    mlflow.sklearn.log_model(model, "model")
    ##train model
    model.fit(x_train, y_train)
    #Prediction des target avec la partie du test
    y_pred = model.predict(x_test)
   #Creation of the dataframe prediction
    pred = pd.DataFrame(y_pred, columns=['values'])


    return pred