import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
from selenium import webdriver
import time
import numpy as np
import pandas as pd

import My_Tools as t
import Read_Load_Database as db
import numpy as np


def changeColumn(df):
    x = 1
    for col in df.columns[0:]:
      name = 'Spieler_'+str(x)
      df = df.rename(columns={col:name})
      x = x+1

    return df

def getPlayerFeatures():
    
    dfPlayerPlayed = db.get_table('bl1_data_spieler_startelf_system')
    dfPlayerPlayed = dfPlayerPlayed.sort_values(['Saison', 'Spieltag'])
    dfPlayerPlayed = dfPlayerPlayed[['Saison', 'Spieltag', 'Vereins_ID', 'Spieler_ID']]
    allPlayer = []
    allPlayerLength = []
    df = pd.DataFrame()
    
    for saison in dfPlayerPlayed['Saison'].drop_duplicates():
        dfSaison = dfPlayerPlayed[dfPlayerPlayed['Saison']==saison]
        
        for spieltag in dfSaison['Spieltag'].drop_duplicates():
            dfSpieltag = dfSaison[dfSaison['Spieltag']==spieltag]
            
            for verein in dfSpieltag['Vereins_ID']:
                dfVerein = dfSpieltag[dfSpieltag['Vereins_ID']==verein]
                dfTransposed = dfVerein[['Spieler_ID']].T
                dfTransposed = changeColumn(dfTransposed)
                dfTransposed = dfTransposed.assign(Spieltag = spieltag, Saison = saison, Vereins_ID = verein)
                allPlayer.append(dfTransposed)
                allPlayerLength.append(len(dfTransposed.columns))
      
    df = df.append(allPlayer[np.argmax(allPlayerLength)])
    
    for x in range(np.argmax(allPlayerLength)):
        df = df.append(allPlayer[x])
    for y in range(np.argmax(allPlayerLength),len(allPlayer)):
        df = df.append(allPlayer[y])
        
    df = df.drop_duplicates()  
    return df
            
            
        
#dfSaison = dfPlayerPlayed[dfPlayerPlayed['Saison']=='2020/21']
#dfSpieltag = dfSaison[dfSaison['Spieltag']==1]
#dfVerein = dfSpieltag[dfSpieltag['Vereins_ID']==7]

df = getPlayerFeatures()
df = df.sort_values(['Saison', 'Spieltag'])
#db.upload_local_data_to_database(df, 'bl1_features_spieler_gespielt')
