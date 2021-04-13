import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')


import pandas as pd
import mysql
import mysql.connector
from sqlalchemy import create_engine

class get_data_db:
    
    def __init__(self, case):
        self.case = case
        
    def get_data(self):
        
        case = self.case
          
        if case == 1:
            query = '''select* from master_spieler_id;'''
        if case == 2:
            query = '''select* from bl1_data_vereine_spielplan;''' 
        if case == 3:
            query = '''select* from master_vereins_id;'''            
        if case == 4:
            query = '''select* from bl1_mapping_ligainsider;'''  
        if case == 5:
            query = '''select* from Bl1_Verletzungen;'''     
        if case == 6:
            query = '''select* from bl1_staging_spieler_verletzt;''' 
        if case == 7:     
            query = '''select* from bl1_mapping_transfermarkt;'''
        if case == 8:
            query = '''select* from bl1_staging_spieler_daten;'''             
        if case == 9:
            query = '''select* from Bl1_Spieler_Daten;'''   
        if case == 10:     
            query = '''select* from bl1_data_spieler_wert_alter;'''
        if case == 11:     
            query = '''select* from bl1_data_spieler_kicker_position;'''    
        if case == 12:     
            query = '''select* from bl1_staging_spieler_kader;'''
        if case == 13:     
            query = '''select* from bl1_data_spieler_kicker_position;'''
        if case == 14:
            query = '''select* from Ligainsider_Transition;'''   
        if case == 15:
            query = '''select* from bl1_data_spieler_verletzt;'''          
        if case == 16:     
            query = '''select* from bl1_mapping_kicker;'''    
        if case == 17:    
            query = '''select* from master_trainer_id;'''
        if case == 18:
            query = '''select* from schiedsrichter_id;'''  
        if case == 19:
            query = '''select* from bl1_data_spieler_kicker_position;''' 
        if case == 20:
            query = '''select* from bl1_staging_ergebnisse;''' 
        if case == 21:
            query = '''select* from bl1_mapping_schiedsrichter;''' 
        if case == 22:
            query = '''select* from bl1_data_ergebnisse_kategorisiert;''' 
        if case == 23:
            query = '''select* from bl1_staging_vereine_kommende_spieltag;''' 
            
             
        mydb = mysql.connector.connect(
            host = '',
            user = '',
            passwd="",
            database = ''
        )
        
        df = pd.read_sql(query, con = mydb)
            
        return df 
    
 
    
