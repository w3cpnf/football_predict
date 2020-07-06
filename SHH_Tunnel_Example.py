# 2 examples how to establish a connection to a non-local database

import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
import time
from sshtunnel import SSHTunnelForwarder, DEFAULT_LOGLEVEL


class get_data_db:
    
    def __init__(self, case):
        self.case = case
        
    def get_data(self):
        
        case = self.case
        data = None
        while data is None:  
            
            try:
                ssh_password='' 
                sql_hostname = '' 
                sql_username = '' 
                sql_password = '!' 
                sql_main_database = '' 
                sql_port =  
                ssh_host = ''
                ssh_user = '' 
                ssh_port = 
            
                
                with SSHTunnelForwarder(
                        (ssh_host, ssh_port),
                        ssh_username=ssh_user,
                        ssh_password=ssh_password,
                        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    time.sleep(10)
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                            passwd=sql_password, db=sql_main_database,
                            port=tunnel.local_bind_port, connect_timeout=1000)
                    
                    if case == 1:
                        query = '''select s.Spieler_ID, s.Spieler from Spieler_ID s;'''
                    if case == 2:
                        query = '''select sd.Spieltag, sd.Jahr, sd.Woche, sd.Saison from Bl1_Spieltage_Date sd;'''
                    if case == 3:
                        query = '''select* from Vereins_ID;'''            

                        
                    data = pd.read_sql_query(query, conn)   
                    conn.close()        
                    df = pd.DataFrame(data) 

            except:
                pass
        
        return df
    
     
def upload_data(query, df):

    result = None
    while result is None:
    
        try:
    
            if query == 1:
                upload = df.values.tolist()
                mySql_insert_query = """INSERT INTO Bl1_Ergebnisse (Spieltag, Heimmannschaft_ID, Heimmannschaft, Ergebnis, HalbzeitErgebnis, Auswärtsmannschaft_ID, Auswärtsmannschaft, Jahr, Woche, Saison) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                                                                      
            if query == 2:
                upload = df.values.tolist()
                mySql_insert_query = """INSERT INTO Bl1_Spiele_Kategorisiert (Spieltag, Vereins_ID, Verein, Spiel_Ausgang, Heim, Tore, Gegentore, Gegner_ID, Gegner, Jahr, Woche, Saison) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            

            ssh_password=''
            sql_hostname = ''
            sql_username = ''
            sql_password = ''
            sql_main_database = ''
            sql_port = 
            ssh_host = ''
            ssh_user = ''
            ssh_port = 
                                     
            with SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                time.sleep(10)
                conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                        passwd=sql_password, db=sql_main_database,
                        port=tunnel.local_bind_port)
              
                cursor = conn.cursor()
                cursor.executemany(mySql_insert_query, upload)
                conn.commit()
                conn.close()  
                
                result = 1
        except:
            pass
    

