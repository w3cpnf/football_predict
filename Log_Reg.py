from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pandas as pd


def get_y(df):
    
    df = df.assign(Gesamtdifferenz = lambda x:x['Gesamt']-x['Gegnergesamt'], Angriffdifferenz = lambda x:x['Angriff']-x['Gegnerabwehr'], Abwehrdifferenz = lambda x:x['Abwehr']-x['Gegnerangriff'],
    Mittelfelddifferenz = lambda x:x['Mittelfeld']-x['Gegnermittelfeld'])
    df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 1 if x > 0 else 0)
    df = df.sort_values(by = ['Saison','Spieltag', 'Vereins_ID'])
    df = df[['Vereins_ID', 'Spieltag', 'Spiel_Ausgang', 'Heim','Gesamtdifferenz', 'Angriffdifferenz', 'Abwehrdifferenz', 'Mittelfelddifferenz', 'Saison']]
   
    return df


class log_reg:
    
    def __init__(self, df):
        self.df = df
    
    def reg(self):
        df = self.df

        df_s = pd.DataFrame()
        v_ids = df['Vereins_ID'].drop_duplicates() 
    
        for v in v_ids:
            df_set = df[df['Vereins_ID']==v]
            
            if len(df_set)>170:
                
                X = df_set.iloc[:, [4,5,6,7]].values
                y = df_set.iloc[:, 2].values
            
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0, shuffle= False) 
                    
                sc = StandardScaler()
                X_train = sc.fit_transform(X_train)
                X_test = sc.transform(X_test)
                logreg = LogisticRegression(solver = 'newton-cg')
                logreg.fit(X_train, y_train)
                y_pred = logreg.predict(X_test)
                score = logreg.score(X_test, y_test)
                predict_pro = logreg.predict_proba(X_test)
                           
                df_proba = pd.DataFrame(predict_pro, columns=['P_NoWin', 'P_Win'])    
                df_proba = df_proba.assign(Vereins_ID = v)
                df_proba = df_proba.assign(Score = score)
                df_proba = df_proba.assign(Prediction = y_pred)
                df_s = df_s.append(df_proba)
                
        print('The overall score is : ' + str(sum(df_s['Score'])/len(df_s)))
            
        return df_s







