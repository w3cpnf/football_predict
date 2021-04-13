import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

import Read_Load_Database as db
import My_Tools as t


def get_verletzungen(saison, transferfenster, c):
    
    f1 = db.get_data_db(27)
    df_mapping_transfermarkt = f1.get_data()
    id_Verein = df_mapping_transfermarkt['Vereins_ID']
    v1 = id_Verein.iloc[c-1]
    
    f2 = db.get_data_db(4)
    df_url = f2.get_data()    
    
    df = df_url[df_url['Saison']==saison]
    df = df[df['Vereins_ID']==v1]
    df = df[df['Transferfenster']==transferfenster]
    
    url = df['Url'].drop_duplicates()
    
    df_all = pd.DataFrame()
    
    for u in url:    
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        page = u +'krankenakte/'
        driver.get(page)
        time.sleep(1)
        try:
            #verletzungen_button = driver.find_element_by_xpath("//a[contains(text(), 'Krankenakte')]")
            #verletzungen_button.click()
            #time.sleep(1)
            verletzungen = driver.find_elements_by_xpath("//div[@class='sick_acts_row']")

            l_verletzungen = t.get_list(verletzungen)
            df_verletzungen = pd.DataFrame(l_verletzungen)

            if len(df_verletzungen)>0:
                df_verletzungen = df_verletzungen[0].str.split('\n', expand = True)
                df_verletzungen.columns = ['Art', 'Saison','Datum', 'Fehlzeit', 'Verpasste_Spielzeit']
                df_verletzungen = df_verletzungen.dropna()
                df_verletzungen = df_verletzungen.assign(Url = u)
                df_all = df_all.append(df_verletzungen)

                driver.quit()
            else:                
                driver.quit()
            
        except NoSuchElementException as v:          
            print(v)
            driver.quit()
        except ValueError as v:          
            print(v)
            driver.quit()
    
    
    if len(df_all)>0:
        df_all = df_all.merge(df, on = 'Url', how = 'inner')
        df_all = df_all.drop(['Url'], axis = 1 ) 
        
        
    return df_all


def prep_ver_upload(df):
    df = df.drop_duplicates()

    aktuel = df[df['Datum'].str.contains('seit')==True]
    vergangen = df[df['Datum'].str.contains('seit')!=True]
    
    if len(aktuel)>0:
        vergangen[['Von', 'Bis']] = vergangen['Datum'].str.split('-', expand = True)
        aktuel[['seit', 'Von']] = aktuel['Datum'].str.split(' ', expand = True)
        aktuel = aktuel.drop(['seit'], axis = 1)
        aktuel = aktuel.assign(Bis = 0, Aktuelle_Verletzung = 1)
        vergangen = vergangen.assign(Aktuelle_Verletzung = 0)
        vergangen['Von'] = pd.to_datetime(vergangen['Von'],  infer_datetime_format=True).dt.date
        vergangen['Bis'] = pd.to_datetime(vergangen['Bis'],  infer_datetime_format=True).dt.date
        aktuel['Von'] = pd.to_datetime(aktuel['Von'],  infer_datetime_format=True).dt.date
        df_c = vergangen.append(aktuel, ignore_index=True)
        
    else:
        vergangen[['Von', 'Bis']] = vergangen['Datum'].str.split('-', expand = True)
        vergangen = vergangen.assign(Aktuelle_Verletzung = 0)
        vergangen['Von'] = pd.to_datetime(vergangen['Von'],  infer_datetime_format=True).dt.date
        vergangen['Bis'] = pd.to_datetime(vergangen['Bis'],  infer_datetime_format=True).dt.date 
        df_c = vergangen
        
    df_c['Verpasste_Spielzeit'] = df_c['Verpasste_Spielzeit'].astype(int)
    df_c = df_c[['Spieler_ID', 'Spieler', 'Aktuelle_Verletzung', 'Art', 'Von', 'Bis', 'Fehlzeit', 'Verpasste_Spielzeit']]

    return df_c


def get_injuries_data_format(saison, transferfenster, c):

    f1 = db.get_data_db(7)
    df_mapping_transfermarkt = f1.get_data()
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    
    v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[c-1]
    verein = df_mapping_transfermarkt['Verein'].iloc[c-1]

    f3 = db.get_data_db(2)
    df_spielplan = f3.get_data()
    df_spielplan = df_spielplan[df_spielplan['Saison']==saison]
    
    f4 = db.get_data_db(6)
    df_verletzt = f4.get_data()
    df_spielplan = df_spielplan[df_spielplan['Vereins_ID']==v1]
    
    f5 = db.get_data_db(12)
    df_kader = f5.get_data()
    df_kader = df_kader[df_kader['Saison']==saison]
    df_kader = df_kader[df_kader['Vereins_ID']==v1]
    df_kader = df_kader[df_kader['Transferfenster']==transferfenster]
    df_kader = df_kader[['Spieler_ID']]

    df_verletzt = df_verletzt.merge(df_kader, on = 'Spieler_ID', how = 'inner')

    df_all = pd.DataFrame()
    
    spieltage = df_spielplan['Spieltag'].drop_duplicates()
    
    for s in spieltage:
        relevant_datum = df_spielplan[df_spielplan['Spieltag']==s]['Datum'].iloc[0]
        relevant_datum = relevant_datum.to_pydatetime()
        
        spieler = df_verletzt['Spieler_ID'].drop_duplicates()
        
        for sp in spieler:
            df_spieler_verletzt = df_verletzt[df_verletzt['Spieler_ID'] == sp]
            l_spieler = len(df_spieler_verletzt)
            
            for i in range(l_spieler):
                einzelne_verletzung = df_spieler_verletzt.iloc[i,:]
                
                
                if (einzelne_verletzung['Von']<relevant_datum and (einzelne_verletzung['Bis']>relevant_datum or einzelne_verletzung['Bis']=='')):
                    df_einzelne_verletzung = pd.DataFrame(einzelne_verletzung).T
    
                    df_einzelne_verletzung = df_einzelne_verletzung.assign(Spieltag = s, Saison = saison, 
                                                                           Vereins_ID = v1, Verein = verein, 
                                                                           Transferfenster = transferfenster, Datum = relevant_datum)
                    df_all = df_all.append(df_einzelne_verletzung)
    
    df_all['Spieler_ID'] = df_all['Spieler_ID'].astype(int)
    df_all = df_all[['Spieltag', 'Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Datum', 'Von', 'Bis', 'Saison']]
    df_all = df_all.drop_duplicates(['Spieler', 'Spieler_ID', 'Saison', 'Spieltag'])
    f6 = db.get_data_db(15)
    df_v = f6.get_data()

    df_v = df_v[df_v['Saison']==saison]
    df_v = df_v[df_v['Vereins_ID']==v1]
    
    df_rest = df_all.merge(df_v, on = ['Spieler', 'Spieler_ID', 'Saison', 'Spieltag', 'Vereins_ID', 'Verein', 'Datum', 'Von', 'Bis'
                                       ], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    
    df_rest = df_rest.drop('_merge', axis = 1)
    #print(df_rest)
    return df_rest

