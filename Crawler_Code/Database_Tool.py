import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')


import pandas as pd
import mysql
import mysql.connector
from sqlalchemy import create_engine

import My_Tools as t

def get_table(table):
    query = 'select* from '+table   
    df = t.connection(query)
    return df

def delete_table_saison(table, saison):
    query = 'delete from '+ table + ' where saison = ' +  saison 
    t.connection(query)
    

def upload_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://root:Teleshop,1871@localhost:3306/bl1_daten', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'append', index=False)
    
    
def upload_replace_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://root:Teleshop,1871@localhost:3306/bl1_daten', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'replace', index=False)
