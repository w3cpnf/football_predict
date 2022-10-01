import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 

import Read_Load_Database as db
import My_Tools as t



def get_bundesliga_player_daten(saison, c, spieltag):  
    
    s1 = 'saison-'+saison[0:4]+'-20'+saison[5:7]
    
    f3 = db.get_data_db(7)
    df_mapping_transfermarkt = f3.get_data()   
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[c-1]

    f2 = db.get_data_db(2)
    df_spielplan = f2.get_data()
    df_spielplan = df_spielplan[df_spielplan['Saison']==saison]
    
    f1 = db.get_data_db(4)
    df_spieler_url = f1.get_data()
    df_spieler_url = df_spieler_url[df_spieler_url['Saison']==saison]
    df_spieler_url = df_spieler_url[df_spieler_url['Vereins_ID']==v1]
    
    f_k =db.get_data_db(12)
    df_kader = f_k.get_data()
    df_kader = df_kader[df_kader['Saison']==saison]
    df_kader = df_kader[df_kader['Vereins_ID']==v1]

    f_s =db.get_data_db(49)
    df_spieler = f_s.get_data()
    df_spieler = df_spieler[df_spieler['Saison']==saison]
    df_spieler = df_spieler[df_spieler['Vereins_ID']==v1]
    
    url = df_spieler_url['Url'].drop_duplicates()

    df_all = pd.DataFrame()
    for u in url:
        
        df_player = df_spieler_url[df_spieler_url['Url']==u]
        spieler_id = df_player['Spieler_ID'].iloc[0]
        spieler = df_player['Spieler'].iloc[0]
        vereins_id = df_player['Vereins_ID'].iloc[0]
        verein = df_player['Verein'].iloc[0]
        print(spieler_id)
        position = df_kader[df_kader['Spieler_ID']==spieler_id]['Position'].iloc[0]
        x = str(u)+'/bundesliga_daten/'+str(s1)
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get(x) 
        #time.sleep(2)
        #driver.find_element_by_xpath('//*[@text ="Akzeptieren & schließen"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[@id="cmpbntyestxt"]'))).click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            bundesliga_daten = driver.find_elements_by_xpath("//div[@class='data_column text-center']")
            
            if len(bundesliga_daten)>0:          
                df_t = t.get_dataframe(bundesliga_daten)
                #position = driver.find_element_by_xpath("//div[@class='data_column_right text-center pull-left']")
        
                if position == 'Torwart':
                    print(position)
                    df_t = t.columns(df_t,3)
                    driver.quit()
        
                    df_t[['Abgwehrte_Schüsse_Prozent', 'Abgwehrte_Schüsse_Absolut']] = df_t['Abgwehrte_Schüsse'].str.split('\n', expand = True)
                    df_t[['Elfmeter_Pariert_Prozent', 'Elfmeter_Pariert_Absolut']] = df_t['Elfmeter_Pariert'].str.split('\n', expand = True)
                    df_t[['Großchancen_Pariert_Prozent', 'Großchancen_Pariert_Absolut']] = df_t['Großchancen_Pariert'].str.split('\n', expand = True)
                    df_t[['Strafraum_Beherrschung_Prozent', 'Strafraum_Beherrschung_Absolut']] = df_t['Strafraum_Beherrschung'].str.split('\n', expand = True)
                    df_t = df_t.drop(['Abgwehrte_Schüsse', 'Elfmeter_Pariert', 'Großchancen_Pariert', 'Strafraum_Beherrschung'], axis = 1)
                    df_t['Spieltag'] = range(0, len(df_t))
                    df_t = df_t.assign(Spieler = spieler, Spieler_ID = spieler_id, Vereins_ID = vereins_id, Verein = verein, Saison = saison)
                    
                    
                    df_all = df_all.append(df_t)
        
                else:
                    df_s = t.columns(df_t, 4)
                    driver.quit()
                    df_s[['Gewonnene_Zweikämpfe_Prozent', 'Gewonnene_Zweikämpfe_Absolut']] = df_s['Gewonnene_Zweikämpfe'].str.split('\n', expand = True)
                    df_s[['Erfolgreiche_Pässe_Prozent', 'Erfolgreiche_Pässe_Absolut']] = df_s['Erfolgreiche_Pässe'].str.split('\n', expand = True)
                    df_s[['Gewonnene_Luftkämpfe_Prozent', 'Gewonnene_Luftkämpfe_Absolut']] = df_s['Gewonnene_Luftkämpfe'].str.split('\n', expand = True)
                    df_s[['Erfolgreiche_Tacklings_Prozent', 'Erfolgreiche_Tacklings_Absolut']] = df_s['Erfolgreiche_Tacklings'].str.split('\n', expand = True)
                    df_s[['Erfolgreiche_Dribblings_Prozent', 'Erfolgreiche_Dribblings_Absolut']] = df_s['Erfolgreiche_Dribblings'].str.split('\n', expand = True)
                    df_s[['Schussgenauigkeit_Prozent', 'Schussgenauigkeit_Absolut']] = df_s['Schussgenauigkeit'].str.split('\n', expand = True)
                    df_s = df_s.drop(['Erfolgreiche_Pässe', 'Gewonnene_Luftkämpfe', 'Erfolgreiche_Tacklings', 'Erfolgreiche_Dribblings', 
                                      'Schussgenauigkeit', 'Gewonnene_Zweikämpfe'], axis = 1)
                    df_s['Spieltag'] = range(0, len(df_s))
                    df_s = df_s.assign(Spieler = spieler, Spieler_ID = spieler_id, Vereins_ID = vereins_id, Verein = verein, Saison = saison)
                    df_all = df_all.append(df_s)
            else:
                print("NoData")
                driver.quit()
                
        except NoSuchElementException as v:          
            print(v)
            driver.quit()
            
    df_all = df_all.replace({'-': 0})
    df_all = df_all.replace({'-\n(-)': 0})
    df_all = df_all.replace({'': 0})
    df_all = df_all.fillna(0)
    df_all['Spieltag'] = df_all['Spieltag']+1 
    
    #df_all = df_all[df_all['Spieltag']==spieltag]
    
    df_all = df_all.merge(df_spielplan, on = ['Verein', 'Vereins_ID', 'Saison', 'Spieltag'], how = 'inner')
    df_all = df_all.merge(df_spieler, on = ['Verein', 'Vereins_ID', 'Spieler', 'Spieler_ID', 'Saison', 'Spieltag'], how = 'inner')
    
    df_all = df_all[['Spieler_ID','Spieler', 'Vereins_ID', 'Verein','Spieltag', 
        'Fouls', 'Geklärte_Bälle', 'Abgefangene_Bälle',
       'Ball_Eroberungen', 'Ballverluste', 'Torschuss_Vorlagen',
       'Kreierte_Großchancen', 'Schüsse_aufs_Tor',
       'Fehler_vor_Schuss_Gegentor', 'Geblockte_Bälle',
       'Gewonnene_Zweikämpfe_Prozent', 'Gewonnene_Zweikämpfe_Absolut',
       'Erfolgreiche_Pässe_Prozent', 'Erfolgreiche_Pässe_Absolut',
       'Gewonnene_Luftkämpfe_Prozent', 'Gewonnene_Luftkämpfe_Absolut',
       'Erfolgreiche_Tacklings_Prozent', 'Erfolgreiche_Tacklings_Absolut',
       'Erfolgreiche_Dribblings_Prozent', 'Erfolgreiche_Dribblings_Absolut',
       'Schussgenauigkeit_Prozent', 'Schussgenauigkeit_Absolut','Paraden', 'Weiße_Weste', 'Abgwehrte_Schüsse_Prozent', 'Abgwehrte_Schüsse_Absolut',
       'Elfmeter_Pariert_Prozent', 'Elfmeter_Pariert_Absolut',
       'Großchancen_Pariert_Prozent', 'Großchancen_Pariert_Absolut', 'Strafraum_Beherrschung_Prozent', 'Strafraum_Beherrschung_Absolut', 'Woche', 'Jahr',
       'Saison']]
    

    df_all = df_all.fillna(0)
            
    return df_all

