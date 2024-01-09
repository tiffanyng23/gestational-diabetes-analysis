#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:20:41 2024

@author: tiffanyng
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


#Prediction Models
#All variables other than mean systolic pressure

#variables significantly different between groups: 
#The mean diastolic blood pressure (p = 0.03), 
#central fat (p = 0.0004), 
#first fasting glucose (p = 0.003)
#age (p =0.03), 
#BMI (p = 0.003) 
#Type of delivery (p=0.04)

#Just central fat

data = pd.read_csv("gdm_vat_data_cleaned.csv")
data_copy = data

#drop mean systolic blood pressure
data_copy = data_copy.drop(["mean_systolic_bp", "number"], axis=1)


#APPLYING LOGISTIC REGRESSION MODELS
#The authors of the study where the dataset came from used logistic regression
#I will also apply logistic regression to three models with various variables.

#model 1: mean diastolic blood pressure, central fat, first fasting glucose, age, bmi, type of delivery
#model 2: central armellini fat, first fasting glucose, bmi, age
#model 3: central armellini fat, first fasting glucose, bmi


#Cross Validation
#cross validation allows for combinations of training-testing sets to be created without using a third vailidation set
#This allows for the model to be trained and tested several times which helps prevent overfitting

#Data transformation - scaling data
#Data transformations should be learned from a training set so standard scaler will be applied to the training data



#DATA TRANSFORMATION
#scaling data to standardize the features
  
def scaling_data(data, variable_list):
    """scaling data for variables of choice"""

    for var in variable_list:
        #convert to numpy array
        data_new = np.array(data[var])
        #reshape data
        data_new = data_new.reshape(-1,1)
        #fit and transform data
        scaled_data = StandardScaler().fit_transform(data_new)
            
        #update values in dataframe
        data[var]=scaled_data.flatten()
    
    return data

#remove variables in a nominal scale from being scaled
data_to_scale = data_copy.drop(["gestational_dm", "type_of_delivery", "ethnicity"], axis=1)
variables = data_to_scale.columns

#scale data
data_copy = scaling_data(data_copy,variables)



#LOGISTIC REGRESSION
log_reg = LogisticRegression(random_state=123)



#Model 1

model_1= data_copy[["central_armellini_fat", "mean_diastolic_bp", "first_fasting_glucose", "age", "bmi_pregestational", "type_of_delivery", "gestational_dm"]]
#x and y variables
model_1_x = model_1.iloc[:, :-1]
model_1_y = model_1.iloc[:, -1]

#cross validation
model_1_scores = cross_validate(log_reg, model_1_x, model_1_y, cv=7, 
                           scoring=["roc_auc", "average_precision"], return_train_score=True)

#comparing prediced and actual y values, creating confusion matrix 
y_predict_1 = cross_val_predict(log_reg, model_1_x, model_1_y, cv=7)
conf_matrix_1 = confusion_matrix(model_1_y,y_predict_1)



#MODEL 2
model_2= data_copy[["age", "central_armellini_fat", "first_fasting_glucose", "bmi_pregestational", "gestational_dm"]]
#x and y variables
model_2_x = model_2.iloc[:, :-1]
model_2_y =model_2.iloc[:, -1]

#cross validation
model_2_scores = cross_validate(log_reg, model_2_x, model_2_y, cv=7, 
                           scoring=["roc_auc", "average_precision"], return_train_score=True)


#comparing prediced and actual y values, creating confusion matrix 
y_predict_2 = cross_val_predict(log_reg, model_2_x, model_2_y, cv=7)
conf_matrix_2 = confusion_matrix(model_2_y,y_predict_2)


#Model 3
model_3=data_copy[["central_armellini_fat", "first_fasting_glucose", "bmi_pregestational", "gestational_dm"]]
#x and y variables, need to convert x variable to a dataframe
model_3_x = model_3.iloc[:, :-1]
model_3_y = model_3.iloc[:, -1]


#cross validation
model_3_scores = cross_validate(log_reg, model_3_x, model_3_y, cv=7, 
                           scoring=["roc_auc", "average_precision"], return_train_score=True)

#comparing prediced and actual y values, creating confusion matrix 
y_predict_3 = cross_val_predict(log_reg, model_3_x, model_3_y, cv=7)
conf_matrix_3 = confusion_matrix(model_3_y,y_predict_3)





#ASSESSING RESULTS
#comparing AUC between models
#model 1
average_auc_1 = np.average(model_1_scores["test_roc_auc"])

#model 2
average_auc_2 = np.average(model_2_scores["test_roc_auc"])

#model 3
average_auc_3 = np.average(model_3_scores["test_roc_auc"])


#comparing precision 
#ability to not have false positives
#TP/(TP+FP)
#model 1
average_prec_1 = np.average(model_1_scores["test_average_precision"])

#model 2
average_prec_2 = np.average(model_2_scores["test_average_precision"])

#model 3
average_prec_3 = np.average(model_3_scores["test_average_precision"])


#sensitivity: ability to identify GDM cases, true positive rate
#sensitivity = TP/(TP+FN)

#model 1
sensitivity_1 = conf_matrix_1[1,1]/(conf_matrix_1[1,1] + conf_matrix_1[1,0])

#model 2
sensitivity_2 = conf_matrix_2[1,1]/(conf_matrix_2[1,1] + conf_matrix_2[1,0])

#model 3
sensitivity_3 = conf_matrix_3[1,1]/(conf_matrix_3[1,1] + conf_matrix_3[1,0])


#specificity: ability to identify non-GDM cases, true negative rate
#spcificity = TN/(TN+FP)

#model 1
specificity_1 = conf_matrix_1[0,0]/(conf_matrix_1[0,0] + conf_matrix_1[0,1])

#model 2
specificity_2 = conf_matrix_2[0,0]/(conf_matrix_2[0,0] + conf_matrix_2[0,1])

#model 3
specificity_3 = conf_matrix_3[0,0]/(conf_matrix_3[0,0] + conf_matrix_3[0,1])


#Summary:
#Model 1 has the highest AUC at 0.83 and precision at 0.55.
#However all models have a lowe sensitivity at 0.18. This is likely due to a low sample size of GDM cases.


#Overall, I would say Model 1 is the best of the three since it has the highest AUC and precision.
#However, none of these Models have a strong ability to predict positive cases.

