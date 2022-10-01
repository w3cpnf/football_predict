import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db
import numpy as np
from sklearn.feature_selection import SelectFromModel
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
df_startelf_kicker = db.get_startelf_grades()
df_startelf_kicker.columns
#df_startelf_kicker_saison = df_startelf_kicker[df_startelf_kicker['saison']=='2021/22']
#df_startelf_kicker_verein = df_startelf_kicker_saison[df_startelf_kicker_saison['Vereins_ID']==1]
#df_startelf_kicker_spieltag = df_startelf_kicker_verein[df_startelf_kicker_verein['Spieler_1']==873]
#df_startelf_kicker_spieltag = df_startelf_kicker_spieltag.assign(Konstanz_Note = 0)
#df_startelf_kicker_spieltag.iloc[0:10,6]

from selenium.webdriver.chrome.service import Service



def get_average_constant_performance(df):

    df_all = pd.DataFrame()
    for saison in df_startelf_kicker['saison'].drop_duplicates():
        df_startelf_kicker_saison = df_startelf_kicker[df_startelf_kicker['saison']==saison]
        
        for verein in df_startelf_kicker_saison['Vereins_ID'].drop_duplicates():
            df_startelf_kicker_verein = df_startelf_kicker_saison[df_startelf_kicker_saison['Vereins_ID']==verein]
            
            for spieler in df_startelf_kicker_verein['Spieler_1'].drop_duplicates():
                
                df_spieler = df_startelf_kicker_verein[df_startelf_kicker_verein['Spieler_1']==spieler]
                df_spieler = df_spieler.sort_values('spieltag')
                df_spieler = df_spieler.assign(Durchschnitt_Note = 0, Konstanz_Note = 0, Form_Note = 0)
                
                if len(df_spieler)>1:
                    for games in range(len(df_spieler)):
                        if games == 0:
                            df_spieler.iloc[games, 7] = df_spieler.iloc[games, 6]
                            df_spieler.iloc[games, 8] = np.std(df_spieler.iloc[games, 6])
                            df_spieler.iloc[games, 9] = df_spieler.iloc[games, 6]
                        if games == 1:
                            df_spieler.iloc[games, 7] = round(sum(df_spieler.iloc[0:games+1, 6])/(games + 1), 2)
                            df_spieler.iloc[games, 8] = round(np.std(df_spieler.iloc[0:games+1, 6]), 2)
                            df_spieler.iloc[games, 9] =  round(sum(df_spieler.iloc[0:games+1, 6])/(games + 1), 2)
                        if games == 2:
                            df_spieler.iloc[games, 7] = round(sum(df_spieler.iloc[0:games+1, 6])/(games + 1), 2)
                            df_spieler.iloc[games, 8] = round(np.std(df_spieler.iloc[0:games+1, 6]), 2)
                            df_spieler.iloc[games, 9] =  round(sum(df_spieler.iloc[0:games+1, 6])/(games + 1), 2)
                        if games > 2:
                            df_spieler.iloc[games, 7] = round(sum(df_spieler.iloc[0:games+1, 6])/(games + 1), 2)
                            df_spieler.iloc[games, 8] = round(np.std(df_spieler.iloc[0:games+1, 6]), 2)
                            df_spieler.iloc[games, 9] =  round(sum(df_spieler.iloc[games-3:games+1, 6])/(games + 1), 2)
                
                else:
                    df_spieler.iloc[0, 7] = df_spieler.iloc[0, 6]
                    
                df_all = df_all.append(df_spieler)
                
    return df_all
    
#df_average_constant_performance = get_average_constant_performance(df_startelf_kicker)
#db.upload_local_data_to_database(df_average_constant_performance, 'bl1_data_kicker_features')   

#df_kicker_features = db.get_table('bl1_data_kicker_features')

def get_kicker_forecast_features(df):
    df_all = pd.DataFrame()
    for saison in df['saison'].drop_duplicates():
        df_saison = df[df['saison']==saison]    
        df_1 = df_saison[df_saison['spieltag']==1]    
        df_saison['spieltag'] = df_saison['spieltag'].add(1)
        df_saison = df_saison[df_saison['spieltag']!=35]
        df_saison = pd.concat([df_1, df_saison], axis = 0)
        df_all = df_all.append(df_saison)
    return df_all
    
#df_kicker_forecast = get_kicker_forecast_features(df_kicker_features)    
#db.upload_local_data_to_database(df_kicker_forecast, 'bl1_feature_kicker_performance')    

def get_order_id(saison, vereins_id):
    df_mapping_transfermarkt = db.get_table('bl1_mapping_transfermarkt')
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    df_mapping_transfermarkt.index = range(len(df_mapping_transfermarkt))
    v_id = df_mapping_transfermarkt[df_mapping_transfermarkt['Vereins_ID']==vereins_id]
    index_nbr = int(v_id.index.tolist()[0])+1
    return index_nbr

