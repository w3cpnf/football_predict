import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')
#packages and modules
import pandas as pd

#import other files 
import Read_Load_Database as db




#f = db.get_data_db(23)
#df_kommender_spieltag = f.get_data()
#df_kommender_spieltag = df_kommender_spieltag[df_kommender_spieltag['Spieltag']==27]
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
f = db.get_data_db(24)
df = f.get_data()
df = df.drop_duplicates()
df = df[df['Vereins_ID']==1]

seasons = df['Saison'].drop_duplicates()
df_all = pd.DataFrame()



for s in seasons:
    l_average = []
    df_saison = df[df['Saison']==s]
    #df_saison.index = range(len(df_saison))
    #len(df_saison)
    spieltage = df_saison['Spieltag'].drop_duplicates()
    #print(df_saisons)
    
    for sp in spieltage:
        if sp == 1:
            l_average.append(1)
        else:
            df_spieltag = df_saison[df_saison['Spieltag']<sp]
            l_average.append(np.average(df_spieltag['Schüsse']))
    print(len(df_saison))      
    print(len(l_average))
    df_saison['Average_Torschuesse']=l_average
    df_all = df_all.append(df_saison)
    

#df_all.to_csv('D:/Projects/Football/Database/test.csv')   


f = db.get_data_db(22)
df = f.get_data()
df = df[df['Vereins_ID']==1] 
df = df[['Saison', 'Spieltag', 'Spiel_Ausgang']]  

df_all = df.merge(df_all, on = ['Saison', 'Spieltag'], how = 'inner')
df_check = df_all[['Spiel_Ausgang', 'Average_Torschuesse']]
X = df_check.iloc[:,1]  #independent columns
y = df_check.iloc[:,0]    #target column i.e price range
#get correlations of each features in dataset
corrmat = df_check.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(df_check[top_corr_features].corr(),annot=True,cmap="RdYlGn")
plt.savefig('D:/Projects/Football/Prediction_Code/Correlation/correlation.png')






from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.cov_struct import (Exchangeable, Independence, Autoregressive)
from statsmodels.genmod.families import Poisson


fam = Poisson()
ind = Independence()
model1 = GEE.from_formula("y ~ age + trt + base", "subject", data, cov_struct=ind, family=fam)
result1 = model1.fit()
print(result1.summary())