def upload_local_db_data(df, query):
        
    if query == 1:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_staging_ergebnisse (Spieltag, Heimmannschaft_ID, Heimmannschaft, Ergebnis, HalbzeitErgebnis, 
                            Auswärtsmannschaft_ID, Auswärtsmannschaft, Jahr, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
                                                              
    if query == 2:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_data_ergebnisse_kategorisiert (Spieltag, Vereins_ID, Verein, Spiel_Ausgang, Heim, Tore, Gegentore,
                                Gegner_ID, Gegner, Jahr, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    
    if query == 3:
        df = df[['Vereins_ID', 'Verein', 'Spieltag', 'Tore', 'Torschüsse', 'Pfosten', 'Eigentore', 'Elfmeter', 'Elfmetertore', 'ZweikämpfeGewonnen',
                 'GelbeKarten', 'Fouls', 'KopfbälleGewonnen', 'Laufleistung', 'Sprints', 'IntensivesLaufen', 'Passquote', 'Flanken', 'Heim', 'Gegentore', 'Jahr', 'Woche', 'Saison']]
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_vereine_bl (Vereins_ID, Verein, Spieltag, Tore, Torschüsse, Pfosten, Eigentore, Elfmeter, Elfmetertore, ZweikämpfeGewonnen,
                                GelbeKarten, Fouls, KopfbälleGewonnen, Laufleistung, Sprints, IntensivesLaufen, Passquote, Flanken, Heim, Gegentore, Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                               
    if query == 4:  
        df = df[['Vereins_ID', 'Verein',  'Spieltag',  'Gesamt',  'Angriff', 'Abwehr',  'Mittelfeld', 'Jahr', 'Woche', 'Saison']]
        upload = df.values.tolist()                  
        mySql_insert_query = """INSERT INTO bl1_staging_vereine_fifa_features (Vereins_ID, Verein,  Spieltag,  Gesamt,  Angriff, Abwehr,  Mittelfeld, Jahr, Saison) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    
    if query == 5:  
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_staging_vereine_daten (Vereins_ID, Verein, Spieltag, Torschüsse, Schüsse, Fouls, GelbeKarten, RoteKarten,
                                Flanken, Ecken, Ballbesitz, Heim,Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                       %s, %s, %s, %s, %s) """
    if query == 6: 
        upload = df.values.tolist()                              
        mySql_insert_query = """INSERT INTO master_spieler_id (Spieler_ID, Spieler) 
                               VALUES (%s, %s) """
                               
    if query == 7:

        upload = df.values.tolist()  
        mySql_insert_query = """INSERT INTO bl1_data_spieler_wert_alter (Spieltag, Spieler_ID, Spieler, Verein, Vereins_ID, Geburtstag,
                                                                            Spieler_Alter, Spielerwert_Million, Jahr, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """                              
    if query == 8:
        upload = df.values.tolist()  
        mySql_insert_query = """INSERT INTO bl1_data_vereine_spielplan (Vereins_ID, Verein, Saison, Spieltag, Datum, Jahr, Monat, Woche, Tag) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    if query == 9:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_data_spieler_kicker_position (Spieler_ID, Spieler, Vereins_ID, Verein, Spieltag, Position, Note, Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    if query == 10:

        df = df[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein',  'Spieltag', 'Position', 'Note_Spieltag', 'Pkt_Spieltag', 'Min_Spieltag', 'Durchschnitt_Note', 
                       'Durchschnitt_Pos_Pkt', 'Jahr', 'Woche', 'Saison', 'Zeitstempel']] 
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO Bl1_Spieler_Performance (Spieler_ID, Spieler, Vereins_ID, Verein,  Spieltag, Position, Note_Spieltag, 
                        Pkt_Spieltag, Min_Spieltag, Durchschnitt_Note, Durchschnitt_Pos_Pkt, Jahr, Woche, Saison, Zeitstempel) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) """                       
    if query == 11:
        mySql_insert_query = """INSERT INTO bl1_mapping_ligainsider (Spieler_ID, Spieler, Url, Verein, Vereins_ID, Saison) 
                       VALUES (%s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()  
        
    if query == 12:
        df = df[['Spieler_ID', 'Spieler', 'Url']]
        mySql_insert_query = """INSERT INTO Ligainsider_Transition (Spieler_ID, Spieler, Url) 
                       VALUES (%s, %s, %s) """
        upload = df.values.tolist() 
        
    if query == 14:
        upload = df.values.tolist()          
        mySql_insert_query = """INSERT INTO bl1_staging_spieler_daten (Spieler_ID, Spieler, Vereins_ID, Verein, Spieltag, Tore, Torvorlagen, Torschüsse, Pfosten, 
                                Elfmeter, ElfmeterTore, Passquote, Ballbesitzphasen, KopfbälleGewonnen, Flanken, GelbeKarten, Fouls, Laufleistung, Sprints, 
                                IntensivesLaufen, Paraden, Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """       
    if query == 14:                          
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO trainer_id (Trainer_ID, Trainer) 
                               VALUES (%s, %s) """
                               
    if query == 15:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_trainer_spiele (Trainer_ID, Trainer, Vereins_ID, Verein, Von, Bis, Saison, Spieltag, Datum, Jahr, Geburtstag) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    if query == 16:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_schiedsrichter_saison (Schiedsrichter_ID, Name, Saison) 
                               VALUES (%s, %s, %s) """                                 
    if query == 17:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_schiedsrichter_spieler (Schiedsrichter_ID, Name, Spieltag, Datum, Heimmannschaft_ID, Heimmannschaft, Auswärtsmannschaft_ID, Auswärtsmannschaft, Saison, Jahr, Woche) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """     
    if query == 18:
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_staging_vereine_kommende_spieltag (Heimmannschaft_ID, Heimmannschaft, Auswärtsmannschaft_ID, Auswärtsmannschaft, Spieltag, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s) """   
                               
    if query == 19:
        df = df[['Vereins_ID', 'Verein', 'Spieltag', 'Tore', 'Torschüsse', 'Pfosten', 'Eigentore', 'Elfmeter', 'Elfmetertore', 'ZweikämpfeGewonnen',
                 'GelbeKarten', 'Fouls', 'KopfbälleGewonnen', 'Laufleistung', 'Sprints', 'IntensivesLaufen', 'Passquote', 'Flanken', 'Heim', 'Gegentore', 'Jahr', 'Woche', 'Saison']]
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO bl1_staging_vereine_bl (Vereins_ID, Verein, Spieltag, Tore, Torschüsse, Pfosten, Eigentore, Elfmeter, Elfmetertore, ZweikämpfeGewonnen,
                                GelbeKarten, Fouls, KopfbälleGewonnen, Laufleistung, Sprints, IntensivesLaufen, Passquote, Flanken, Heim, Gegentore, Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """   
    if query == 20:                      
        mySql_insert_query = """INSERT INTO bl1_staging_spieler_kader (Vereins_ID, Verein, Spieler_ID, Spieler, Position, Transferfenster, Saison) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()
        
    if query == 21:                      
        mySql_insert_query = """INSERT INTO bl1_data_vereine_kader_wert (Spieltag, Vereins_ID, Verein, Kadergröße, Kaderwert_Million,
                                Kaderwert_Per_Spieler_Million, Jahr, Saison) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """  
        upload = df.values.tolist()
        
    if query == 22:
        df = df[['Spieler_ID', 'Spieler','Vereins_ID', 'Verein', 'Spieltag', 'Fouls', 'Geklärte_Bälle', 'Abgefangene_Bälle', 'Ball_Eroberungen', 'Ballverluste', 
                 'Torschuss_Vorlagen', 'Kreierte_Großchancen', 'Schüsse_aufs_Tor', 'Fehler_vor_Schuss_Gegentor', 'Geblockte_Bälle', 'Gewonnene_Zweikämpfe_Prozent', 
                 'Gewonnene_Zweikämpfe_Absolut','Erfolgreiche_Pässe_Prozent',
                 'Erfolgreiche_Pässe_Absolut', 'Gewonnene_Luftkämpfe_Prozent', 'Gewonnene_Luftkämpfe_Absolut', 'Erfolgreiche_Tacklings_Prozent',
                 'Erfolgreiche_Tacklings_Absolut', 'Erfolgreiche_Dribblings_Prozent', 'Erfolgreiche_Dribblings_Absolut', 'Schussgenauigkeit_Prozent', 
                 'Schussgenauigkeit_Absolut', 'Paraden', 'Weiße_Weste', 'Abgwehrte_Schüsse_Prozent', 'Abgwehrte_Schüsse_Absolut','Elfmeter_Pariert_Prozent', 
                 'Elfmeter_Pariert_Absolut','Großchancen_Pariert_Prozent', 'Großchancen_Pariert_Absolut','Strafraum_Beherrschung_Prozent', 'Strafraum_Beherrschung_Absolut',
                 'Woche', 'Jahr', 'Saison']]
        
        mySql_insert_query = """INSERT INTO bl1_staging_spieler_daten (Spieler_ID, Spieler, Vereins_ID, Verein, Spieltag, Fouls, Geklärte_Bälle, Abgefangene_Bälle, Ball_Eroberungen,
                                                                Ballverluste, Torschuss_Vorlagen, Kreierte_Großchancen, Schüsse_aufs_Tor, Fehler_vor_Schuss_Gegentor,
                                                                Geblockte_Bälle, Gewonnene_Zweikämpfe_Prozent, Gewonnene_Zweikämpfe_Absolut,
                                                                Erfolgreiche_Pässe_Prozent, Erfolgreiche_Pässe_Absolut, Gewonnene_Luftkämpfe_Prozent,
                                                                Gewonnene_Luftkämpfe_Absolut, Erfolgreiche_Tacklings_Prozent, Erfolgreiche_Tacklings_Absolut,
                                                                Erfolgreiche_Dribblings_Prozent, Erfolgreiche_Dribblings_Absolut, Schussgenauigkeit_Prozent,
                                                                Schussgenauigkeit_Absolut, Paraden, Weiße_Weste, Abgwehrte_Schüsse_Prozent, Abgwehrte_Schüsse_Absolut,
                                                                Elfmeter_Pariert_Prozent, Elfmeter_Pariert_Absolut, Großchancen_Pariert_Prozent, Großchancen_Pariert_Absolut,
                                                                Strafraum_Beherrschung_Prozent, Strafraum_Beherrschung_Absolut, Woche, Jahr, Saison) 
        
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        
        upload = df.values.tolist()
    if query == 23:

        df = df[['Spieler_ID', 'Spieler','Aktuelle_Verletzung', 'Art', 'Von','Bis', 'Fehlzeit', 'Verpasste_Spielzeit', 'Zeitstempel']]
        mySql_insert_query = """INSERT INTO Bl1_Spieler_Verletzt (Spieler_ID, Spieler, Aktuelle_Verletzung, Art, Von, Bis, Fehlzeit, Verpasste_Spielzeit, Zeitstempel) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()  

    if query == 24:
        mySql_insert_query = """INSERT INTO bl1_data_spieler_startelf_system (Vereins_ID, Verein, Spieler_ID, Spieler, Spieltag, Startelf, Spiel_System, 
                                Jahr, Woche, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist() 
        
    if query == 25:
        mySql_insert_query = """INSERT INTO bl1_data_schiedsrichter_spiele (Schiedsrichter_ID, Schiedsrichter, Spieltag, Heimmannschaft_ID,
                                Heimmannschaft, Auswärtsmannschaft_ID, Auswärtsmannschaft, Saison, Jahr) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()   
        
    if query == 26:
        mySql_insert_query = """INSERT INTO bl1_staging_spieler_verletzt (Spieler_ID, Spieler, Aktuelle_Verletzung, Art, Von, Bis, Fehlzeit, 
                                Verpasste_Spielzeit) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()   
        
    if query == 27:
        mySql_insert_query = """INSERT INTO bl1_data_spieler_verletzt (Spieltag, Spieler_ID, Spieler, Vereins_ID, Verein, Datum, Von, Bis, Saison) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
        upload = df.values.tolist()   
        
    if query == 28:  
        mySql_insert_query = """INSERT INTO bl1_data_spieler_daten (Spieler_ID, Spieler, Vereins_ID, Verein,Spieltag, Fouls, Geklärte_Bälle, Abgefangene_Bälle,Ball_Eroberungen, Ballverluste,
                                Torschuss_Vorlagen, Kreierte_Großchancen, Schüsse_aufs_Tor, Fehler_vor_Schuss_Gegentor, Geblockte_Bälle, 
                                Gewonnene_Zweikämpfe_Prozent, Gewonnene_Zweikämpfe, Zweikämpfe, Erfolgreiche_Pässe_Prozent, Erfolgreiche_Pässe,
                                Pässe, Gewonnene_Luftkämpfe_Prozent, Gewonnene_Luftkämpfe, Luftkämpfe,Erfolgreiche_Tacklings_Prozent, 
                                Erfolgreiche_Tacklings, Tacklings, Erfolgreiche_Dribblings_Prozent, Erfolgreiche_Dribblings, Dribblings,
                                Schussgenauigkeit_Prozent, Erfolgreiche_Schussgenauigkeit,Schussgenauigkeit, Abgwehrte_Schüsse_Prozent, 
                                Erfolgreiche_Abgwehrte_Schüsse, Abgwehrte_Schüsse, Elfmeter_Pariert_Prozent, Elfmeter_Pariert, Elfmeter, 
                                Großchancen_Pariert_Prozent, Großchancen_Pariert, Großchancen, Strafraum_Beherrschung_Prozent,
                                Erfolgreiche_Strafraum_Beherrschung, Strafraum_Beherrschung, Paraden, Weiße_Weste, Woche, Jahr, Saison) 
        
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        
        upload = df.values.tolist()    
    if query == 29:
        mySql_insert_query = """INSERT INTO test (Spieler_ID, Spiel_System) 
                               VALUES (%s, %s) """
        upload = df.values.tolist()  
        
    if query == 30:

        df = df[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein',  'Spieltag', 'Position', 'Note_Spieltag', 'Pkt_Spieltag', 'Min_Spieltag', 'Durchschnitt_Note', 
                       'Durchschnitt_Pos_Pkt', 'Jahr', 'Woche', 'Saison', 'Zeitstempel']] 
        upload = df.values.tolist()
        mySql_insert_query = """INSERT INTO Bl1_Spieler_Performance (Spieler_ID, Spieler, Vereins_ID, Verein,  Spieltag, Position, Note_Spieltag, 
                        Pkt_Spieltag, Min_Spieltag, Durchschnitt_Note, Durchschnitt_Pos_Pkt, Jahr, Woche, Saison) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                               %s, %s, %s, %s) """ 
        upload = df.values.tolist()  
        
    mydb = mysql.connector.connect(
         host = '',
         user = '',
         passwd="",
         database = ''
     )
    cursor = mydb.cursor()
    cursor.executemany(mySql_insert_query, upload)
    mydb.commit()
    mydb.close()
    


def upload_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://pw@localhost:3306/datenbank', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'append', index=False)
    #print("Data succesfully uploaded")
    
def upload_replace_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://pw@localhost:3306/datenbank', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'replace', index=False)
    #print("Data succesfully uploaded")