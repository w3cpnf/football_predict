#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


import Tools as t
import Read_Load_Database as db

class goal_minutes:
    
    def __init__(self, spieltag):

        self.spieltag = spieltag
        
    def get_goal_minutes(self):
        
        s = self.spieltag
        d = db.get_data_db(24)
        df = d.get_data()

        df_all = pd.DataFrame()
        df_1 = df[df['Spieltag']==s] 
        df_1.index = range(len(df_1.index))
        vereine = df_1['Heimmannschaft'].drop_duplicates()
        
        for v in vereine:
            
            df_v = df_1[df_1['Heimmannschaft']==v]
            
            df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft','Ergebnis', 'Jahr', 'Woche', 'Saison']]
            df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft','Ergebnis', 'Jahr', 'Woche', 'Saison']]
            
            heimmannschaft_id = df_h['Heimmannschaft_ID'].iloc[0]
            heimmannschaft = df_h['Heimmannschaft'].iloc[0]
            jahr = df_h['Jahr'].iloc[0]
            woche = df_h['Woche'].iloc[0]
            saison = df_h['Saison'].iloc[0]
            ergebnis = df_h['Ergebnis'].iloc[0]
            
            auswärtsmannschaft_id = df_a['Auswärtsmannschaft_ID'].iloc[0]
            auswärtsmannschaft = df_a['Auswärtsmannschaft'].iloc[0]
            
            
            df_h[['Tore', 'Gegentore']] = df_h['Ergebnis'].str.split(':', expand = True)
            df_a[['Gegentore', 'Tore']] = df_a['Ergebnis'].str.split(':', expand = True) 
            
            tore_heim = int(df_h['Tore'].iloc[0])
            tore_auswärts = int(df_a['Tore'].iloc[0])
            
            df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
            df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
            

            
            
            driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
            driver.get('http://www.google.com')
            
            query = 'bundesliga ergebnisse Saison 2019/20 '+ str(v) + ' ' + str(s) + ' Spieltag'
            #query = 'bundesliga ergebnisse '+ str(v) + ' ' + str(s) + ' Spieltag'
            search = driver.find_element_by_name('q')
            search.send_keys(query)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
            element.click()
            time.sleep(3)
            #maker = driver.find_elements_by_xpath("//div[@class='imso_gs__gs-r']")
            minutes = driver.find_elements_by_xpath("//span[@class='imso_gs__g-a-t']")
            
            df_done = pd.DataFrame()
            
            if len(minutes)==0:
                
                df_dh = df_h.assign(Gegner_ID = auswärtsmannschaft_id, 
                                      Gegner = auswärtsmannschaft,
                                      Minutes = 0, Heim = 1) 
                df_dh = df_dh.rename(columns={"Heimmannschaft_ID": "Vereins_ID", "Heimmannschaft": "Verein"})
                
                df_da = df_a.assign(Gegner_ID = heimmannschaft_id, 
                                      Gegner = heimmannschaft,
                                      Minutes = 0, Heim = 0) 
                
                df_dh = df_dh.rename(columns={"Heimmannschaft_ID": "Vereins_ID", "Heimmannschaft": "Verein"})
                df_da = df_da.rename(columns={"Auswärtsmannschaft_ID": "Vereins_ID", "Auswärtsmannschaft": "Verein"})
                                     
                df_done = df_dh.append(df_da)
                df_done = df_done[['Minutes', 'Vereins_ID', 'Verein', 'Gegner_ID', 'Gegner', 'Ergebnis',
                                   'Saison', 'Heim', 'Jahr', 'Woche']]
             
                df_all = df_all.append(df_done)
                
                
            else:
                f = t.get_df(minutes)
                df_minutes = f.df() 
                driver.quit()
                
                df_minutes = df_minutes[0].str.split('\'', expand = True)
                df_minutes = df_minutes.dropna()
                df_minutes = df_minutes[[0]]
                
                df_minutes.columns = ['Minutes']
                
                
                
                if tore_heim > 0 and tore_auswärts > 0:
                    
                    
                    df_minutes_home = df_minutes.iloc[0:tore_heim]
                    df_minutes_auswärts = df_minutes.iloc[tore_heim:tore_heim+tore_auswärts]
                    
                    df_minutes_home = df_minutes_home.assign(Vereins_ID = heimmannschaft_id, 
                                                             Verein = heimmannschaft, 
                                                             Gegner_ID = auswärtsmannschaft_id,
                                                             Gegner = auswärtsmannschaft,
                                                             Ergebnis = ergebnis, Saison = saison, Heim = 1, 
                                                             Jahr = jahr, Woche = woche)
                    
                    df_minutes_auswärts = df_minutes_auswärts.assign(Vereins_ID = auswärtsmannschaft_id, 
                                                             Verein = auswärtsmannschaft, 
                                                             Gegner_ID = heimmannschaft_id,
                                                             Gegner = heimmannschaft,
                                                             Ergebnis = ergebnis, Heim = 0, Saison = saison,
                                                             Jahr = jahr, Woche = woche)  
                    
                    df_done = df_minutes_home.append(df_minutes_auswärts)
                    df_all = df_all.append(df_done)

                    
                if tore_heim > 0 and tore_auswärts == 0:
                    df_minutes_home = df_minutes.iloc[0:tore_heim]
                    
                    df_minutes_home = df_minutes_home.assign(Vereins_ID = heimmannschaft_id, 
                                                             Verein = heimmannschaft, 
                                                             Gegner_ID = auswärtsmannschaft_id,
                                                             Gegner = auswärtsmannschaft,
                                                             Ergebnis = ergebnis, Heim = 1, Saison = saison,
                                                             Jahr = jahr, Woche = woche)
                    
                    df_da = df_a.assign(Gegner_ID = heimmannschaft_id, 
                                      Gegner = heimmannschaft,
                                      Minutes = 0, Heim = 0) 
                    df_da = df_da[['Minutes', 'Vereins_ID', 'Verein', 'Gegner_ID', 'Gegner', 'Ergebnis',
                                   'Saison', 'Heim', 'Jahr', 'Woche']]
                    df_done = df_minutes_home.append(df_da)
                    df_all = df_all.append(df_done)
                    
                   
                
                if tore_auswärts > 0 and tore_heim == 0:
                    df_minutes_auswärts = df_minutes.iloc[0:tore_auswärts]
                    df_minutes_auswärts = df_minutes_auswärts.assign(Vereins_ID = auswärtsmannschaft_id, 
                                                             Verein = auswärtsmannschaft, 
                                                             Gegner_ID = heimmannschaft_id,
                                                             Gegner = heimmannschaft,
                                                             Ergebnis = ergebnis, Heim = 0, Saison = saison,
                                                             Jahr = jahr, Woche = woche) 
                    
                    df_dh = df_h.assign(Gegner_ID = auswärtsmannschaft_id, 
                                      Gegner = auswärtsmannschaft,
                                      Minutes = 0, Heim = 1) 
                    df_dh = df_dh[['Minutes', 'Vereins_ID', 'Verein', 'Gegner_ID', 'Gegner', 'Ergebnis',
                                   'Saison', 'Heim', 'Jahr', 'Woche']]
                    df_done = df_minutes_auswärts.append(df_dh)
                    df_all = df_all.append(df_done)
                    df_all = df_all.append(df_minutes_auswärts)
                    
                
                
                
            df_all = df_all.assign(Spieltag = s)
            df_all = df_all[['Vereins_ID', 'Verein', 'Gegner_ID', 'Gegner', 'Spieltag', 'Ergebnis', 'Minutes', 'Heim', 'Jahr', 'Woche', 'Saison']]
        return df_all

def check_df(df):
    vereine = df['Vereins_ID'].drop_duplicates()
    if len(vereine) == 18:
        print('Done')
    else:
        print("Problem with Nbr of clubs")


f = goal_minutes(1)
df = f.get_goal_minutes()

check_df(df)
#df = df.assign(Spieltag = 1)


import mysql
import mysql.connector

def upload_local_db_data(df, query):
        
    if query == 1:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_tore_minute (Vereins_ID, Verein, Gegner_ID, Gegner, Spieltag, Ergebnis, Minutes,
                                Heim, Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                                                                                          
                               
    mydb = mysql.connector.connect(
         host = 'localhost',
         user = 'root',
         passwd="Teleshop,1871",
         database = 'bl1_daten'
     )
    cursor = mydb.cursor()
    cursor.executemany(mySql_insert_query, upload)
    mydb.commit()
    mydb.close()

#upload_local_db_data(df,1)