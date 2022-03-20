import os
os.chdir('D:/Projects/Football/Prediction_Code')

import pandas as pd
import numpy as np
import math
import Read_Load_Prediction as db
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.optimizers import SGD


f = db.get_data_db(6)
df = f.get_data()

df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
       'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
       'Trainer_ID']]   

df = df[df['Heimmannschaft_ID']==16]

x = df.iloc[:,[1,2,3,4,5,6,7,8,9,10,11]].values
y = df.iloc[:,0].values
y = y.reshape(-1, 1)
min_max_scaler = MinMaxScaler(feature_range = (0,1))
x = min_max_scaler.fit_transform(x)
y = min_max_scaler.fit_transform(y)

def split_to_percentage(data, percentage):
    return data[0:int(len(data)*percentage)],data[int(len(data)*percentage):]
    

x_train, x_test = split_to_percentage(x, 0.8)
y_train, y_test = split_to_percentage(y, 0.8)
x_train.shape
x_test.shape[1]
y_train.shape
model = tf.keras.Sequential()
model.add(LSTM(10))
model.add(Dense(1))
sgd = SGD(lr=0.1)
model.compile(loss="mean_squared_error", optimizer = sgd, metrics=[tf.keras.metrics.mse])
model.fit(x_train, y_train, epochs = 100, verbose = 1)




score,_ = model.evaluate(x_test, y_test)
rmse = math.sqrt(score)

prediction = model.predict(x_test)
prediction_training = model.predict(x_train)

predictions_on_training = min_max_scaler.inverse_transform(prediction_training)
shift = range(len(prediction_training)-1, len(y)-1)

plt.plot(y, color = "#CFCEC4", label = "Results")
plt.plot(prediction_training, color = "green", label = "Training")
plt.plot(shift,prediction, label = 'Test', color = "red")
plt.legend(loc = 'upper left')
plt.show()
