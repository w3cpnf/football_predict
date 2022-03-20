import os
os.chdir('D:/Projects/Football/Prediction_Code')

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import Read_Load_Prediction as db

from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt




def random_forest_score(X_train, X_test, y_train, y_test, n_, criterion):
    
    classifier = RandomForestClassifier(n_estimators = n_, criterion = criterion, random_state = 0)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    
    print("the score is:")
    print(score)
    
    return score


def random_forest_for_tool(df_results, df_variable, home_odds, draw_odds, away_odds):
    
    all_scores = []
    predict = []
    #all except 
    X_train = df_variable.values[:-1]
    X_test = df_variable.values[-1:]
    y_train = df_results.values[:-1].ravel()
    y_test = df_results.values[-1:].ravel()
    
    classifier = RandomForestClassifier(n_estimators = 2000, criterion='gini', random_state = 0)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    y_predict = classifier.predict(X_test)
    y_proba = classifier.predict_proba(X_test)
    
    all_scores.append(score)
    predict.append(y_predict)
    home_difference = (1/y_proba[0][2]) - home_odds
    draw_difference = (1/y_proba[0][1]) - draw_odds
    away_difference = (1/y_proba[0][0]) - away_odds
    
    
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


#random_forest_test(4, '2020/21', 31,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], 2000)


def get_randomforest_best_bet(forecast, variables, results, home_team, away_team):
    
    x = variables
    y = results.ravel()

    classifier = RandomForestClassifier(n_estimators = 2000, criterion = 'gini', random_state = 0)
    classifier.fit(x, y)
    
    x_forecast = forecast
    
    y_proba = classifier.predict_proba(x_forecast)
    

    print("Home Team : " + home_team + " against " + away_team)
    print("Fair odds for home win is : ")
    print(" ")    
    print(1/y_proba[0][2])

    print("Fair odds for draw is : ")   
    print(" ")
    print(1/y_proba[0][1])
    print(" ")

    print("Fair odds for home lost is : ")
    print(" ")
    print(1/y_proba[0][0])
    
    return y_proba




def random_forest_miner(vereins_ID, threshold_1, threshold_2, threshold_3):
    
    all_scores_1 = []
    factors_1 = []
    estimators_1 = []
    predict_1 = []
    
    f = db.get_data_db(9)
    df = f.get_data()
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 
             'Abwehrdifferenz','Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz',
             'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz','Trainer_ID', 'L1', 'L2', 'L3', 
             'L4', 'L5', 'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5']]    
    
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
    
    l1 = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    length_factors = len(l1)  

    for i in range(length_factors):
        for t in range(length_factors):
            variables = l1[i:t+1]
            
            if len(variables)==0:
                pass
            else:
                n_estimators = [100, 200, 500, 1000, 2000]
                
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
        X_train = df_set.iloc[:,variables].values[:-7]
        X_test = df_set.iloc[:,variables].values[-7:]
        y_train = df_set.iloc[:, 0].values[:-7]
        y_test = df_set.iloc[:, 0].values[-7:]
          
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
        X_train = df_set.iloc[:,variables].values[:-15]
        X_test = df_set.iloc[:,variables].values[-15:]
        y_train = df_set.iloc[:, 0].values[:-15]
        y_test = df_set.iloc[:, 0].values[-15:]
              
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