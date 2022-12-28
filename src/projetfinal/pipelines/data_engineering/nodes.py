"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.3
"""
import os
import pandas as pd
import numpy as np
from pyexpat import model
import cv2
from sklearn.model_selection import train_test_split
from typing import Any, Tuple, Dict
import sys
from sklearn.decomposition import PCA
from sklearn.svm import SVC
import mlflow
import logging

np.set_printoptions(threshold=np.inf)
np.set_string_function(lambda x : repr(x), repr=False)
####Fonction pour compter le nombre total d'image###

def nombreTotalImage (base_path : str) -> int:
    total_images = 0
    folder = os.listdir(base_path)
    
    for n in range(len(folder)):
        patient_id = folder[n]
        for c in [0, 1]:
            patient_path = base_path + patient_id 
            class_path = patient_path + "/" + str(c) + "/"
            
            if (os.path.exists(class_path)) :
                subfiles = os.listdir(class_path)
                total_images += len(subfiles)

    return total_images

###################Création du dataset#######################    
    
def create_dataframe(base_path : str) -> pd.DataFrame:
    total_images = nombreTotalImage(base_path)
    data = pd.DataFrame(index=np.arange(0, total_images), columns=["patient_id", "path","feature", "target"])
    k = 0
    folder = os.listdir(base_path)
    for n in range(len(folder)):
        patient_id = folder[n]
        patient_path = base_path + patient_id 
        for c in [0,1]:
            class_path = patient_path + "/" + str(c) + "/"
            if (os.path.exists(class_path)) :
                subfiles = os.listdir(class_path)
                for m in range(len(subfiles)):
                    image_path = subfiles[m]
                    #data.iloc[k]["path"] = class_path + image_path
                    data.iloc[k]["feature"] = cv2.imread(class_path + image_path)
                    data.iloc[k]["target"] = c
                    data.iloc[k]["patient_id"] = patient_id
                    k += 1  
    return data 

#def update_culumn_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    
    

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

def support_vector_machine(x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame):
    #Model initialization
    x_train['values'] = x_train['values'].apply(np.array)
    x_test['values'] = x_test['values'].apply(np.array)
    y_train['values'] = y_train['values'].apply(np.array)
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