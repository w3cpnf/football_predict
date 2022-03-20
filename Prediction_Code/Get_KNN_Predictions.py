import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from itertools import combinations
import Read_Load_Prediction as db




#df_miner = knn_prediction_miner(4, 0.5, 0.5, 0.5)
#df_miner.to_csv('D:/Projects/Football/Code_ML/Data/results.csv')

def knn(vereins_ID, saison, spieltag, variables, n, m, p):
    #variables = list(variables)
    variables = variables.replace('[','')
    variables = variables.replace(']','')
    variables = variables.split(",")
    variables = [ int(x) for x in variables]
    print(variables)
    print(type(variables))
    print(n)
    print(m)
    print(p)
    f = db.get_data_db(9)
    df = f.get_data()
    
    f_1 = db.get_data_db(10)
    df_forecast = f_1.get_data()
    df_forecast = df_forecast[df_forecast['Saison']==saison]
    df_forecast = df_forecast[df_forecast['Spieltag']==spieltag]
    df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==vereins_ID]

    home_team = df_forecast['Heimmannschaft'].iloc[0]
    away_team = df_forecast['Gegner'].iloc[0]
    
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5', 'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5']]
    df_forecast = df_forecast[['Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 'L4_Forecast', 'L5_Forecast', 
            'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5']]   
    
    #get one club
    df_set = df[df['Heimmannschaft_ID']==vereins_ID]
   
    #choose variables to predict
    x = df_set.iloc[:,variables].values
    y = df_set.iloc[:, 0].values

    classifier = KNeighborsClassifier(n_neighbors = n, metric = m, p = p)
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
        print("Home team"+str(home_team) + " is expected to play draw against " + str(away_team))
    if y_pred[0] == -1:
        print(" ")
        print("Home team"+str(home_team) + " is expected to lose against " + str(away_team))
        
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


#knn(4, '2020/21', 31,[6, 7, 8, 9, 10, 11, 12],16, 'euclidean', 2)







def knn_prediction_miner(vereins_id, threshold_1, threshold_2, threshold_3):
    all_scores = []
    factors = []
    neighbors = []
    metric = []
    predict = []
    pp = []
    f = db.get_data_db(9)
    df = f.get_data()
    
    df = df[['Spiel_Ausgang', 'Heimmannschaft_ID', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
           'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz','Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
           'Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5', 'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5']] 
    
    df_set = df[df['Heimmannschaft_ID']==vereins_id]

    l1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    variables_all = sum([list(map(list, combinations(l1, i))) for i in range(len(l1) + 1)], [])
    for variables in variables_all:
        print(variables)
        if len(variables)==0:
            pass
        else:
            n_neighbors = [1, 2, 3, 4, 5, 8, 16]
            metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']
            params = [1,2,3,4,5]
            for n in n_neighbors:  
                
                for m in metrics:
                    
                    for p in params:
                
                        X_train = df_set.iloc[:,variables].values[:-10]
                        X_test = df_set.iloc[:,variables].values[-10:]
                        y_train = df_set.iloc[:, 0].values[:-10]
                        y_test = df_set.iloc[:, 0].values[-10:]  
                        
                        classifier = KNeighborsClassifier(n_neighbors = n, metric = m, p = p)
                        classifier.fit(X_train, y_train)    
                        
                        y_pred = classifier.predict(X_test)
                        score = classifier.score(X_test, y_test)
                        
                        all_scores.append(score)
                        factors.append(variables)
                        neighbors.append(n)
                        metric.append(m)
                        predict.append(y_pred)
                        pp.append(p)
                        print(score)
                        
    df = pd.DataFrame(
    {'Score': all_scores,
     'Factors': factors,
     'Neighbors': neighbors,
     'Metric': metric,
     'P_Value':pp,
     'Prediction': predict
    })
    df_1 = df[df['Score']>threshold_1]
    
    all_scores_1 = []
    factors_1 = []
    neighbors_1 = []
    metric_1 = []
    predict_1 = []
    pp_1 = []
    
    for i in range(len(df_1)):
        n = df_1['Neighbors'].iloc[i]
        variables = df_1['Factors'].iloc[i]
        m = df_1['Metric'].iloc[i]
        p = df_1['P_Value'].iloc[i]
        print(variables)

        X_train = df_set.iloc[:,variables].values[:-5]
        X_test = df_set.iloc[:,variables].values[-5:]
        y_train = df_set.iloc[:, 0].values[:-5]
        y_test = df_set.iloc[:, 0].values[-5:]
          
        classifier = KNeighborsClassifier(n_neighbors = n, metric = m, p = p)
        classifier.fit(X_train, y_train)    
        
        y_pred = classifier.predict(X_test)
        score = classifier.score(X_test, y_test)
        
        all_scores_1.append(score)
        factors_1.append(variables)
        neighbors_1.append(n)
        metric_1.append(m)
        predict_1.append(y_pred)
        pp_1.append(p)
        print(score)
                        
    df_2 = pd.DataFrame(
    {'Score': all_scores_1,
     'Factors': factors_1,
     'Neighbors': neighbors_1,
     'Metric': metric_1,
     'P_Value':pp_1,
     'Prediction': predict_1
    })

    df_2 = df_2[df_2['Score']>threshold_2]

    all_scores_2 = []
    factors_2 = []
    neighbors_2 = []
    metric_2 = []
    predict_2 = []
    pp_2 = []
    
    for i in range(len(df_2)):
        n = df_2['Neighbors'].iloc[i]
        variables = df_2['Factors'].iloc[i]
        m = df_2['Metric'].iloc[i]
        p = df_2['P_Value'].iloc[i]
        print(variables)

        X_train = df_set.iloc[:,variables].values[:-15]
        X_test = df_set.iloc[:,variables].values[-15:]
        y_train = df_set.iloc[:, 0].values[:-15]
        y_test = df_set.iloc[:, 0].values[-15:]
          
        classifier = KNeighborsClassifier(n_neighbors = n, metric = m, p = p)
        classifier.fit(X_train, y_train)    
        
        y_pred = classifier.predict(X_test)
        score = classifier.score(X_test, y_test)
        
        all_scores_2.append(score)
        factors_2.append(variables)
        neighbors_2.append(n)
        metric_2.append(m)
        predict_2.append(y_pred)
        pp_2.append(p)
        print(score)
                        
    df_3 = pd.DataFrame(
    {'Score': all_scores_2,
     'Factors': factors_2,
     'Neighbors': neighbors_2,
     'Metric': metric_2,
     'P_Value':pp_2,
     'Prediction': predict_2
    })

    df_3 = df_3[df_3['Score']>threshold_3]  
    
    return df_3 

    