"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.3
"""
import os
import pandas as pd
import numpy as np
from PIL import Image
import cv2

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

###########Fonction pour verifier la resolution des images################

# def resolutionImg (data : pd.DataFrame):
    
#     for path in data['path'] :
#             im = Image.open(path)
#             width, height = im.size

#     return width, height