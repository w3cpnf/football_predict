from django.shortcuts import render
from django.http import HttpResponse
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from django.db import connection 

def main_page(request):
    return render(request, 'RandomForestApp/home.html')
    
def methods(request): 
    return render(request, 'RandomForestApp/methods.html')

def forecast_leagues(request): 
    return render(request, 'RandomForestApp/forecast_leagues.html')

def dataquality_leagues(request): 
    return render(request, 'RandomForestApp/legaues_dataquality.html')

def randomforest(request): 
    return render(request, 'RandomForestApp/random_forest.html')

def randomforest_premierleague(request): 
    return render(request, 'RandomForestApp/random_forest_premierleague.html')

def dq_premierleauge(request): 
    return render(request, 'RandomForestApp/dq_premierleague.html')

def dq_bundesliga(request): 
    return render(request, 'RandomForestApp/dq_bundesliga.html')

def dq_premierleauge_duplicates(request): 
    return render(request, 'RandomForestApp/dq_duplicates.html')

def dq_bundesliga_duplicates(request): 
    return render(request, 'RandomForestApp/dq_duplicates_bundesliga.html')

def dq_premierleauge_matchdays(request): 
    return render(request, 'RandomForestApp/dq_matchdays.html')

def dq_bundesliga_matchdays(request): 
    return render(request, 'RandomForestApp/dq_matchdays_bundesliga.html')

def dq_premierleauge_clubs(request): 
    return render(request, 'RandomForestApp/dq_clubs.html')

def dq_bundesliga_clubs(request): 
    return render(request, 'RandomForestApp/dq_clubs_bundesliga.html')

def feature_check_leagues(request): 
    return render(request, 'RandomForestApp/feature_check_leagues.html')

def feature_check_bundesliga(request): 
    return render(request, 'RandomForestApp/feature_check_bundesliga.html')      

def feature_check_odds_vs_bookmaker(request): 
    return render(request, 'RandomForestApp/feature_check_odds_vs_bookmaker.html')  
      
def feature_check_odds_vs_bookmaker_method(request): 
    return render(request, 'RandomForestApp/feature_check_odds_vs_bookmaker_method.html')  

def feature_check_odds_vs_bookmaker_results(request): 
    return render(request, 'RandomForestApp/feature_check_odds_vs_bookmaker_results.html')  

def feature_check_score_method(request): 
    return render(request, 'RandomForestApp/feature_check_score_method.html')  

def feature_check_score_randomforest(request): 
    return render(request, 'RandomForestApp/feature_check_score_randomforest.html') 

def get_random_forest_proba(x, y, forecast):
    classifier = RandomForestClassifier(n_estimators = 2000, criterion = 'gini', random_state = 0)
    classifier.fit(x, y)
    y_proba = classifier.predict_proba(forecast)       
    
    return y_proba

def prepare_data(df, vereins_id, saison, spieltag, variables_chosen):
    df = df[df['Heimmannschaft_ID']==vereins_id]
    df_seasons_before = df[df['Saison'] < saison]
    df_season_chosen = df[df['Saison'] == saison]
    df_season_chosen = df_season_chosen[df_season_chosen['Spieltag'] < spieltag]
    df_analyse = df_seasons_before.append(df_season_chosen, ignore_index = True)
    df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])        
    
    results = df_analyse[['Spiel_Ausgang']].values
    variables = df_analyse[variables_chosen].values
    
    return results, variables 

def prepare_forecast(df_forecast, saison, spieltag, vereins_id, variables_chosen):

    df_forecast = df_forecast.rename(columns = {'Auswärtsmannschaft_ID':'Gegner_ID'})
    df_forecast = df_forecast[df_forecast['Saison']==saison]
    df_forecast = df_forecast[df_forecast['Spieltag']==spieltag]
    df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==vereins_id]       
    home_team = df_forecast['Heimmannschaft'].iloc[0]
    away_team = df_forecast['Auswärtsmannschaft'].iloc[0]
    forecast = df_forecast[variables_chosen].values
    
    return home_team, away_team, forecast

