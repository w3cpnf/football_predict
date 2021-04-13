import os
os.chdir('D:/Projects/Football/Prediction_Code')


from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

import Read_Load_Prediction as db



def log_reg_miner(vereins_id, threshold_1, threshold_2, threshold_3):
    
    all_scores = []
    factors = []
    predictions = []    
    
    f = db.get_data_db(6)
    df = f.get_data()
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5']] 
    
    df_set = df[df['Heimmannschaft_ID']==vereins_id]
    
    l1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    length = len(l1)  
    
    for i in range(length):
        for t in range(length):
            variables = l1[i:t+1]
            
            if len(variables)==0:
                pass
            else:        
                print(variables)
                X_train = df_set.iloc[:,variables].values[:-10]
                X_test = df_set.iloc[:,variables].values[-10:]
                y_train = df_set.iloc[:, 0].values[:-10]
                y_test = df_set.iloc[:, 0].values[-10:] 
                    
                logreg = LogisticRegression(solver = 'newton-cg')
                logreg.fit(X_train, y_train)
                
                y_pred = logreg.predict(X_test)
                score = logreg.score(X_test, y_test)
                         
                all_scores.append(score)
                factors.append(variables)
                predictions.append(y_pred)
                print(score)
            
    df_1 = pd.DataFrame(
    {'Score': all_scores,
     'Factors': factors,
     'Predictions': predictions
    })
    df_1 = df_1[df_1['Score']>threshold_1]
    
    
    all_scores_1 = []
    factors_1 = []
    predictions_1 = []    
     
    for i in range(len(df_1)):
        variables = df_1['Factors'].iloc[i]
        print(variables)
        X_train = df_set.iloc[:,variables].values[:-5]
        X_test = df_set.iloc[:,variables].values[-5:]
        y_train = df_set.iloc[:, 0].values[:-5]
        y_test = df_set.iloc[:, 0].values[-5:] 
            
        logreg = LogisticRegression(solver = 'newton-cg')
        logreg.fit(X_train, y_train)
        
        y_pred = logreg.predict(X_test)
        score = logreg.score(X_test, y_test)
                 
        all_scores_1.append(score)
        factors_1.append(variables)
        predictions_1.append(y_pred)
        print(score)
        
    df_2 = pd.DataFrame(
    {'Score': all_scores_1,
     'Factors': factors_1,
     'Predictions': predictions_1
    })
    df_2 = df_2[df_2['Score']>threshold_2]   
    
    all_scores_2 = []
    factors_2 = []
    predictions_2 = []    
     
    for i in range(len(df_2)):
        variables = df_2['Factors'].iloc[i]
        print(variables)
        X_train = df_set.iloc[:,variables].values[:-20]
        X_test = df_set.iloc[:,variables].values[-20:]
        y_train = df_set.iloc[:, 0].values[:-20]
        y_test = df_set.iloc[:, 0].values[-20:] 
            
        logreg = LogisticRegression(solver = 'newton-cg')
        logreg.fit(X_train, y_train)
        
        y_pred = logreg.predict(X_test)
        score = logreg.score(X_test, y_test)
                 
        all_scores_2.append(score)
        factors_2.append(variables)
        predictions_2.append(y_pred)
        print(score)
        
    df_3 = pd.DataFrame(
    {'Score': all_scores_2,
     'Factors': factors_2,
     'Predictions': predictions_2
    })
    df_3 = df_3[df_3['Score']>threshold_3] 

    return df_3

#df_miner = log_reg_miner(17, 0.6, 0.6, 0.6)




def log_reg(vereins_ID, saison, spieltag, variables):
    
    f = db.get_data_db(6)
    df = f.get_data()
    
    f_1 = db.get_data_db(7)
    df_forecast = f_1.get_data()
    df_forecast = df_forecast[df_forecast['Saison']==saison]
    df_forecast = df_forecast[df_forecast['Spieltag']==spieltag]
    df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==vereins_ID]
    home_team = df_forecast['Heimmannschaft'].iloc[0]
    away_team = df_forecast['Gegner'].iloc[0]
    
    variables = variables.replace('[','')
    variables = variables.replace(']','')
    variables = variables.split(",")
    variables = [ int(x) for x in variables]    
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5']] 
    df_forecast = df_forecast[['Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 'L4_Forecast', 'L5_Forecast']]   
    
    #get one club
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
    
    #choose variables to predict
    x = df_set.iloc[:,variables].values
    y = df_set.iloc[:, 0].values

    classifier = LogisticRegression(solver = 'newton-cg')
    classifier.fit(x, y)
    
    x_forecast = df_forecast.iloc[:,np.subtract(variables, 1)].values
      
    y_pred = classifier.predict(x_forecast)
    y_proba = classifier.predict_proba(x_forecast)
    print(y_pred)
    print(y_proba)
    
    if y_pred[0] == 1:
        print(" ")
        print("Home team "+str(home_team) + " is expected to win against " + str(away_team))
    if y_pred[0] == 0:
        print(" ")
        print("Home team"+str(home_team) + "is expected to play draw against " + str(away_team))
    if y_pred[0] == -1:
        print(" ")
        print("Home team"+str(home_team) + "is expected to lose against " + str(away_team))
        
    print(" ")
    print("Fair odds for home win is : ")
    print(" ")
    print(1/y_proba[0][2])

    print(" ")
    print("Fair odds for draw is : ")
    print(" ")
    print(1/y_proba[0][1])
    print(" ")
    print("Fair odds for home lost is : ")
    print(" ")
    print(1/y_proba[0][0])
    
    return y_proba


#log_reg(17, '2020/21', 28, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])