def get_kicker(spieltag, saison, c):
        
    s1 = saison[0:4]+'-'+saison[5:7]
    
    df_mapping_transfermarkt = db.get_table('bl1_mapping_transfermarkt')
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    print(df_mapping_transfermarkt)
    id_Verein = df_mapping_transfermarkt['Vereins_ID']
    v1 = id_Verein.iloc[c-1]

    df = db.get_table('bl1_data_vereine_spielplan')
    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]   
    
    df_mapping_kicker = db.get_table('bl1_mapping_kicker')

    df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Saison']==saison]
    df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Vereins_ID']==v1]
    
    v = df_mapping_kicker['Webpage'].iloc[0]
    verein = df_mapping_kicker['Verein'].iloc[0]


    url = 'https://www.kicker.de/1-bundesliga/'+str(v)+'/topspieler-spieltag/'+str(s1)+'/'+str(spieltag)

    driver = webdriver.Chrome(service=Service('D:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe'))
    #driver = webdriver.Firefox(executable_path=r'C:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    #driver = webdriver.Chrome(executable_path=r"D:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe")
    driver.get(url)

    time.sleep(5)
    name = driver.find_elements("xpath", "//td[@class='kick__table--ranking__index kick__table--ranking__index--teamplayer']")
    position = driver.find_elements("xpath", "//td[@class='kick__table--ranking__number kick__respt-m-w-100']")
    note = driver.find_elements("xpath", "//td[@class='kick__table--ranking__master kick__respt-m-w-65 kick__table--ranking__mark']")
    #name = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__index kick__table--ranking__index--teamplayer']")    
    #position = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__number kick__respt-m-w-100']")
    #note = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__master kick__respt-m-w-65 kick__table--ranking__mark']")
               
    f1 = t.get_df(name)
    f2 = t.get_df(position)
    f3 = t.get_df(note)

    df_name = f1.df()           
    df_position = f2.df()
    df_note = f3.df()
    
    driver.quit()   
    
    df_name = df_name.fillna('')
    df_name['Spieler'] = df_name[1] + ' ' + df_name[0]
    df_name = df_name.drop([0,1], axis = 1)
    df_position.columns = ['Position']
    df_note.columns = ['Note']
    
    df_all  = pd.concat([df_name, df_position, df_note], axis = 1)

    f4 = t.unify_letters(df_all,1)
    df_all = f4.replace_letters()
    df_all['Spieler'] = df_all['Spieler'].str.strip()

    df_all = t.replace_kicker_names(df_all)
    df_all = df_all.assign(Spieltag = spieltag)
    

    df_spieler_config = db.get_table('bl1_staging_spieler_kader')
    df_spieler_config = df_spieler_config[df_spieler_config['Saison']==saison]
    df_spieler_config = df_spieler_config[df_spieler_config['Vereins_ID']==v1]
    df_spieler_config = df_spieler_config.drop('Position', axis = 1)
    print(df_all['Spieler'].iloc[4])
    df_a = df_all.merge(df_spieler_config, on = ['Spieler'], how = 'inner')
    
    df_a['Note'] = df_a['Note'].str.replace(",",".").astype(float)  
    df_a = df_a.assign(Verein = verein)

    df_a = df_a[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note', 'Saison']]
    df_a = df_a.drop_duplicates()
    print(df_a['Spieler'])
    #print(df_spieler_config['Spieler'].drop_duplicates())
    mistake = t.get_outer_on_player(df_a, df_spieler_config)

    if len(df_a)==len(df_all):
        print('Everthing fine')
    else:
        print(mistake)
        print(str(v))

    return df_a 

spieltag = 27
vereins_id_database = 10
verein = get_order_id('2021/22', vereins_id_database)

df = get_kicker(spieltag, '2021/22', verein)
db.delete_matchday_club('bl1_data_spieler_kicker_position', "'2021/22'", str(spieltag), str(vereins_id_database))
db.upload_local_data_to_database(df, 'bl1_data_spieler_kicker_position')


def get_kicker_all(saison, c):
    
    df_complete = pd.DataFrame()
    
    for spieltag in range(1,34):
        
        s1 = saison[0:4]+'-'+saison[5:7]
        
        df_mapping_transfermarkt = db.get_table('bl1_mapping_transfermarkt')
        #print(df_mapping_transfermarkt)
        df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
        id_Verein = df_mapping_transfermarkt['Vereins_ID']
        v1 = id_Verein.iloc[c-1]
    
        df = db.get_table('bl1_data_vereine_spielplan')
        df = df[df['Saison']==saison]
        df = df[df['Spieltag']==spieltag]   
        #print(df)
        df_mapping_kicker = db.get_table('bl1_mapping_kicker')
        #print(df_mapping_kicker)
        df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Saison']==saison]
        df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Vereins_ID']==v1]
        
        v = df_mapping_kicker['Webpage'].iloc[0]
        verein = df_mapping_kicker['Verein'].iloc[0]
    
     
        #driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver = webdriver.Chrome(service=Service('C:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe'))
        url = 'https://www.kicker.de/1-bundesliga/'+str(v)+'/topspieler-spieltag/'+str(s1)+'/'+str(spieltag)
        

        driver.get(url)
        #time.sleep(5)
        #print(driver.find_element(By.XPATH, '//div[@class="sc-gsDKAQ kMbmJI"]'))
        #driver.find_element_by_class_name("sc-gsDKAQ kMbmJI").click()
        #if driver.find_element(By.XPATH, '//button[@data-testid="uc-accept-all-button"]') != 0:
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[@id="cmpbntyestxt"]'))).click()
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-testid="uc-accept-all-button"]'))).click()
        time.sleep(2)   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        name = driver.find_elements("xpath", "//td[@class='kick__table--ranking__index kick__table--ranking__index--teamplayer']")
        position = driver.find_elements("xpath", "//td[@class='kick__table--ranking__number kick__respt-m-w-100']")
        note = driver.find_elements("xpath", "//td[@class='kick__table--ranking__master kick__respt-m-w-65 kick__table--ranking__mark']")
                   
        f1 = t.get_df(name)
        f2 = t.get_df(position)
        f3 = t.get_df(note)
    
        df_name = f1.df()           
        df_position = f2.df()
        df_note = f3.df()
        
        driver.quit()   
        
        df_name = df_name.fillna('')
        df_name['Spieler'] = df_name[1] + ' ' + df_name[0]
        df_name = df_name.drop([0,1], axis = 1)
        df_position.columns = ['Position']
        df_note.columns = ['Note']
        
        df_all  = pd.concat([df_name, df_position, df_note], axis = 1)
    
        f4 = t.unify_letters(df_all,1)
        df_all = f4.replace_letters()
        df_all = t.replace_kicker_names(df_all)
        df_all = df_all.assign(Spieltag = spieltag)
    
        df_spieler_config = db.get_table('bl1_staging_spieler_kader')
        df_spieler_config = df_spieler_config[df_spieler_config['Saison']==saison]
        df_spieler_config = df_spieler_config[df_spieler_config['Vereins_ID']==v1]
        #df_spieler_config = df_spieler_config[df_spieler_config['Spieltag']==spieltag]
        df_spieler_config = df_spieler_config.drop('Position', axis = 1)
        df_a = df_all.merge(df_spieler_config, on = ['Spieler'], how = 'inner')
        
        df_a['Note'] = df_a['Note'].str.replace(",",".").astype(float)  
        df_a = df_a.assign(Verein = verein)
    
        df_a = df_a[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note', 'Saison']]
        df_a = df_a.drop_duplicates()
        
        mistake = t.get_outer_on_player(df_a, df_spieler_config)
        print(df_a.merge(df_spieler_config, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']['Spieler'])
        if len(df_a)==len(df_all):
            print('Everthing fine')
        else:
            print(mistake)
            print(str(v))
        
        df_complete = df_complete.append(df_a)
        
    return df_complete 

#df = get_kicker_all('2020/21', 3)

#db.upload_local_data_to_database(df, 'bl1_data_spieler_kicker_position')
#db.upload_local_db_data(df, 9)
# f = db.get_data_db(19)
# df = f.get_data()
# df = df[df['Saison']=='2019/20']
# df = df.drop_duplicates()



 



#driver = webdriver.Chrome(service=Service('C:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe'))
#url = 'https://www.kicker.de/bundesliga/fc-schalke-04/topspieler-spieltag/2020-21/1'


#driver.get(url)
#time.sleep(5)
#print(driver.find_element(By.XPATH, '//div[@class="sc-gsDKAQ kMbmJI"]'))
#driver.find_element_by_class_name("sc-gsDKAQ kMbmJI").click()
#if driver.find_element(By.XPATH, '//button[@data-testid="uc-accept-all-button"]') != 0:
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[@id="cmpbntyestxt"]'))).click()
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-testid="uc-accept-all-button"]'))).click()
#test = driver.find_elements(By.XPATH, "button[contains(text(), 'Alles akzeptieren')] and @tabindex='-1'") 

#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Alles akzeptieren'])[@tabindex=-1]"))).click()


#test = driver.find_elements("xpath", "(//button[@data-testid = 'uc-accept-all-button'])[@tabindex = -1]")

#driver.find_element("link text", "Alles akzeptieren").click();