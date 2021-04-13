import os
os.chdir('D:/Projects/Football/Prediction_Code')

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import Read_Load_Prediction as db


def random_forest_miner(vereins_ID, threshold_1, threshold_2, threshold_3):
    
    all_scores_1 = []
    factors_1 = []
    estimators_1 = []
    predict_1 = []
    
    f = db.get_data_db(6)
    df = f.get_data()
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5']]    
    
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
    
    l1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    length_factors = len(l1)  

    for i in range(length_factors):
        for t in range(length_factors):
            variables = l1[i:t+1]
            
            if len(variables)==0:
                pass
            else:
                n_estimators = [10, 20, 40, 50, 100, 200, 500, 1000]
                
                for e in n_estimators:
                    
                    print(variables)
                    X_train = df_set.iloc[:,variables].values[:-10]
                    X_test = df_set.iloc[:,variables].values[-10:]
                    y_train = df_set.iloc[:, 0].values[:-10]
                    y_test = df_set.iloc[:, 0].values[-10:]
         
                    classifier = RandomForestClassifier(n_estimators = e, criterion='gini', random_state = 0)
                    classifier.fit(X_train, y_train)
                    score = classifier.score(X_test, y_test)
                    y_predict = classifier.predict(X_test)
                    
                    all_scores_1.append(score)
                    factors_1.append(variables)
                    estimators_1.append(e)
                    predict_1.append(y_predict)
                    print(score)
                
    df = pd.DataFrame(
    {'Score': all_scores_1,
     'Factors': factors_1,
     'N_Estimators': estimators_1,
     'Prediction': predict_1
    })
    df_1 = df[df['Score']>threshold_1]
    
    all_scores_2 = []
    factors_2 = []
    estimators_2 = []
    predict_2 = []
    
    for i in range(len(df_1)):
        n = df_1['N_Estimators'].iloc[i]
        variables = df_1['Factors'].iloc[i]
        print(variables)
        print(n)
        X_train = df_set.iloc[:,variables].values[:-5]
        X_test = df_set.iloc[:,variables].values[-5:]
        y_train = df_set.iloc[:, 0].values[:-5]
        y_test = df_set.iloc[:, 0].values[-5:]
          
        classifier = RandomForestClassifier(n_estimators = n, criterion='gini', random_state = 0)
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        y_predict = classifier.predict(X_test)
        
        all_scores_2.append(score)
        factors_2.append(variables)
        estimators_2.append(e)
        predict_2.append(y_predict)
        print(score)
                    
    df_2 = pd.DataFrame(
    {'Score': all_scores_2,
     'Factors': factors_2,
     'N_Estimators': estimators_2,
     'Prediction': predict_2
    })
    df_3 = df_2[df_2['Score']>threshold_2]
    
    all_scores_3 = []
    factors_3 = []
    estimators_3 = []
    predict_3 = []
    
    for i in range(len(df_3)):
        n = df_3['N_Estimators'].iloc[i]
        variables = df_3['Factors'].iloc[i]
        print(variables)
        print(n)
        X_train = df_set.iloc[:,variables].values[:-20]
        X_test = df_set.iloc[:,variables].values[-20:]
        y_train = df_set.iloc[:, 0].values[:-20]
        y_test = df_set.iloc[:, 0].values[-20:]
              
        classifier = RandomForestClassifier(n_estimators = n, criterion='gini', random_state = 0)
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        y_predict = classifier.predict(X_test)
        
        all_scores_3.append(score)
        factors_3.append(variables)
        estimators_3.append(e)
        predict_3.append(y_predict)
        print(score)
                
    df_4 = pd.DataFrame(
    {'Score': all_scores_3,
     'Factors': factors_3,
     'N_Estimators': estimators_3,
     'Prediction': predict_3
    })
    df_4 = df_4[df_4['Score']>threshold_3]

    
    return df_4



#df_miner = random_forest_miner(10, 0.5, 0.5, 0.5)
#df_miner['Factors']
#df_miner.to_csv('D:/Projects/Football/Code_ML/Data/results_randomforest.csv')

def random_forest(vereins_ID, saison, spieltag, variables, n):
    
    variables = variables.replace('[','')
    variables = variables.replace(']','')
    variables = variables.split(",")
    variables = [ int(x) for x in variables]
    
    f = db.get_data_db(6)
    df = f.get_data()
    
    f_1 = db.get_data_db(7)
    df_forecast = f_1.get_data()
    df_forecast = df_forecast[df_forecast['Saison']==saison]
    df_forecast = df_forecast[df_forecast['Spieltag']==spieltag]
    df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==vereins_ID]
    home_team = df_forecast['Heimmannschaft'].iloc[0]
    away_team = df_forecast['Gegner'].iloc[0]
    

    variables_forecast = np.subtract(variables,1)
    print(variables_forecast)
    variables_used = variables


                
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5']]
    df_forecast = df_forecast[['Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 'L4_Forecast', 'L5_Forecast']]   
    
    #get one club
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
    
    #choose variables to predict
    x = df_set.iloc[:,variables_used].values
    y = df_set.iloc[:, 0].values

    #classifier
    classifier = RandomForestClassifier(n_estimators = n, criterion = 'gini', random_state = 0)
    classifier.fit(x, y)
    
    x_forecast = df_forecast.iloc[:,variables_forecast].values   
    print(x_forecast)
    
    y_pred = classifier.predict(x_forecast)
    y_proba = classifier.predict_proba(x_forecast)
    print(y_pred)
    print(y_proba)
    
    if y_pred[0] == 1:
        print(" ")
        print("Home team "+str(home_team) + " is expected to win against " + str(away_team))
    if y_pred[0] == 0:
        print(" ")
        print("Home team "+str(home_team) + "is expected to play draw against " + str(away_team))
    if y_pred[0] == -1:
        print(" ")
        print("Home team "+str(home_team) + "is expected to lose against " + str(away_team))
        
    print(" ")
    print(y_proba[0][2])
    print(" ")
    print("Fair odds for home win is : ")
    print(" ")    
    print(1/y_proba[0][2])

    print(" ")
    print(y_proba[0][1])
    print("Fair odds for draw is : ")   
    print(" ")
    print(1/y_proba[0][1])
    print(" ")
    print(y_proba[0][0])
    print("Fair odds for home lost is : ")
    print(" ")
    print(1/y_proba[0][0])
    
    return y_proba

#outcome = random_forest(10, '2020/21', 28,[1,2,3,4,5,6,7,8,9,10,11,12, 13, 14,15,16], 1000)



def random_forest_test(vereins_ID, saison, spieltag, variables, n):
    
    all_scores_1 = []
    predict_1 = []
    
    f = db.get_data_db(6)
    df = f.get_data()
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5']]    
    
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
    
                  
    print(variables)
    X_train = df_set.iloc[:,variables].values[:-3]
    X_test = df_set.iloc[:,variables].values[-3:]
    y_train = df_set.iloc[:, 0].values[:-3]
    y_test = df_set.iloc[:, 0].values[-3:]
 
    classifier = RandomForestClassifier(n_estimators = 1000, criterion='gini', random_state = 0)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    y_predict = classifier.predict(X_test)
    
    all_scores_1.append(score)
    predict_1.append(y_predict)
    print(score)
#
#random_forest_test(17, '2020/21', 28,[1,2,3,4,5,6,7,8,9,10,11,12, 13, 14,15,16], 1000)



