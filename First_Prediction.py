import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


class predict:
    
    def __init__(self, df):
        self.df = df

    def random_forest(self):
        df = self.df
        v_id = df['Heimmannschaft_ID'].drop_duplicates()           
        gesamt = []
        for v in v_id:
    
            df_set = df[df['Heimmannschaft_ID']==v]
            X = df_set.iloc[:,2:len(df_set)].values
            y = df_set.iloc[:, 0].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0, shuffle= False) 
                
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)  
                   
            classifier = RandomForestClassifier(n_estimators = 41, random_state = 0)
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)
            score = classifier.score(X_test, y_test)
            gesamt.append(score)
            
        return gesamt

    def knn(self):
        df = self.df
        v_id = df['Heimmannschaft_ID'].drop_duplicates()
        gesamt = []
        for v in v_id:
            
            df_set = df[df['Heimmannschaft_ID']==v]
            X = df_set.iloc[:,2:len(df_set)].values
            y = df_set.iloc[:, 0].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0, shuffle= False)   
            
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)     
            
            classifier = KNeighborsClassifier()
            classifier.fit(X_train, y_train)       
            y_pred = classifier.predict(X_test)
            score = classifier.score(X_test, y_test)
            
            gesamt.append(score)
            
        return gesamt    
    
    def log_reg(self):       
        df = self.df
        v_id = df['Heimmannschaft_ID'].drop_duplicates() 
        gesamt = []
        for v in v_id:
            df_set = df[df['Heimmannschaft_ID']==v]
                       
            X = df_set.iloc[:,2:len(df_set)].values
            y = df_set.iloc[:, 0].values  
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0, shuffle= False) 
                
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)
            
            logreg = LogisticRegression(solver = 'newton-cg')
            logreg.fit(X_train, y_train)
            y_pred = logreg.predict(X_test)
            score = logreg.score(X_test, y_test)
            gesamt.append(score)
            
        return gesamt








