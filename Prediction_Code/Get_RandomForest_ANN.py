import os
os.chdir('D:/Projects/Football/Prediction_Code')
import numpy as np
import pandas as pd
import tensorflow as tf
import Read_Load_Prediction as db
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import  accuracy_score
from keras.utils import np_utils
import Get_RandomForest_Prediction as rp
from tensorflow.keras.optimizers import SGD
from sklearn.ensemble import RandomForestClassifier

def getRandomForestAnn(forecast, variables, results, home_team, away_team):
    
    x = variables
    y = results.ravel()

    classifier = RandomForestClassifier(n_estimators = 2000, criterion = 'gini', random_state = 0)
    classifier.fit(x, y)
    
    x_forecast = forecast
    
    y_proba = classifier.predict_proba(x_forecast) 
    
    
    sc = StandardScaler()
    X = sc.fit_transform(variables)
    X_forecast = sc.transform(forecast)
    
    y_categorical = np_utils.to_categorical(results, num_classes=3)
    
    predictionHome = []
    predictionAway = []
    predictionDraw = []
    
    for i in range(50):
        ann = tf.keras.Sequential( 
            [
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=25, activation='softmax', input_shape=(X.shape[1],)),
             tf.keras.layers.Dense(units=3, activation='softmax')
        ]
            )
        opt = SGD(lr=1)
        ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
        ann.fit(X, y_categorical, batch_size = 1, epochs = 100)
        y_pred = ann.predict(X_forecast)
        predictionHome.append(y_pred[0][1])
        predictionAway.append(y_pred[0][2])
        predictionDraw.append(y_pred[0][0])
        
    print("Home Team : " + home_team + " against " + away_team)  
    print("Fair odds for home win") 
    proba = (np.mean(predictionHome)+y_proba[0][2])/2
    print(1/proba)
    print("Fair odds for draw") 
    print(1/((np.mean(predictionDraw)+y_proba[0][1])/2))
    print("Fair odds for away win") 
    print(1/((np.mean(predictionAway)+y_proba[0][0])/2))