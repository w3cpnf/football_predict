import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
from selenium import webdriver
import time
import numpy as np
import pandas as pd
from collections import Counter

import My_Tools as t
import Read_Load_Database as db
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
import itertools


def get_dataframe_startelf(l_players):
    if len(l_players)==22:
        df = pd.DataFrame(l_players) 
        df = t.columns(df, 12)
    else:
        l_players = l_players[1:23]
        df = pd.DataFrame(l_players) 
        df = t.columns(df, 12)    
    
    return df

def replace_player_name(df):
    df = df.replace({'Cleber':'Reis', 'Junior':'Caicara', 'Fedetsky':'Fedetskyi', 'Marset':'Torro'
                                 , 'Aaron':'Martin', 'Kunde': 'Malong', 'Silas':'Mvumpa', 'Bruun Larsen':'Larsen',
                                 'Bella-Kotchap':'Kotchap', 'Myziane':'Maolida', 'Jae-Sung': 'Lee', 'Dabour':'Dabbur',
                                 'Mueller':'Müller', 'PEDERSEN':'Pedersen', 'Loewen':'Löwen', 'Antwi-Adjej':'Antwi-Adjei',
                                 'Maury':'Borre', 'Tasende':'Angelino', 'Odilon':'Kossounou', 'Kouassi':'Nianzou',
                                 'Woo-Yeong':'Jeong'})
    return df

def getClubs(url):
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')    
    driver.get(url)
    time.sleep(2)
    clubs = driver.find_elements_by_xpath("//div[@class='leg_column_row']")
    urls = []

    for i in range(len(clubs)):
        text = clubs[i].get_attribute('innerHTML')
        index_home = text.find("href") + 7
        index_ende_home = text.find("2022/") + 11
        clubUrlHome = text[index_home:index_ende_home]
        print(clubUrlHome)
        urls.append(clubUrlHome)
        index_away = text.find("href", text.find("href") + 1) + 7
        index_ende_away = text.find("2022/", text.find("2022/") + 1) + 11
        clubUrlAway = text[index_away:index_ende_away]
        print(clubUrlAway)
        urls.append(clubUrlAway)
    driver.quit()
    return urls

def getNachname(df):
    dfSpieler = df['Spieler'].str.split(" ", expand = True)
    dfSpieler.index = range(len(dfSpieler))
    spieler = []
    dfSpieler = dfSpieler.fillna(0)
    
    for i in range(len(dfSpieler)):
        columns = len(dfSpieler.columns)-1   
        while columns >= 0:
            if dfSpieler.iloc[i, columns]!= 0:
                spieler.append(dfSpieler.iloc[i, columns])
                columns = -1
            else:
                columns = columns - 1
    df['Spieler_Nachname']=spieler
    return df


def getNachnameCorrect(df):
    dfSpieler = df['Spieler_Nachname'].str.split(" ", expand = True)
    dfSpieler.index = range(len(dfSpieler))
    spieler = []
    dfSpieler = dfSpieler.fillna(0)
    
    for i in range(len(dfSpieler)):
        columns = len(dfSpieler.columns)-1   
        while columns >= 0:
            if dfSpieler.iloc[i, columns]!= 0:
                spieler.append(dfSpieler.iloc[i, columns])
                columns = -1
            else:
                columns = columns - 1
    df['Spieler_Nachname']=spieler
    df = df.replace({'Prince': 'Boateng', 'Matuschyk': 'Matuszczyk'})

    return df

def getSquadNachname(saison):

    dfID = db.get_table('bl1_staging_spieler_kader')
    dfID = dfID[dfID['Saison']==saison]
    dfID = dfID[['Spieler', 'Spieler_ID', 'Verein', 'Vereins_ID']]
    dfID = dfID.drop_duplicates()
    dfID.index = range(len(dfID))


    dfSpieler = dfID['Spieler'].str.split(" ", expand = True)
    dfSpieler.index = range(len(dfSpieler))
    spieler = []
    dfSpieler = dfSpieler.fillna(0)
    
    for i in range(len(dfSpieler)):
        columns = len(dfSpieler.columns) - 1   
        while columns >= 0:
            if dfSpieler.iloc[i, columns]!= 0:
                spieler.append(dfSpieler.iloc[i, columns])
                columns = - 1
            else:
                columns = columns - 1
    dfID['Spieler_Nachname']=spieler
    
    return dfID