def get_odds_random_forest(y_proba):
    odds_home = round(1/y_proba[0][2], 2)
    odds_draw = round(1/y_proba[0][1], 2)
    odds_away = round(1/y_proba[0][0], 2)
    return odds_home, odds_draw , odds_away

def get_premierleague_tables(variables):

    tables = ["pl_staging_ergebnisse", "pl_data_ergebnisse_kategorisiert"]
    for v in variables:
        if v == 'Kaderwert':
            tables.extend(["pl_data_vereine_kader_wert"])
        if v == 'FifaFeatures':
            tables.extend(["pl_staging_vereine_fifa_features"])
        if v == 'Trainer':
            tables.extend(["pl_data_trainer_spiele"])
        if v == 'Form':
            tables.extend(["pl_features_club_form"])
        if v == 'Odds':
            tables.extend(["pl_features_odds"])
        if v == 'System':
            tables.extend(["pl_data_vereine_spielsystem"])
        if v == 'GameData':
            tables.extend(["pl_features_club_data"])

    return tables

def get_premierleague_forecast_tables(variables):

    tables = ["pl_staging_vereine_kommende_spieltag"]
    for v in variables:
        if v == 'Kaderwert':
            tables.extend(["pl_data_vereine_kader_wert"])
        if v == 'FifaFeatures':
            tables.extend(["pl_staging_vereine_fifa_features"])
        if v == 'Trainer':
            tables.extend(["pl_data_trainer_spiele"])
        if v == 'Form':
            tables.extend(["pl_features_forecast_club_form"])
        if v == 'Odds':
            tables.extend(["pl_features_odds"])
        if v == 'System':
            tables.extend(["pl_data_vereine_spielsystem"])
        if v == 'GameData':
            tables.extend(["pl_features_forecast_club_data"])
    return tables


def get_bundesliga_tables(variables):

    tables = ["bl1_staging_ergebnisse", "bl1_data_ergebnisse_kategorisiert"]
    for v in variables:
        if v == 'Kaderwert':
            tables.extend(["bl1_data_vereine_kader_wert"])
        if v == 'FifaFeatures':
            tables.extend(["bl1_staging_vereine_fifa_features"])
        if v == 'Trainer':
            tables.extend(["bl1_data_trainer_spiele"])
        if v == 'Form':
            tables.extend(["bl1_features_club_form"])
        if v == 'Odds':
            tables.extend(["bl1_features_odds"])
        if v == 'System':
            tables.extend(["bl1_data_vereine_spielsystem"])
        if v == 'GameData':
            tables.extend(["bl1_features_club_data"])
        if v == 'Startelf':
            tables.extend(["bl1_features_startelf"])
    return tables

def get_bundesliga_forecast_tables(variables):

    tables = ["bl1_staging_vereine_kommende_spieltag"]
    for v in variables:
        if v == 'Kaderwert':
            tables.extend(["bl1_data_vereine_kader_wert"])
        if v == 'FifaFeatures':
            tables.extend(["bl1_staging_vereine_fifa_features"])
        if v == 'Trainer':
            tables.extend(["bl1_data_trainer_spiele"])
        if v == 'Form':
            tables.extend(["bl1_features_forecast_club_form"])
        if v == 'Odds':
            tables.extend(["bl1_features_odds"])
        if v == 'System':
            tables.extend(["bl1_data_vereine_spielsystem"])
        if v == 'GameData':
            tables.extend(["bl1_features_forecast_club_data"])
        if v == 'Startelf':
            tables.extend(["bl1_features_startelf"])
    return tables



