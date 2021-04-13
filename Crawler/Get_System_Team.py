import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

#import other files 
import My_Tools as t 
import Read_Load_Database as db


def get_system():
    f1 = db.get_data_db(41)
    df_plan = f1.get_data()
    
    f2 = db.get_data_db(30)
    df_kader = f2.get_data()
    
    f3 = db.get_data_db(42)
    df_gegner = f3.get_data()
    
    
    saison = '2014/15'
    spieltag = 1
    club_id = 7
    transferfenster = 1
    
    df_plan = df_plan[df_plan['Saison']==saison]
    df_plan = df_plan[df_plan['Spieltag']==spieltag]
    df_plan = df_plan[df_plan['Vereins_ID']==club_id]
    
    df_gegner = df_gegner[df_gegner['Saison']==saison]
    df_gegner = df_gegner[df_gegner['Spieltag']==spieltag]
    df_gegner = df_gegner[df_gegner['Vereins_ID']==club_id]
    
    df_kader = df_kader[df_kader['Saison']==saison]
    df_kader = df_kader[df_kader['Transferfenster']==transferfenster]
    df_kader = df_kader[['Verein', 'Vereins_ID', 'Spieler_ID', 'Spieler_ID', 'Saison']]
    
    month = df_plan['Datum'].iloc[0].month
    day =  df_plan['Datum'].iloc[0].day
    year =  df_plan['Datum'].iloc[0].year
    club = df_plan['Verein'].iloc[0]
    
    club_gegner = df_gegner['Gegner'].iloc[0]
    club_gegner_id = df_gegner['Gegner_ID'].iloc[0]
    
    df_kader_verein = df_kader[df_kader['Vereins_ID']==club_id]
    df_kader_gegner = df_kader[df_kader['Vereins_ID']==club_gegner_id]
    
    
    driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
    driver.get('http://www.google.com')
          
    query = 'bundesliga ergebnisse ' + str(day) + '.' +str(month) + '.' + str(year) + ' ' + str(club)
        
    search = driver.find_element_by_name('q')
    search.send_keys(query)
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
    element.click()
    time.sleep(5)
    #element_1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tb_sh')))
    element_1 = driver.find_elements_by_xpath("//li[@class='imso-hide-overflow tb_l GSkImd']")
    
    element_1[8].click()
    #ActionChains(driver).click(element_1[2]).perform()
    
    time.sleep(5)
    start_aufstellung = driver.find_elements_by_xpath("//div[@class='lr-vl-ls']")
    l_start_aufstellung_h = []
    l_start_aufstellung_a = []
    l_start_auswechseln_h = []
    l_start_auswechseln_a = []
    l_system_h = []
    l_system_a = []
    
    l_start_aufstellung_h.append(start_aufstellung[0].text)
    l_start_aufstellung_a.append(start_aufstellung[1].text)
    
    
    auswechsler_heim = driver.find_elements_by_xpath("//td[@class='lr-imso-ls-ftnc lr-imso-ls-lt']")
    auswechsler_auswärts = driver.find_elements_by_xpath("//td[@class='lr-imso-ls-stnc lr-imso-ls-rt']")
    
    n_h = len(auswechsler_heim)
    
    for i in range(0,n_h):
        l_start_auswechseln_h.append(auswechsler_heim[i].text)
        
    n_a = len(auswechsler_auswärts)
    
    for x in range(0,n_a):
        l_start_auswechseln_a.append(auswechsler_auswärts[x].text)
    
           
    systeme = driver.find_elements_by_xpath("//span[@class='lrvl-tvc lrvl-f']") 
    
    l_system_h.append(systeme[0].text)
    l_system_a.append(systeme[1].text)
    
    driver.quit()
    
    df_start_h = pd.DataFrame(l_start_aufstellung_h)
    df_start_a = pd.DataFrame(l_start_aufstellung_a)
    df_auswechseln_h = pd.DataFrame(l_start_auswechseln_h)
    df_auswechseln_a = pd.DataFrame(l_start_auswechseln_a)
    df_system_h = pd.DataFrame(l_system_h)
    df_system_a = pd.DataFrame(l_system_a)
    
    end_1 = len(df_start_h[0].str.split('\n', expand = True).columns)-1
    end_2 = len(df_start_a[0].str.split('\n', expand = True).columns)-1
    
    start_elf_heim = df_start_h[0].str.split('\n', expand = True).T.drop([0,2,4,6,8,10,12,14,16,18, end_1-1], axis = 0)[0].str.split('.', expand = True)[1]        
    start_elf_auswärts = df_start_a[0].str.split('\n', expand = True).T.drop([0,2,4,6,8,10,12,14,16,18, end_2-1], axis = 0)[0].str.split('.', expand = True)[1]
    
    df_start_elf_heim = pd.DataFrame(start_elf_heim)
    df_start_elf_auswärts = pd.DataFrame(start_elf_auswärts)
    df_start_elf_heim.columns = ['Spieler']
    df_start_elf_auswärts.columns = ['Spieler']
    
    auswechseln_h = df_auswechseln_h[0].str.split(' ', expand = True)[1]
    auswechseln_a = df_auswechseln_a[0].str.split(' ', expand = True)[1]
    df_auswechseln_h = pd.DataFrame(auswechseln_h)
    df_auswechseln_a = pd.DataFrame(auswechseln_a)
    
    
    system_h = str(df_system_h.iloc[0,0])
    system_a = str(df_system_a.iloc[0,0])
    
    df_auswechseln_h.columns = ['Spieler']
    df_auswechseln_a.columns = ['Spieler']
    
    f4 = t.unify_letters(df_auswechseln_h, 1)
    f5 = t.unify_letters(df_auswechseln_a, 1)
    df_auswechseln_h = f4.replace_letters()
    df_auswechseln_a = f5.replace_letters()
    
    
    df_auswechseln_heim = df_auswechseln_h.merge(df_kader_verein, on = 'Spieler', how = 'inner')
    df_auswechseln_auswärts = df_auswechseln_a.merge(df_kader_gegner, on = 'Spieler', how = 'inner')
    df_auswechseln_heim = df_auswechseln_heim.assign(Startelf = 0)
    df_auswechseln_auswärts = df_auswechseln_auswärts.assign(Startelf = 0)
    
    df_start_heim = df_spieler_h.merge(df_kader_verein, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only'] 
    df_start_heim = df_start_heim.drop(columns = ['_merge'], axis = 1)
    df_start_heim = df_start_heim.assign(Startelf = 1)
    
    df_start_auswärts = df_spieler_a.merge(df_kader_gegner, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    df_start_auswärts = df_start_auswärts.drop(columns = ['_merge'], axis = 1)
    df_start_auswärts = df_start_auswärts.assign(Startelf = 1)
    
    actually_played_h = df_start_heim.append(df_auswechseln_heim)
    actually_played_a = df_start_auswärts.append(df_auswechseln_auswärts)
    
    actually_played_h = actually_played_h.assign(System = system_h)
    actually_played_a = actually_played_a.assign(System = system_a)
    
    all_player = actually_played_h.append(actually_played_a)
    
    df_all = df_all.append(all_player)
    
    df_all = df_all[['Vereins_ID', 'Verein', 'Spieler_ID', 'Spieler', 'Spieltag', 'Startelf', 'System', 'Jahr', 'Woche', 'Saison']]













def get_system_aufstellung():
    
    f1 = db.get_data_db(12)
    df_ergebnisse = f1.get_data()
    
    f2 = db.get_data_db(32)
    df_spieler = f2.get_data()
    
    f3 = db.get_data_db(32)
    df_date = f3.get_data()
    
    s = 1
    
    df_all = pd.DataFrame()

    df_2 = df_ergebnisse[df_ergebnisse['Spieltag']==s] 
    df_2.index = range(len(df_2.index))
    
    vereine = df_2['Heimmannschaft'].drop_duplicates()
    
    df_d = df_date[df_date['Spieltag']==s]
    
    df_3 = df_spieler[df_spieler['Spieltag']==s]
    
    for v in vereine:
        
        df_da = df_d[df_d['Verein']==v]
        month = df_da['Datum'].iloc[0].month
        day =  df_da['Datum'].iloc[0].day
        df_v = df_2[df_2['Heimmannschaft']==v]
        
        df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft','Jahr', 'Woche', 'Saison']]
        df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Jahr', 'Woche', 'Saison']]
        
        heimmannschaft_spieler = df_v['Heimmannschaft'].iloc[0]
        auswärtsmannschaft_spieler = df_v['Auswärtsmannschaft'].iloc[0]
        
                  
        df_spieler_h = df_3[df_3['Verein']==heimmannschaft_spieler]
        df_spieler_a = df_3[df_3['Verein']==auswärtsmannschaft_spieler]
        
        df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
        df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
        
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        driver.get('http://www.google.com')
              
        query = 'bundesliga ergebnisse ' + str(day) +'.'+str(month)+ ' ' + str(v)
            
        search = driver.find_element_by_name('q')
        search.send_keys(query)
        time.sleep(3)
        search.send_keys(Keys.RETURN)
        
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
        element.click()
        time.sleep(5)
        #element_1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tb_sh')))
        element_1 = driver.find_elements_by_xpath("//li[@class='imso-hide-overflow tb_l GSkImd']")
        element_1[7].click()
        ActionChains(driver).click(element_1[2]).perform()
        
        time.sleep(5)
        start_aufstellung = driver.find_elements_by_xpath("//div[@class='lr-vl-ls']")
        l_start_aufstellung_h = []
        l_start_aufstellung_a = []
        l_start_auswechseln_h = []
        l_start_auswechseln_a = []
        l_system_h = []
        l_system_a = []
        
        l_start_aufstellung_h.append(start_aufstellung[0].text)
        l_start_aufstellung_a.append(start_aufstellung[1].text)
        
        
        auswechsler_heim = driver.find_elements_by_xpath("//td[@class='lr-imso-ls-ftnc lr-imso-ls-lt']")
        auswechsler_auswärts = driver.find_elements_by_xpath("//td[@class='lr-imso-ls-stnc lr-imso-ls-rt']")
        
        n_h = len(auswechsler_heim)
        
        for i in range(0,n_h):
            l_start_auswechseln_h.append(auswechsler_heim[i].text)
            
        n_a = len(auswechsler_auswärts)
        
        for x in range(0,n_a):
            l_start_auswechseln_a.append(auswechsler_auswärts[x].text)
        
               
        systeme = driver.find_elements_by_xpath("//span[@class='lrvl-tvc lrvl-f']") 

        l_system_h.append(systeme[0].text)
        l_system_a.append(systeme[1].text)
        
        driver.quit()
        
        df_start_h = pd.DataFrame(l_start_aufstellung_h)
        df_start_a = pd.DataFrame(l_start_aufstellung_a)
        df_auswechseln_h = pd.DataFrame(l_start_auswechseln_h)
        df_auswechseln_a = pd.DataFrame(l_start_auswechseln_a)
        df_system_h = pd.DataFrame(l_system_h)
        df_system_a = pd.DataFrame(l_system_a)
        
        end_1 = len(df_start_h[0].str.split('\n', expand = True).columns)-1
        end_2 = len(df_start_a[0].str.split('\n', expand = True).columns)-1
        
        start_elf_heim = df_start_h[0].str.split('\n', expand = True).T.drop([0,2,4,6,8,10,12,14,16,18, end_1-1], axis = 0)[0].str.split('.', expand = True)[1]        
        start_elf_auswärts = df_start_a[0].str.split('\n', expand = True).T.drop([0,2,4,6,8,10,12,14,16,18, end_2-1], axis = 0)[0].str.split('.', expand = True)[1]
        
        df_start_elf_heim = pd.DataFrame(start_elf_heim)
        df_start_elf_auswärts = pd.DataFrame(start_elf_auswärts)
        df_start_elf_heim.columns = ['Spieler']
        df_start_elf_auswärts.columns = ['Spieler']
        
        auswechseln_h = df_auswechseln_h[0].str.split(' ', expand = True)[1]
        auswechseln_a = df_auswechseln_a[0].str.split(' ', expand = True)[1]
        df_auswechseln_h = pd.DataFrame(auswechseln_h)
        df_auswechseln_a = pd.DataFrame(auswechseln_a)
        

        system_h = str(df_system_h.iloc[0,0])
        system_a = str(df_system_a.iloc[0,0])
        
        df_auswechseln_h.columns = ['Spieler']
        df_auswechseln_a.columns = ['Spieler']
        
        f4 = t.unify_letters(df_auswechseln_h, 1)
        f5 = t.unify_letters(df_auswechseln_a, 1)
        df_auswechseln_h = f4.df()
        df_auswechseln_a = f5.df()
        
        df_auswechseln_heim = df_auswechseln_h.merge(df_spieler_h, on = 'Spieler', how = 'inner')
        df_auswechseln_auswärts = df_auswechseln_a.merge(df_spieler_a, on = 'Spieler', how = 'inner')
        df_auswechseln_heim = df_auswechseln_heim.assign(Startelf = 0)
        df_auswechseln_auswärts = df_auswechseln_auswärts.assign(Startelf = 0)
        
        df_start_heim = df_spieler_h.merge(df_auswechseln_h, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only'] 
        df_start_heim = df_start_heim.drop(columns = ['_merge'], axis = 1)
        df_start_heim = df_start_heim.assign(Startelf = 1)
        
        df_start_auswärts = df_spieler_a.merge(df_auswechseln_a, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
        df_start_auswärts = df_start_auswärts.drop(columns = ['_merge'], axis = 1)
        df_start_auswärts = df_start_auswärts.assign(Startelf = 1)
        
        actually_played_h = df_start_heim.append(df_auswechseln_heim)
        actually_played_a = df_start_auswärts.append(df_auswechseln_auswärts)
        
        actually_played_h = actually_played_h.assign(System = system_h)
        actually_played_a = actually_played_a.assign(System = system_a)
        
        all_player = actually_played_h.append(actually_played_a)
    
        df_all = df_all.append(all_player)
    
        df_all = df_all[['Vereins_ID', 'Verein', 'Spieler_ID', 'Spieler', 'Spieltag', 'Startelf', 'System', 'Jahr', 'Woche', 'Saison']]
        
    return df_all







