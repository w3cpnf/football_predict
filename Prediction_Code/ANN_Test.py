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

from tensorflow.keras.optimizers import SGD


f = db.get_data_db(3)
df = f.get_data()
df = df[df['Heimmannschaft_ID']==16]


X = df.iloc[:, [5,7,8,9,10,11,12,13,14,16,17]].values
y = df.iloc[:, 6].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

y_train_categorical = np_utils.to_categorical(y_train, num_classes=3)
y_test_categorical = np_utils.to_categorical(y_test, num_classes=3)
ann = tf.keras.Sequential( 
    [
     tf.keras.layers.Dense(units=11, activation='softmax',input_shape=(X_train.shape[1],)),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=3, activation='softmax')
]
    )
opt = SGD(lr=1)
ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
ann.fit(X_train, y_train_categorical, batch_size = 32, epochs = 100)
y_pred = ann.predict(X_test)
#ann.predict()


results = list()
win_p= list()
draw_p= list()
lost_p= list()

for i in range(len(y_pred)):
    
    win_p.append(y_pred[i][1])
    draw_p.append(y_pred[i][0])
    lost_p.append(y_pred[i][2])
    
    if  y_pred[i][0]> y_pred[i][1] > y_pred[i][2] or y_pred[i][0]> y_pred[i][2] > y_pred[i][1]:
        y_pred[i][0] = 1
        y_pred[i][1] = 0
        y_pred[i][2] = 0
        results.append(0)
        
    if  y_pred[i][1]> y_pred[i][0] > y_pred[i][2] or y_pred[i][1]> y_pred[i][2] > y_pred[i][0]:
        y_pred[i][1] = 1
        y_pred[i][0] = 0
        y_pred[i][2] = 0
        results.append(1)
        
    if  y_pred[i][2]> y_pred[i][1] > y_pred[i][0] or y_pred[i][2]> y_pred[i][0] > y_pred[i][1]:
        y_pred[i][2] = 1
        y_pred[i][1] = 0
        y_pred[i][0] = 0
        results.append(-1)            
            
          
print(accuracy_score(y_test_categorical, y_pred))

f = db.get_data_db(3)
df = f.get_data()
df = df[df['Heimmannschaft_ID']==7]

f_forecast = db.get_data_db(2)
df_forecast = f_forecast.get_data()
df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==3]
X_forecast = df_forecast.iloc[:, [4,6,7,8,9,10,11,12,13,14,15]].values

X = df.iloc[:, [5,7,8,9,10,11,12,13,14,16,17]].values
y = df.iloc[:, 6].values


sc = StandardScaler()
X = sc.fit_transform(X)
X_forecast = sc.transform(X_forecast)

y_categorical = np_utils.to_categorical(y, num_classes=3)


ann = tf.keras.Sequential( 
    [
     tf.keras.layers.Dense(units=11, activation='softmax',input_shape=(X.shape[1],)),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=3, activation='softmax')
]
    )
opt = SGD(lr=1)
ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
ann.fit(X, y_categorical, batch_size = 32, epochs = 100)
y_pred = ann.predict(X_forecast)



print("Fair odds for draw") 
print(1/y_pred[0][0])
print("Fair odds for how win") 
print(1/y_pred[0][1])
print("Fair odds for away win") 
print(1/y_pred[0][2])