def get_chosen_data(table_list, variables):

    df_all_home = pd.DataFrame()
    df_all_away = pd.DataFrame()
    
    for table in table_list:
        
        if table == 'pl_data_vereine_spielsystem' or table == 'bl1_data_vereine_spielsystem':
            query = '''Select Vereins_ID, Verein, Spieltag, Saison, System_ID as Spiel_System
                        from ''' +table+''' vss1
                        left outer join 
                        master_system ms on ms.System = vss1.Spiel_System'''
        else:
            query = 'select * from ' + table
        df = pd.read_sql(query, con = connection) 
        
        if table == 'pl_staging_vereine_kommende_spieltag' or table == 'bl1_staging_vereine_kommende_spieltag' or table == 'bl1_staging_ergebnisse' or table == 'pl_staging_ergebnisse':
            df_all_home = df
            df_all_away = df
            
        elif table == 'pl_features_odds' or table == 'bl1_features_odds':
            df_all_home = df_all_home.merge(df, on = ['Spieltag', 'Saison', 'Heimmannschaft_ID', 'Heimmannschaft'
                                            ,'Auswärtsmannschaft', 'Auswärtsmannschaft_ID'], how = 'inner')
            
        elif table == 'bl1_features_startelf' or table == 'pl_features_startelf':
            df_all_home = df_all_home.merge(df, left_on = ['Spieltag', 'Saison', 'Heimmannschaft_ID'],
                                  right_on = ['Spieltag', 'Saison', 'Vereins_ID'], how = 'inner')
            df_all_away = df_all_away.merge(df, left_on = ['Spieltag', 'Saison', 'Auswärtsmannschaft_ID'],
                                  right_on = ['Spieltag', 'Saison', 'Vereins_ID'], how = 'inner')
            df_all_home = df_all_home.drop(['Vereins_ID'], axis = 1)
            df_all_away = df_all_away.drop(['Vereins_ID'], axis = 1)
            
        else:
            df_all_home = df_all_home.merge(df, left_on = ['Spieltag', 'Saison', 'Heimmannschaft_ID', 'Heimmannschaft'],
                                  right_on = ['Spieltag', 'Saison', 'Vereins_ID', 'Verein'], how = 'inner')
            df_all_away = df_all_away.merge(df, left_on = ['Spieltag', 'Saison', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft'],
                                  right_on = ['Spieltag', 'Saison', 'Vereins_ID', 'Verein'], how = 'inner')
            df_all_home = df_all_home.drop(['Verein', 'Vereins_ID'], axis = 1)
            df_all_away = df_all_away.drop(['Verein', 'Vereins_ID'], axis = 1)
    
    
    df_all_away = df_all_away.rename(columns=lambda s: 'Gegner_' + s)        
    df_all = df_all_home.merge(df_all_away, left_on = ['Spieltag', 'Saison', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Heimmannschaft'],
                  right_on = ['Gegner_Spieltag', 'Gegner_Saison', 'Gegner_Auswärtsmannschaft_ID', 'Gegner_Auswärtsmannschaft'
                              , 'Gegner_Heimmannschaft'], how = 'inner')
    
    if 'Kaderwert' in variables:
        df_all = df_all.assign(Kaderwert_Differenz = lambda x: x['Kaderwert_Million'] - x['Gegner_Kaderwert_Million'],
                               Kaderwert_Per_Spieler_Differenz = lambda x: x['Kaderwert_Per_Spieler_Million'] - x['Gegner_Kaderwert_Per_Spieler_Million'])


    if 'FifaFeatures' in variables:
        df_all['Abwehr'] = pd.to_numeric(df_all['Abwehr'])
        df_all['Gesamt'] = pd.to_numeric(df_all['Gesamt'])
        df_all['Angriff'] = pd.to_numeric(df_all['Angriff'])
        df_all['Mittelfeld'] = pd.to_numeric(df_all['Mittelfeld'])
        df_all['Gegner_Abwehr'] = pd.to_numeric(df_all['Gegner_Abwehr'])
        df_all['Gegner_Gesamt'] = pd.to_numeric(df_all['Gegner_Gesamt'])
        df_all['Gegner_Angriff'] = pd.to_numeric(df_all['Gegner_Angriff'])
        df_all['Gegner_Mittelfeld'] = pd.to_numeric(df_all['Gegner_Mittelfeld'])
        df_all = df_all.assign(Abwehrdifferenz = lambda x: x['Abwehr'] - x['Gegner_Abwehr']
                               ,Gesamtdiffferenz = lambda x: x['Gesamt'] - x['Gegner_Gesamt']
                               ,Angriffdifferenz = lambda x: x['Angriff'] - x['Gegner_Angriff']
                               ,Mittelfelddifferenz = lambda x: x['Mittelfeld'] - x['Gegner_Mittelfeld']
                               ,Heimangriff_Abwehr_Differenz = lambda x: x['Angriff'] - x['Gegner_Abwehr']
                               ,Auswärtsangriff_Abwehr_Differenz = lambda x: x['Gegner_Angriff'] - x['Abwehr']
                               )
    df_all = df_all.rename(columns = {'Gegner_L1_Forecast':'Gegner_L1'
                                      ,'Gegner_L2_Forecast':'Gegner_L2', 'Gegner_L3_Forecast':'Gegner_L3'
                                      ,'Gegner_L4_Forecast':'Gegner_L4', 'Gegner_L5_Forecast':'Gegner_L5' 
                                      ,'L1_Forecast':'L1', 'L2_Forecast':'L2', 'L3_Forecast':'L3'
                                      ,'L4_Forecast':'L4', 'L5_Forecast':'L5'})
    return df_all


def get_variables_chosen(variables_chosen):
    variables = ['Gegner_ID']
    if len(variables_chosen)>0:
        for v in variables_chosen:
            
            if v == 'Kaderwert':
                variables.extend(["Kaderwert_Differenz", "Kaderwert_Per_Spieler_Differenz"])
            if v == 'FifaFeatures':
                variables.extend(["Abwehrdifferenz", "Gesamtdiffferenz", "Angriffdifferenz", "Mittelfelddifferenz", 
                                  "Heimangriff_Abwehr_Differenz", "Auswärtsangriff_Abwehr_Differenz"])
            if v == 'Trainer':
                variables.extend(["Trainer_ID", "Gegner_Trainer_ID"])
                
            if v == 'Form':
                variables.extend(["L1", "L2", "L3", "L4", "L5", "Gegner_L1", "Gegner_L2", "Gegner_L3", "Gegner_L4", "Gegner_L5"])
            if v == 'Odds':
                variables.extend(["B365H", "B365D", "B365A"])
            if v == 'System':
                variables.extend(["Spiel_System", "Gegner_Spiel_System"])
            if v == 'GameData':
                variables.extend(["Shot_Feature", "Shot_On_Goal_Feature", "Fouls_Feature", "Corner_Feature", 
                                  "Yellowcard_Feature", "Gegner_Shot_Feature", "Gegner_Shot_On_Goal_Feature",
                                  "Gegner_Fouls_Feature", "Gegner_Corner_Feature", "Gegner_Yellowcard_Feature"])
            if v == 'Startelf':
                variables.extend(["Spieler_1", "Spieler_2", "Spieler_3", "Spieler_4", "Spieler_5", "Spieler_6", "Spieler_7", "Spieler_8", 
                                  "Spieler_9", "Spieler_10", "Spieler_11", "Gegner_Spieler_1","Gegner_Spieler_2", "Gegner_Spieler_3", 
                                  "Gegner_Spieler_4", "Gegner_Spieler_5", "Gegner_Spieler_6", "Gegner_Spieler_7", "Gegner_Spieler_8",
                                  "Gegner_Spieler_9", "Gegner_Spieler_10", "Gegner_Spieler_11"])
    return variables


def random_forest_results(request):

    if request.GET.get('randomforest') == 'randomforest':

        variables = request.GET.getlist('selectvariables')
        variables_chosen  = get_variables_chosen(variables)
        
        vereins_id = int(request.GET.get('vereins_id'))
        saison = request.GET.get('saison')
        spieltag = int(request.GET.get('spieltag'))

        table_list = get_bundesliga_tables(variables)
        df = get_chosen_data(table_list, variables)
        df = df.sort_values(['Saison', 'Spieltag'])    
        
        results, x_variables = prepare_data(df, vereins_id, saison, spieltag, variables_chosen)
        
        table_list_forecast = get_bundesliga_forecast_tables(variables)
        df_forecast = get_chosen_data(table_list_forecast, variables)
        df_forecast = df_forecast.sort_values(['Saison', 'Spieltag']) 
        home_team, away_team, forecast = prepare_forecast(df_forecast, saison, spieltag, vereins_id, variables_chosen) 

        x = x_variables
        y = results.ravel()
        y_proba = get_random_forest_proba(x, y, forecast)
        
        odds_home, odds_draw, odds_away = get_odds_random_forest(y_proba)

        return render(request, 'RandomForestApp/random_forest_results.html', {'odds_home':odds_home, 'odds_draw':odds_draw, 'odds_away':odds_away,
                                                                              'home_team':home_team, 'away_team':away_team, 'variables_chosen':variables_chosen})
    else:
       return render(request, 'RandomForestApp/random_forest.html')
           
def random_forest_results_premier_league(request):

    if request.GET.get('randomforest') == 'randomforest':

        variables = request.GET.getlist('selectvariables')
        variables_chosen  = get_variables_chosen(variables)
        
        vereins_id = int(request.GET.get('vereins_id'))
        saison = request.GET.get('saison')
        spieltag = int(request.GET.get('spieltag'))
        
        table_list = get_premierleague_tables(variables)
        df = get_chosen_data(table_list, variables)
        df = df.sort_values(['Saison', 'Spieltag'])      
        
        results, x_variables = prepare_data(df, vereins_id, saison, spieltag, variables_chosen)
        
        table_list_forecast = get_premierleague_forecast_tables(variables)
        df_forecast = get_chosen_data(table_list_forecast, variables)
        
        home_team, away_team, forecast = prepare_forecast(df_forecast, saison, spieltag, vereins_id, variables_chosen)     
              
        x = x_variables
        y = results.ravel()
        
        y_proba = get_random_forest_proba(x, y, forecast)       
        
        odds_home, odds_draw, odds_away = get_odds_random_forest(y_proba)

        return render(request, 'RandomForestApp/random_forest_results.html', {'odds_home':odds_home, 'odds_draw':odds_draw, 'odds_away':odds_away,
                                                                              'home_team':home_team, 'away_team':away_team, 'variables_chosen':variables_chosen})
    else:
       return render(request, 'RandomForestApp/random_forest.html') 



def check_duplicates_premierleague(request):
    
    if request.GET.get('duplicates') == 'duplicates':
        
        table_list_gamedays = ['pl_staging_ergebnisse', 'pl_staging_football_uk', 'pl_staging_vereine_fifa_features', 
                               'pl_staging_vereine_kommende_spieltag', 'pl_data_ergebnisse_kategorisiert', 'pl_data_trainer_spiele', 
                               'pl_data_vereine_bookmaker_odds',
                               'pl_data_vereine_data_gov', 'pl_data_vereine_kader_wert', 'pl_data_vereine_spielplan', 
                               'pl_data_vereine_spielsystem', 'pl_features_club_data', 'pl_features_club_form',
                               'pl_features_forecast_club_data', 'pl_features_forecast_club_form', 'pl_features_odds']    
        
        no_duplicates_output = list()
        duplicates_output = list()
        for table in table_list_gamedays:
            query = 'select * from ' + table
            
            df = pd.read_sql(query, con = connection) 
            print(table)
            saisons = df['Saison'].drop_duplicates()    
            for s in saisons:
                df_s = df[df['Saison']==s]
                if len(df_s.drop_duplicates())==len(df_s):
                    no_duplicates_output.append(table)
                    no_duplicates_output.append(s)
                else:
                    duplicates_output.append(table)
                    duplicates_output.append(s)
                    
        return render(request, 'RandomForestApp/dq_results_premierleague.html', {'no_duplicates_output':no_duplicates_output, 
                                                                              'duplicates_output':duplicates_output})
    else:
        return render(request, 'RandomForestApp/dq_premierleague.html')             
    
def check_duplicates_bundesliga(request):
    
    if request.GET.get('duplicates') == 'duplicates':
        
        table_list_gamedays = ['bl1_staging_ergebnisse', 'bl1_staging_football_uk', 'bl1_staging_vereine_fifa_features', 
                           'bl1_staging_vereine_kommende_spieltag', 'bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele', 
                           'bl1_data_vereine_bookmaker_odds', 'bl1_data_vereine_data_gov', 'bl1_data_vereine_kader_wert', 
                           'bl1_data_vereine_spielplan', 'bl1_data_vereine_spielsystem', 'bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form', 'bl1_features_odds']    
        
        no_duplicates_output = list()
        duplicates_output = list()
        for table in table_list_gamedays:
            query = 'select * from ' + table
            
            df = pd.read_sql(query, con = connection) 
            print(table)
            saisons = df['Saison'].drop_duplicates()    
            for s in saisons:
                df_s = df[df['Saison']==s]
                if len(df_s.drop_duplicates())==len(df_s):
                    no_duplicates_output.append(table)
                    no_duplicates_output.append(s)
                else:
                    duplicates_output.append(table)
                    duplicates_output.append(s)
                    
        return render(request, 'RandomForestApp/dq_results_bundesliga.html', {'no_duplicates_output':no_duplicates_output, 
                                                                              'duplicates_output':duplicates_output})
    else:
        return render(request, 'RandomForestApp/dq_bundesliga.html')   


def check_matchdays_premierleague(request):
    
    if request.GET.get('matchday') == 'matchday':
        
        table_list_gamedays = ['pl_data_ergebnisse_kategorisiert', 'pl_data_trainer_spiele', 'pl_data_vereine_bookmaker_odds',
                               'pl_data_vereine_data_gov', 'pl_data_vereine_kader_wert', 'pl_data_vereine_spielplan', 
                               'pl_data_vereine_spielsystem', 'pl_features_club_data', 'pl_features_club_form',
                               'pl_features_forecast_club_data', 'pl_features_forecast_club_form', 'pl_features_odds', 
                               'pl_staging_ergebnisse', 'pl_staging_football_uk', 'pl_staging_vereine_fifa_features', 
                               'pl_staging_vereine_kommende_spieltag'] 
        
        df_all = pd.DataFrame()
        tables = list()
        for table in table_list_gamedays:
            query = 'select saison, count(distinct spieltag) as Spieltage from ' + table + ' group by saison'
            
            df = pd.read_sql(query, con = connection)   
            df = df.assign(Tables = table)
            df_all = df_all.append(df)

            
        saisons = list(df_all['saison']) 
        spieltage = list(df_all['Spieltage'])
        tables = list(df_all['Tables'])
        zipped = zip(saisons, spieltage, tables)

        return render(request, 'RandomForestApp/dq_results_premierleague_matchdays.html', {'zipped':zipped})
    else:
        return render(request, 'RandomForestApp/dq_premierleague.html')

def check_matchdays_bundesliga(request):
    
    if request.GET.get('matchday') == 'matchday':
        
        table_list_gamedays = ['bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele', 'bl1_data_vereine_bookmaker_odds',
                           'bl1_data_vereine_data_gov', 'bl1_data_vereine_kader_wert', 'bl1_data_vereine_spielplan', 
                           'bl1_data_vereine_spielsystem', 'bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form', 'bl1_features_odds', 
                           'bl1_staging_ergebnisse', 'bl1_staging_football_uk', 'bl1_staging_vereine_fifa_features', 
                           'bl1_staging_vereine_kommende_spieltag'] 
        
        df_all = pd.DataFrame()
        tables = list()
        for table in table_list_gamedays:
            query = 'select saison, count(distinct spieltag) as Spieltage from ' + table + ' group by saison'
            
            df = pd.read_sql(query, con = connection)   
            df = df.assign(Tables = table)
            df_all = df_all.append(df)

            
        saisons = list(df_all['saison']) 
        spieltage = list(df_all['Spieltage'])
        tables = list(df_all['Tables'])
        zipped = zip(saisons, spieltage, tables)

        return render(request, 'RandomForestApp/dq_results_bundesliga_matchdays.html', {'zipped':zipped})
    else:
        return render(request, 'RandomForestApp/dq_bundesliga.html')

def check_clubs_premier_league(request):
    if request.GET.get('clubs') == 'clubs':
        
        table_list_club_nbr = ['pl_data_ergebnisse_kategorisiert', 'pl_data_trainer_spiele',
                               'pl_data_vereine_kader_wert', 'pl_data_vereine_spielplan', 
                               'pl_data_vereine_spielsystem', 'pl_features_club_data', 'pl_features_club_form',
                               'pl_features_forecast_club_data', 'pl_features_forecast_club_form',
                               'pl_staging_vereine_fifa_features']    
        df_all = pd.DataFrame()
        for table in table_list_club_nbr:
    
            query = 'select saison, spieltag, count(distinct vereins_id) as Clubs_Nbr from ' + table + ' group by saison, spieltag having count(distinct vereins_id) != 20 order by saison, spieltag'
            
            df = pd.read_sql(query, con = connection)      
            df = df.assign(Tables = table)
            df_all = df_all.append(df)
            saisons = list(df_all['saison']) 
            spieltage = list(df_all['spieltag'])
            clubs = list(df_all['Clubs_Nbr'])
            tables = list(df_all['Tables'])
            zipped = zip(saisons, spieltage, tables, clubs)
            
        return render(request, 'RandomForestApp/dq_results_premierleague_clubs.html', {'zipped':zipped})
    else:
        return render(request, 'RandomForestApp/dq_premierleague.html')
    
    
def check_clubs_bundesliga(request):
    if request.GET.get('clubs') == 'clubs':
        
        table_list_club_nbr = ['bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele',
                           'bl1_data_vereine_kader_wert', 'bl1_data_vereine_spielplan', 
                           'bl1_data_vereine_spielsystem', 'bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form',
                           'bl1_staging_vereine_fifa_features']    
        df_all = pd.DataFrame()

        for table in table_list_club_nbr:
    
            query = 'select saison, spieltag, count(distinct vereins_id) as Clubs_Nbr from '  + table + ' group by saison, spieltag having count(distinct vereins_id) != 18 and saison > ' + "'2013/14'" + ' order by saison, spieltag'
            
            df = pd.read_sql(query, con = connection)      
            df = df.assign(Tables = table)
            df_all = df_all.append(df)
            saisons = list(df_all['saison']) 
            spieltage = list(df_all['spieltag'])
            clubs = list(df_all['Clubs_Nbr'])
            tables = list(df_all['Tables'])
            zipped = zip(saisons, spieltage, tables, clubs)
            
        return render(request, 'RandomForestApp/dq_results_bundesliga_clubs.html', {'zipped':zipped})
    else:
        return render(request, 'RandomForestApp/dq_bundesliga.html')
    
    
def get_random_forest_odds_vs_bookmaker(request):   
    if request.GET.get('CheckOdds') == 'CheckOdds':
        variables_chosen = request.GET.getlist('selectvariables')
        vereins_id = int(request.GET.get('vereins_id'))
        saison = request.GET.get('saison')
        von = int(request.GET.get('von'))
        bis = int(request.GET.get('bis'))
    
        table_list = get_bundesliga_tables(variables)
        df = get_chosen_data(table_list, variables)
        df = df[df['Heimmannschaft_ID'] == vereins_id]
        
        
        df = df.sort_values(by = ['Saison', 'Spieltag'])  
        #seperate df because only spieltage of season to analyse are relevant, otherwise all spieltage of all season are filtered
        df_seasons_before = df[df['Saison'] < saison]
        df_season_analysed = df[df['Saison'] == saison]
        
        #get spieltage to analyse of relevant season

        df_spieltag_seasons_analysed = df_season_analysed[df_season_analysed['Spieltag'] <= bis]
        df_spieltag_seasons_analysed = df_season_analysed[df_season_analysed['Spieltag'] >= von]
            
        all_left_spieltage = df_spieltag_seasons_analysed['Spieltag'].drop_duplicates()
        total_list = list()
        for spieltag_left in all_left_spieltage:
            #get data of relevant season
            df_spieltag_lef = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag']<=spieltag_left]
            #get data history of passed seasons
            df_analyse = df_seasons_before.append(df_spieltag_lef, ignore_index = True)
            df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])
            df_results = df_analyse[['Spiel_Ausgang']]
            df_variables = df_analyse[variables_chosen]
            
            df_odds = df_season_analysed[df_season_analysed['Spieltag']==spieltag_left]
            home_odds = df_odds['B365H'].iloc[0]
            draw_odds = df_odds['B365D'].iloc[0]
            away_odds = df_odds['B365A'].iloc[0]


            X_train = df_variables.values[:-1]
            X_test = df_variables.values[-1:]
            y_train = df_results.values[:-1].ravel()
            y_test = df_results.values[-1:].ravel()
            
            classifier = RandomForestClassifier(n_estimators = 2000, criterion='gini', random_state = 0)
            classifier.fit(X_train, y_train)
            y_proba = classifier.predict_proba(X_test)
            
            home_difference = (1/y_proba[0][2]) - home_odds
            draw_difference = (1/y_proba[0][1]) - draw_odds
            away_difference = (1/y_proba[0][0]) - away_odds
    
    
            if home_difference > draw_difference and home_difference > away_difference:
                
                if y_test == 1:
                    win = home_odds * 10
                else:
                    win = -10
        
            if draw_difference > home_difference and draw_difference > away_difference:
                
                if y_test == 0:
                    win = home_odds * 10
                else:
                    win = -10
         
            if away_difference > draw_difference and away_difference > home_difference:
                
                if y_test == 1:
                    win = home_odds * 10
                else:
                    win = -10  
            total_list.append(win)
    
        Result = sum(total_list)  
      
        return render(request, 'RandomForestApp/feature_check_odds_vs_bookmaker_results.html', {'Result':Result})
    else:
        return render(request, 'RandomForestApp/feature_check_odds_vs_bookmaker.html')


