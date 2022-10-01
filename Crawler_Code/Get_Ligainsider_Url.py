import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#import other files 
import Read_Load_Database as db


def get_url_via_google(saison, c):
    
    f1 = db.get_data_db(12)
    f2 = db.get_data_db(7)
    
    df_kader = f1.get_data()
    df_mapping_transfermarkt = f2.get_data()
    
    id_Verein = df_mapping_transfermarkt['Vereins_ID']
    v1 = id_Verein.iloc[c-1]
    
    df = df_kader[df_kader['Saison']==saison]
    df = df[df['Vereins_ID']==v1]

    spieler = df['Spieler'].drop_duplicates()
    
    df_url = pd.DataFrame()
    
    for s in spieler:
        
        df_s = df[df['Spieler']==s]
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        #driver = webdriver.Chrome('D:\Crawling\chromedriver')
        driver.get('http://www.google.com')
        query = str(s) + " Ligainsider "
        search = driver.find_element_by_name('q')
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@id="L2AGLb"]'))).click()
        time.sleep(2)
        try:
            element = driver.find_element_by_xpath("//h3[@class='LC20lb DKV0Md']")
            time.sleep(1)
            element.click()
            url = driver.current_url
            df_s = df_s.assign(Url = url)
            df_url = df_url.append(df_s)
            driver.quit()  
            
        except NoSuchElementException as v: 
            print(v)
            driver.quit()   
    df_url = df_url[['Spieler_ID', 'Spieler', 'Url', 'Verein', 'Vereins_ID', 'Saison']]  
    df_url = df_url.drop_duplicates()     
    return df_url
  
#df = get_url_via_google('2020/21', 2)
#db.upload_local_db_data(df, 11)    