#df = get_bundesliga_player_daten('2020/21', 11, 1)    
#db.upload_local_db_data(df, 22)
#db.upload_local_data_to_database(df, 'bl1_staging_spieler_kader')

#.iloc[50,:]
# df_all['Note_Spieltag'] = df_all['Note_Spieltag'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
# df_all['Note_Spieltag'] = df_all['Note_Spieltag'].str.replace(',','.').astype(float)
# df_all['Durchschnitt_Note'] = df_all['Durchschnitt_Note'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
# df_all['Durchschnitt_Note'] = df_all['Durchschnitt_Note'].fillna(0).str.replace(',','.').astype(float)
# df_all['Durchschnitt_Pos_Pkt'] = df_all['Durchschnitt_Pos_Pkt'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
# df_all['Durchschnitt_Pos_Pkt'] = df_all['Durchschnitt_Pos_Pkt'].fillna(0).str.replace(',','.').astype(float)
# df_all['Pkt_Spieltag'] = df_all['Pkt_Spieltag'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
# df_all['Pkt_Spieltag']  = df_all['Pkt_Spieltag'].astype(float)
    
def get_data_ligainsider(saison, c, spieltag):
    

    f_l = db.get_data_db(8)
    df_staging_ligainsider = f_l.get_data()
    
    f3 = db.get_data_db(7)
    df_mapping_transfermarkt = f3.get_data()   
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[c-1] 
   
    print(v1)
    df_staging_ligainsider = df_staging_ligainsider[df_staging_ligainsider['Saison']==saison] 
    df_staging_ligainsider = df_staging_ligainsider[df_staging_ligainsider['Vereins_ID']==v1]
    
    #df_staging_ligainsider = df_staging_ligainsider[df_staging_ligainsider['Spieltag']==spieltag]
    #df_staging_ligainsider['Paraden'] = df_staging_ligainsider['Paraden'].astype(int)
    
    df_staging_ligainsider['Gewonnene_Zweikämpfe_Prozent'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Zweikämpfe'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Gewonnene_Zweikämpfe'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Erfolgreiche_Pässe_Prozent'] = df_staging_ligainsider['Erfolgreiche_Pässe_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Pässe'] = df_staging_ligainsider['Erfolgreiche_Pässe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Erfolgreiche_Pässe'] = df_staging_ligainsider['Erfolgreiche_Pässe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Gewonnene_Luftkämpfe_Prozent'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Luftkämpfe'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Gewonnene_Luftkämpfe'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Erfolgreiche_Tacklings_Prozent'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Tacklings'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Erfolgreiche_Tacklings'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Erfolgreiche_Dribblings_Prozent'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Dribblings'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Erfolgreiche_Dribblings'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Schussgenauigkeit_Prozent'] = df_staging_ligainsider['Schussgenauigkeit_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Schussgenauigkeit'] = df_staging_ligainsider['Schussgenauigkeit_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Erfolgreiche_Schussgenauigkeit'] = df_staging_ligainsider['Schussgenauigkeit_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    df_staging_ligainsider['Abgwehrte_Schüsse_Prozent'] = df_staging_ligainsider['Abgwehrte_Schüsse_Prozent'].str.split('%', expand = True)[0].astype(int)
    df_staging_ligainsider['Abgwehrte_Schüsse'] = df_staging_ligainsider['Abgwehrte_Schüsse_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Erfolgreiche_Abgwehrte_Schüsse'] = df_staging_ligainsider['Abgwehrte_Schüsse_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    
    
    df_staging_ligainsider['Elfmeter'] = df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
    df_staging_ligainsider['Elfmeter_Pariert_Prozent'] = df_staging_ligainsider['Elfmeter_Pariert_Prozent'].str.split('%', expand = True)[0].astype(float)
    if len(df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True).columns) > 1:
        df_staging_ligainsider['Elfmeter_Pariert'] = df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    else:
        df_staging_ligainsider['Elfmeter_Pariert'] = 0    
          
    df_staging_ligainsider['Großchancen_Pariert_Prozent'] = df_staging_ligainsider['Großchancen_Pariert_Prozent'].str.split('%', expand = True)[0].astype(float)
    df_staging_ligainsider['Großchancen'] = df_staging_ligainsider['Großchancen_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
    df_staging_ligainsider['Großchancen_Pariert'] = df_staging_ligainsider['Großchancen_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

    df_staging_ligainsider['Strafraum_Beherrschung_Prozent'] = df_staging_ligainsider['Strafraum_Beherrschung_Prozent'].str.split('%', expand = True)[0].astype(float)
    if len(df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True).columns)>1:
        df_staging_ligainsider['Strafraum_Beherrschung'] = df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
        df_staging_ligainsider['Erfolgreiche_Strafraum_Beherrschung'] = df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)    
    else:
        df_staging_ligainsider['Strafraum_Beherrschung'] = 0  
        df_staging_ligainsider['Erfolgreiche_Strafraum_Beherrschung'] = 0  
    
    df_staging_ligainsider = df_staging_ligainsider[[
        'Spieler_ID','Spieler', 'Vereins_ID', 'Verein','Spieltag', 'Fouls', 'Geklärte_Bälle', 'Abgefangene_Bälle','Ball_Eroberungen', 'Ballverluste',
        'Torschuss_Vorlagen', 'Kreierte_Großchancen', 'Schüsse_aufs_Tor', 'Fehler_vor_Schuss_Gegentor', 'Geblockte_Bälle', 
        'Gewonnene_Zweikämpfe_Prozent', 'Gewonnene_Zweikämpfe', 'Zweikämpfe', 'Erfolgreiche_Pässe_Prozent', 'Erfolgreiche_Pässe', 'Pässe', 
        'Gewonnene_Luftkämpfe_Prozent', 'Gewonnene_Luftkämpfe', 'Luftkämpfe','Erfolgreiche_Tacklings_Prozent', 'Erfolgreiche_Tacklings', 'Tacklings', 
        'Erfolgreiche_Dribblings_Prozent', 'Erfolgreiche_Dribblings', 'Dribblings', 'Schussgenauigkeit_Prozent', 'Erfolgreiche_Schussgenauigkeit',
        'Schussgenauigkeit', 'Abgwehrte_Schüsse_Prozent', 'Erfolgreiche_Abgwehrte_Schüsse', 'Abgwehrte_Schüsse', 'Elfmeter_Pariert_Prozent', 
        'Elfmeter_Pariert', 'Elfmeter', 'Großchancen_Pariert_Prozent', 'Großchancen_Pariert', 'Großchancen', 'Strafraum_Beherrschung_Prozent',
        'Erfolgreiche_Strafraum_Beherrschung', 'Strafraum_Beherrschung' ,'Paraden', 'Weiße_Weste', 'Woche', 'Jahr', 'Saison']]
        
    return df_staging_ligainsider
    
#df = get_data_ligainsider('2016/17', 8, 1)  
#db.upload_local_db_data(df, 28)  
#type(df.iloc[24,:]['Paraden'])
# f_l = db.get_data_db(8)
# df_staging_ligainsider = f_l.get_data()

# f3 = db.get_data_db(7)
# df_mapping_transfermarkt = f3.get_data()   
# df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']=='2015/16']
# v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[17] 
   


# df_staging_ligainsider = df_staging_ligainsider[df_staging_ligainsider['Saison']=='2015/16'] 
# df_staging_ligainsider = df_staging_ligainsider[df_staging_ligainsider['Vereins_ID']==v1]

# df_staging_ligainsider['Gewonnene_Zweikämpfe_Prozent'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Zweikämpfe'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Gewonnene_Zweikämpfe'] = df_staging_ligainsider['Gewonnene_Zweikämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Erfolgreiche_Pässe_Prozent'] = df_staging_ligainsider['Erfolgreiche_Pässe_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Pässe'] = df_staging_ligainsider['Erfolgreiche_Pässe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Erfolgreiche_Pässe'] = df_staging_ligainsider['Erfolgreiche_Pässe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Gewonnene_Luftkämpfe_Prozent'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Luftkämpfe'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Gewonnene_Luftkämpfe'] = df_staging_ligainsider['Gewonnene_Luftkämpfe_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Erfolgreiche_Tacklings_Prozent'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Tacklings'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Erfolgreiche_Tacklings'] = df_staging_ligainsider['Erfolgreiche_Tacklings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Erfolgreiche_Dribblings_Prozent'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Dribblings'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Erfolgreiche_Dribblings'] = df_staging_ligainsider['Erfolgreiche_Dribblings_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Schussgenauigkeit_Prozent'] = df_staging_ligainsider['Schussgenauigkeit_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Schussgenauigkeit'] = df_staging_ligainsider['Schussgenauigkeit_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Erfolgreiche_Schussgenauigkeit'] = df_staging_ligainsider['Schussgenauigkeit_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Abgwehrte_Schüsse_Prozent'] = df_staging_ligainsider['Abgwehrte_Schüsse_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Abgwehrte_Schüsse'] = df_staging_ligainsider['Abgwehrte_Schüsse_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Erfolgreiche_Abgwehrte_Schüsse'] = df_staging_ligainsider['Abgwehrte_Schüsse_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)


# df_staging_ligainsider['Elfmeter'] = df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)
# df_staging_ligainsider['Elfmeter_Pariert_Prozent'] = df_staging_ligainsider['Elfmeter_Pariert_Prozent'].str.split('%', expand = True)[0].astype(float)
# if len(df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True).columns) > 1:
#     df_staging_ligainsider['Elfmeter_Pariert'] = df_staging_ligainsider['Elfmeter_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# else:
#     df_staging_ligainsider['Elfmeter_Pariert'] = 0    
      
# df_staging_ligainsider['Großchancen_Pariert_Prozent'] = df_staging_ligainsider['Großchancen_Pariert_Prozent'].str.split('%', expand = True)[0].astype(int)
# df_staging_ligainsider['Großchancen'] = df_staging_ligainsider['Großchancen_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
# df_staging_ligainsider['Großchancen_Pariert'] = df_staging_ligainsider['Großchancen_Pariert_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)

# df_staging_ligainsider['Strafraum_Beherrschung_Prozent'] = df_staging_ligainsider['Strafraum_Beherrschung_Prozent'].str.split('%', expand = True)[0].astype(float)
# if len(df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True).columns)>1:
#     df_staging_ligainsider['Strafraum_Beherrschung'] = df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[1].fillna(0).astype(int)
#     df_staging_ligainsider['Erfolgreiche_Strafraum_Beherrschung'] = df_staging_ligainsider['Strafraum_Beherrschung_Absolut'].str.replace('(','').str.replace(')','').str.split('/', expand = True)[0].replace('-',np.nan).fillna(0).astype(int)    
# else:
#     df_staging_ligainsider['Strafraum_Beherrschung'] = 0  
#     df_staging_ligainsider['Erfolgreiche_Strafraum_Beherrschung'] = 0
    
# df_staging_ligainsider = df_staging_ligainsider[[
#     'Spieler_ID','Spieler', 'Vereins_ID', 'Verein','Spieltag', 'Fouls', 'Geklärte_Bälle', 'Abgefangene_Bälle','Ball_Eroberungen', 'Ballverluste',
#     'Torschuss_Vorlagen', 'Kreierte_Großchancen', 'Schüsse_aufs_Tor', 'Fehler_vor_Schuss_Gegentor', 'Geblockte_Bälle', 
#     'Gewonnene_Zweikämpfe_Prozent', 'Gewonnene_Zweikämpfe', 'Zweikämpfe', 'Erfolgreiche_Pässe_Prozent', 'Erfolgreiche_Pässe', 'Pässe', 
#     'Gewonnene_Luftkämpfe_Prozent', 'Gewonnene_Luftkämpfe', 'Luftkämpfe','Erfolgreiche_Tacklings_Prozent', 'Erfolgreiche_Tacklings', 'Tacklings', 
#     'Erfolgreiche_Dribblings_Prozent', 'Erfolgreiche_Dribblings', 'Dribblings', 'Schussgenauigkeit_Prozent', 'Erfolgreiche_Schussgenauigkeit',
#     'Schussgenauigkeit', 'Abgwehrte_Schüsse_Prozent', 'Erfolgreiche_Abgwehrte_Schüsse', 'Abgwehrte_Schüsse', 'Elfmeter_Pariert_Prozent', 
#     'Elfmeter_Pariert', 'Elfmeter', 'Großchancen_Pariert_Prozent', 'Großchancen_Pariert', 'Großchancen', 'Strafraum_Beherrschung_Prozent',
#     'Erfolgreiche_Strafraum_Beherrschung', 'Strafraum_Beherrschung' ,'Paraden', 'Weiße_Weste', 'Woche', 'Jahr', 'Saison']]

# db.upload_local_data_to_database(df_staging_ligainsider, 'bl1_data_spieler_daten')

    
    
    