def random_forest_score(X_train, X_test, y_train, y_test, n_, criterion):
    
    classifier = RandomForestClassifier(n_estimators = n_, criterion = criterion, random_state = 0)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    
    print(score)
    
    return score



def get_random_forest_score(request):


    if request.GET.get('CheckOdds') == 'CheckOdds':
        variables_chosen = request.GET.getlist('selectvariables')
        criterion = request.GET.get('selectcriterion')
        saison = request.GET.get('saison')
        vereins_id = int(request.GET.get('vereins_id'))
        length = int(request.GET.get('testlength'))
        treenodes = int(request.GET.get('treenodes'))
        maxspieltag = int(request.GET.get('maxspieltag'))

        query_first_part = get_query_first_part()
        query_second_part = get_query_second_part()
        
        df_first = pd.read_sql(query_first_part, con = connection) 
        df_second = pd.read_sql(query_second_part, con = connection) 
        df = df_first.merge(df_second, on = ['Saison', 'Spieltag', 'Heimmannschaft_ID', 'Gegner_ID'])
        df = df.sort_values(by = ['Saison', 'Spieltag']) 
        df = df[df['Heimmannschaft_ID']==vereins_id]
        df_seasons_before = df[df['Saison'] < saison]
        df_season_chosen = df[df['Saison'] == saison]
        
        df_season_chosen = df_season_chosen[df_season_chosen['Spieltag']<=maxspieltag]
        df_analyse = df_seasons_before.append(df_season_chosen, ignore_index = True)
        df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])
        
        df_results = df_analyse[['Spiel_Ausgang']]
        df_analyse = df_analyse[variables_chosen]
        
        
        
        X_train = df_analyse.iloc[:,:].values[:-length]
        X_test = df_analyse.iloc[:,:].values[-length:]
        y_train = df_results.iloc[:,:].values[:-length].ravel()
        y_test = df_results.iloc[:,:].values[-length:].ravel()
    
        score = random_forest_score(X_train, X_test, y_train, y_test, treenodes, criterion)
        
        return render(request, 'RandomForestApp/feature_check_score_randomforest_results.html', {'score':score})
    else:
        return render(request, 'RandomForestApp/feature_check_leagues.html')        
        