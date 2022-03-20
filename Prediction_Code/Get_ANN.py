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

spieltag = 27
saison = '2021/22'
vereins_id = 7
f1 = db.get_data_db(15)
df1 = f1.get_data()

f2 = db.get_data_db(16)
df2 = f2.get_data()

df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft_ID', 'Gegner_ID'])
df = df.sort_values(['Saison', 'Spieltag'])
variables = df[['Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz','Abwehrdifferenz', 'Gesamtdiffferenz', 'Angriffdifferenz',
    'Mittelfelddifferenz', 'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz', 'L1', 'L2', 'L3', 'L4', 'L5',
    'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5', 'B365H', 'B365D', 'B365A', 'HeimSystem', 'AuswärtsSystem', 'Home_Shot_Feature',
    'Home_Shot_On_Goal_Feature', 'Home_Fouls_Feature', 'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Away_Shot_Feature',
    'Away_Shot_On_Goal_Feature', 'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature']].values

results = df[['Spiel_Ausgang']].values

f1 = db.get_data_db(17)
df1_forecast = f1.get_data()
f2 = db.get_data_db(18)
df2_forecast = f2.get_data()
df_forecast = df1_forecast.merge(df2_forecast, on = ['Saison', 'Spieltag', 'Heimmannschaft_ID', 'Gegner_ID'])
df_forecast = df_forecast.sort_values(['Saison', 'Spieltag'])
df_forecast = df_forecast[df_forecast['Saison']=='2021/22']
df_forecast = df_forecast[df_forecast['Spieltag']==spieltag]
df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==vereins_id]

forecast = df_forecast[['Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz','Abwehrdifferenz', 'Gesamtdiffferenz', 'Angriffdifferenz',
    'Mittelfelddifferenz', 'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz', 'L1', 'L2', 'L3', 'L4', 'L5',
    'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5', 'B365H', 'B365D', 'B365A', 'HeimSystem', 'AuswärtsSystem', 'Home_Shot_Feature',
    'Home_Shot_On_Goal_Feature', 'Home_Fouls_Feature', 'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Away_Shot_Feature',
    'Away_Shot_On_Goal_Feature', 'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature']].values

sc = StandardScaler()
X = sc.fit_transform(variables)
X_forecast = sc.transform(forecast)

y_categorical = np_utils.to_categorical(results, num_classes=3)

ann = tf.keras.Sequential( 
[
 tf.keras.layers.Dense(units=32, activation='softmax', input_shape=(X.shape[1],)),
 tf.keras.layers.Dense(units=32, activation='softmax'),
 tf.keras.layers.Dense(units=32, activation='softmax'),
 tf.keras.layers.Dense(units=3, activation='softmax')
 ]
)    
#smaller learning rate, more stable resutls
opt = SGD(lr=0.5)
ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
ann.fit(X, y_categorical, batch_size = 16, epochs = 100)
y_pred = ann.predict(X_forecast)

print(1/y_pred[0][1])
print(1/y_pred[0][2])
print(1/y_pred[0][0])


def test_ann():
    f1 = db.get_data_db(15)
    df1 = f1.get_data()
    
    f2 = db.get_data_db(16)
    df2 = f2.get_data()
    
    df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft_ID', 'Gegner_ID'])
    df = df.sort_values(['Saison', 'Spieltag'])
    df_variable = df[['Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz','Abwehrdifferenz', 'Gesamtdiffferenz', 'Angriffdifferenz',
        'Mittelfelddifferenz', 'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz', 'L1', 'L2', 'L3', 'L4', 'L5',
        'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5', 'B365H', 'B365D', 'B365A', 'HeimSystem', 'AuswärtsSystem', 'Home_Shot_Feature',
        'Home_Shot_On_Goal_Feature', 'Home_Fouls_Feature', 'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Away_Shot_Feature',
        'Away_Shot_On_Goal_Feature', 'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature']].values
    
    df_results = df[['Spiel_Ausgang']]#.values
    
    X_train = df_variable.values[:-20]
    X_test = df_variable.values[-20:]
    y_train = df_results.values[:-20].ravel()
    y_test = df_results.values[-0:].ravel()
    
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
     
    y_train_categorical = np_utils.to_categorical(y_train, num_classes=3)
    
    ann = tf.keras.Sequential( 
    [
     tf.keras.layers.Dense(units=11, activation='softmax', input_shape=(X_train.shape[1],)),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=3, activation='softmax')
     ]
    )    
    opt = SGD(lr=0.5)
    ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
    ann.fit(X_train, y_train_categorical, batch_size = 1, epochs = 100)
    y_pred = ann.predict(X_test)    

    for i in range(len(y_pred)):
        home = y_pred[i][1]
        draw = y_pred[i][0]
        away = y_pred[i][2]
        y_train[i]
        
        print("Proba for home is:")
        print(home)
        print("")
        print("Proba for draw is:")
        print(draw)
        print("")
        print("Proba for away is:")
        print(away)
        print("")
        print("resulst is:")
        print(y_train[i])
        print("")

def get_best_ann(forecast, variables, results, home_team, away_team):
    
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
        
    print("Fair odds for home win") 
    print(1/np.mean(predictionHome))    
    print("Fair odds for draw") 
    print(1/np.mean(predictionDraw))
    print("Fair odds for away win") 
    print(1/np.mean(predictionAway))

  
def ann_for_tool(df_results, df_variable, home_odds, draw_odds, away_odds):
    
    X_train = df_variable.values[:-1]
    X_test = df_variable.values[-1:]
    y_train = df_results.values[:-1].ravel()
    y_test = df_results.values[-1:].ravel()
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    y_train_categorical = np_utils.to_categorical(y_train, num_classes=3)
    
    ann = tf.keras.Sequential( 
    [
     tf.keras.layers.Dense(units=11, activation='softmax', input_shape=(X_train.shape[1],)),
     tf.keras.layers.Dense(units=11, activation='softmax'),
     tf.keras.layers.Dense(units=3, activation='softmax')
     ]
    )    
    
    opt = SGD(lr=1)
    ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
    ann.fit(X_train, y_train_categorical, batch_size = 1, epochs = 100)
    y_pred = ann.predict(X_test)    
    
    home_difference = (1/y_pred[0][1]) - home_odds
    draw_difference = (1/y_pred[0][0]) - draw_odds
    away_difference = (1/y_pred[0][2]) - away_odds
    
    
    if home_difference > draw_difference and home_difference > away_difference:
        
        if y_test == 1:
            win = home_odds * 10
        else:
            win = -10

    if draw_difference > home_difference and draw_difference > away_difference:
        
        if y_test == 0:
            win = home_odds * 10
        else:
            win = -10
 
    if away_difference > draw_difference and away_difference > home_difference:
        
        if y_test == 1:
            win = home_odds * 10
        else:
            win = -10
    
    return win

