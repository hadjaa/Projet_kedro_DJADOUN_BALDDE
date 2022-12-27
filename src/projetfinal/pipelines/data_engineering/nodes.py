"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.3
"""
import os
import pandas as pd
import numpy as np
from PIL import Image
import cv2
from sklearn.model_selection import train_test_split
from typing import Any, Tuple, Dict
import sys

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

def split_train_test_data(data: pd.DataFrame, test_size : float) -> Tuple:
    x = []
    y = []
    np.set_printoptions(threshold=sys.maxsize)
    for i, row in data.iterrows():
        x.append(row['feature'])
        y.append(row['target'])
    x = np.array(x)
        #x = np.append(x)
    y = np.array(y)
        #x = np.append(y)
    pd.Series(y).value_counts()
    x_updated = x.reshape(len(x), -1)
    x_train, x_test, y_train, y_test = train_test_split(x_updated, y, test_size=test_size, shuffle=True)

    return  pd.DataFrame(data=x_train, columns=['values']),  pd.DataFrame(data=x_test, columns=['values']),  pd.DataFrame(data=y_train, columns=['values']),  pd.DataFrame(data=y_test, columns=['values'])