def removePlayerWithSameFamilyName (df):
    
    if len(df.groupby('Vereins_ID').count())>1:
        occurence_count = Counter(df['Vereins_ID'])
        vereins_id = occurence_count.most_common(1)[0][0]
        df = df[df['Vereins_ID']==vereins_id]
        print(vereins_id)
        
    return df


def getStartelfSingle(Url, spieltag, saison, dfID):

    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(Url)
    time.sleep(3)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")        
    player = driver.find_elements_by_xpath("//div[@class='player_name']")
    f1 = t.get_df(player)
    dfPlayer = f1.df()
    driver.quit()
    dfPlayer = dfPlayer[dfPlayer[0]!=''][[0]]
    dfPlayer.columns = ['Spieler_Nachname']
    f = t.unify_letters(dfPlayer, 3)
    dfPlayer = f.replace_letters()
    dfPlayer.index = range(len(dfPlayer))
    dfPlayer = dfPlayer.iloc[0:11]
    print(dfPlayer)
    dfPlayer = getNachnameCorrect(dfPlayer)
    dfPlayer = replace_player_name(dfPlayer)  
    df = dfPlayer.merge(dfID, on = 'Spieler_Nachname', how = 'inner')
    df_rest = dfPlayer.merge(df, on = ['Spieler_Nachname'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    print(df_rest)
    df = removePlayerWithSameFamilyName(df)
    df = df.assign(Spieltag = spieltag, Saison = saison)
        
    return df
 

#add player not found
def getStartelf(Urls, spieltag, saison, dfID):
    df_all = pd.DataFrame()
    for clubUrl in Urls:
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        print(clubUrl)
        url = 'https://www.ligainsider.de/'+clubUrl
        driver.get(url)
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[@id="cmpbntyestxt"]'))).click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")        
        player = driver.find_elements_by_xpath("//div[@class='player_name']")
        f1 = t.get_df(player)
        dfPlayer = f1.df()
        driver.quit()
        dfPlayer = dfPlayer[dfPlayer[0]!=''][[0]]
        dfPlayer.columns = ['Spieler_Nachname']
        f = t.unify_letters(dfPlayer, 3)
        dfPlayer = f.replace_letters()
        dfPlayer.index = range(len(dfPlayer))
        dfPlayer = dfPlayer.iloc[0:11]
        dfPlayer = getNachnameCorrect(dfPlayer)
        dfPlayer = replace_player_name(dfPlayer)
 
        df = dfPlayer.merge(dfID, on = 'Spieler_Nachname', how = 'inner')
        df_rest = dfPlayer.merge(df, on = ['Spieler_Nachname'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
        print(df_rest)
        df = removePlayerWithSameFamilyName(df)
        df = df.assign(Spieltag = spieltag, Saison = saison)
        print(len(df))
        df_all = df_all.append(df)
        
    return df_all

saison = '2021/22'
spieltag = 26
Url_clubs = 'https://www.ligainsider.de/bundesliga/spieltage/saison-2021-2022/66543/'

#Urls = getClubs(Url_clubs)
#dfID = getSquadNachname(saison)
#df = getStartelf(Urls, spieltag, saison, dfID)

#db.upload_local_data_to_database(df, 'bl1_data_startelf')
#df = getStartelfSingle('https://www.ligainsider.de/bundesliga/team/rb-leipzig/1311/saison-2019-2020/116538/', 1, '2019/20', dfID)

def get_feature_startelf(saison, spieltag):
    dfStartelf = db.get_table('bl1_data_startelf')
    dfStartelf = dfStartelf[dfStartelf['Saison']==saison]
    dfStartelf = dfStartelf[dfStartelf['Spieltag']==spieltag]

    df_all = pd.DataFrame()
    for vereins_id in dfStartelf['Vereins_ID'].drop_duplicates():
        dfStartelf_verein = dfStartelf[dfStartelf['Vereins_ID']==vereins_id]
        #dfStartelf_verein.index = range(len(dfStartelf_verein))
        for s in range(1, len(dfStartelf_verein)):
            column = 'Spieler_' + str(s+1)
            dfStartelf_verein.loc[:, column] = dfStartelf_verein.iloc[s, 2]
        dfStartelf_verein = dfStartelf_verein.rename(columns = {'Spieler_ID':'Spieler_1'})
        dfStartelf_verein = dfStartelf_verein.iloc[0, :]
        df_all = df_all.append(dfStartelf_verein)
        
    df_all = df_all.drop_duplicates()
    df_all = df_all[['Saison', 'Spieltag', 'Vereins_ID', 'Spieler_1', 'Spieler_2', 'Spieler_3', 'Spieler_4', 'Spieler_5', 'Spieler_6', 'Spieler_7',
                     'Spieler_8', 'Spieler_9','Spieler_10', 'Spieler_11']]    
    
    df_feature_startelf = db.get_table('bl1_features_startelf')     
    df_feature_startelf = df_feature_startelf[df_feature_startelf['Saison'] ==saison]
    df_feature_startelf = df_feature_startelf[df_feature_startelf['Spieltag']==spieltag]  
    
    df_all = df_all[~df_all.apply(tuple, 1).isin(df_feature_startelf.apply(tuple, 1))]
         
    return df_all







def get_features_startelf_all():
    dfStartelf = db.get_table('bl1_data_startelf')
    dfStartelf = dfStartelf[['Saison', 'Spieltag', 'Vereins_ID', 'Spieler_ID']]
    
    df_all = pd.DataFrame()
    for saison in dfStartelf['Saison'].drop_duplicates():
        dfStartelf_saison = dfStartelf[dfStartelf['Saison']==saison]
        for spieltag in dfStartelf_saison['Spieltag'].drop_duplicates():
            dfStartelf_spieltag = dfStartelf_saison[dfStartelf_saison['Spieltag']==spieltag]
            for vereins_id in dfStartelf_spieltag['Vereins_ID'].drop_duplicates():
                dfStartelf_verein = dfStartelf_spieltag[dfStartelf_spieltag['Vereins_ID']==vereins_id]
                for s in range(1, len(dfStartelf_verein)):
                    column = 'Spieler_' + str(s+1)
                    dfStartelf_verein.loc[:, column] = dfStartelf_verein.iloc[s, 3] 
                    
                dfStartelf_verein = dfStartelf_verein.rename(columns = {'Spieler_ID':'Spieler_1'})
                dfStartelf_verein = dfStartelf_verein.iloc[0, :]
                df_all = df_all.append(dfStartelf_verein)
                    
    df_all = df_all.drop_duplicates()
    df_all = df_all[['Saison', 'Spieltag', 'Vereins_ID', 'Spieler_1', 'Spieler_2', 'Spieler_3', 'Spieler_4', 'Spieler_5', 'Spieler_6', 'Spieler_7',
                     'Spieler_8', 'Spieler_9','Spieler_10', 'Spieler_11']]    
    return df_all
#db.upload_local_data_to_database(df_all, 'bl1_features_startelf')        

#dfStartelf_saison = dfStartelf[dfStartelf['Saison']=='2014/15']
#dfStartelf_spieltag = dfStartelf_saison[dfStartelf_saison['Spieltag']==1]
#dfStartelf_verein = dfStartelf_spieltag[dfStartelf_spieltag['Vereins_ID']==1]

#for s in range(1, len(dfStartelf_verein)):
#    column = 'Spieler_' + str(s+1)
#    dfStartelf_verein.loc[:, column] = dfStartelf_verein.iloc[s, 3] 

 


def get_startelf_google(url, saison, spieltag):

    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@id="L2AGLb"]'))).click()
    time.sleep(5)
    players = driver.find_elements_by_xpath("//div[@class='lr-vl-ls']") 
    players_home = players[0].text
    players_away = players[1].text
    
    home = players_home.split('\n')
    away = players_away.split('\n')
            
    df_home = get_dataframe_startelf(home)     
    df_away = get_dataframe_startelf(away) 

    f1 = t.unify_letters(df_home, 1)
    f2 = t.unify_letters(df_away, 1)
    df_home = f1.replace_letters()
    df_away = f2.replace_letters()
    df_home = getNachname(df_home)
    df_away = getNachname(df_away)
    
    df_home = replace_player_name(df_home) 
    df_away = replace_player_name(df_away) 
    dfID = getSquadNachname('2021/22')
    
    df_home = df_home.drop('Spieler', axis = 1)
    df_away = df_away.drop('Spieler', axis = 1)

    df_home = df_home.merge(dfID, on = 'Spieler_Nachname', how = 'inner')
    df_away = df_away.merge(dfID, on = 'Spieler_Nachname', how = 'inner')
    
    df_home = removePlayerWithSameFamilyName(df_home)
    df_home = df_home.assign(Spieltag = spieltag, Saison = saison)
    
    df_away = removePlayerWithSameFamilyName(df_away)
    df_away = df_away.assign(Spieltag = spieltag, Saison = saison)
    df_home = df_home[['Spieler_Nachname', 'Spieler', 'Spieler_ID', 'Verein', 'Vereins_ID', 'Spieltag', 'Saison']]
    df_away = df_away[['Spieler_Nachname', 'Spieler', 'Spieler_ID', 'Verein', 'Vereins_ID', 'Spieltag', 'Saison']]
    driver.quit()
    
    return df_home, df_away

url = 'https://www.google.de/search?q=bundesliga&sxsrf=ALiCzsaICL--Qozp91i8VvUsAOVN7dimcA%3A1651253674246&source=hp&ei=qiFsYpi2C8mMkgX9ipDYBQ&iflsig=AJiK0e8AAAAAYmwvujByrcP70qVlizwomFUY2A5Op9Df&ved=0ahUKEwiYs7yl57n3AhVJhqQKHX0FBFsQ4dUDCAk&uact=5&oq=bundesliga&gs_lcp=Cgdnd3Mtd2l6EAMyBAguECcyBAgjECcyBAgjECcyCwgAEIAEELEDEIMBMg0IABCABBCHAhCxAxAUMgsIABCABBCxAxCDATIICAAQgAQQsQMyCAgAEIAEELEDMgsIABCABBCxAxCDAToKCAAQsQMQgwEQQzoICC4QsQMQgwE6CgguEMcBEKMCEEM6BAguEEM6CAgAELEDEIMBOg4ILhCABBCxAxDHARCjAjoECAAQQzoHCC4Q1AIQQzoTCC4QsQMQgwEQxwEQowIQ1AIQQzoICC4QgAQQsQNQAFjYCGDJCWgAcAB4AIABdIgBxQaSAQM4LjKYAQCgAQE&sclient=gws-wiz#sie=m;/g/11rgnqsjqv;2;/m/037169;dt;fp;1;;'
saison = '2021/22'
spieltag = 32
#df_home_startelf, df_away_startelf = get_startelf_google(url, saison, spieltag)
#df_home_startelf = df_home_startelf[df_home_startelf['Spieler']!='Keven Schlotterbeck']
#df_away_startelf = df_away_startelf[df_away_startelf['Spieler']!='Felix Nmecha']
#df_home_startelf = df_home_startelf[df_home_startelf['Spieler']!='Jannes Horn']
#db.upload_local_data_to_database(df_home_startelf, 'bl1_data_startelf')      
#db.upload_local_data_to_database(df_away_startelf, 'bl1_data_startelf')   


#df_feature = get_feature_startelf('2021/22', 32)

#db.upload_local_data_to_database(df_feature, 'bl1_features_startelf')   


# dfStartelf = db.get_table('bl1_features_startelf')
# dfStartelf_only_player = dfStartelf[['Spieler_1', 'Spieler_2', 'Spieler_3', 'Spieler_4', 'Spieler_5', 'Spieler_6', 'Spieler_7', 'Spieler_8', 'Spieler_9', 'Spieler_10', 'Spieler_11']]
# list_startelf = dfStartelf_only_player.values.tolist()
# list_startelf.sort()
# unique_startelf = list(list_startelf for list_startelf,_ in itertools.groupby(list_startelf))





