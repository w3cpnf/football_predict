from django.shortcuts import render
from Test_Methods import models
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from keras.utils import np_utils
from io import StringIO
from sklearn.feature_selection import mutual_info_classif  
import numpy as np
import pandas as pd
import json
from django.http import HttpResponse


def main_page(request):
    return render(request, 'Test_Methods/app_choice.html')

def method_performance(request):
    return render(request, 'Test_Methods/method_performance.html')
    
def method_performance_league_choice(request):
    return render(request, 'Test_Methods/method_performance_league_choice.html')

def method_odds_against_bookmaker_league_choice(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_league_choice.html')

def method_mutual_information_league_choice(request):
    return render(request, 'Test_Methods/method_mutual_information_league_choice.html')

def method_tree_importance_league_choice(request):
    return render(request, 'Test_Methods/method_tree_importance_league_choice.html')

def method_correlation_league_choice(request):
    return render(request, 'Test_Methods/method_correlation_league_choice.html')

def method_step_forward_league_choice(request):
    return render(request, 'Test_Methods/method_step_forward_league_choice.html')

def method_step_backward_league_choice(request):
    return render(request, 'Test_Methods/method_step_backward_league_choice.html')

def method_exhaustive_search_league_choice(request):
    return render(request, 'Test_Methods/method_exhaustive_search_league_choice.html')

def method_gradient_boost_league_choice(request):
    return render(request, 'Test_Methods/method_gradient_boost_league_choice.html')

def method_performance_bundesliga_algorithm_choice(request):
    return render(request, 'Test_Methods/method_performance_bundesliga_algorithm_choice.html')    

def method_performance_premierleague_algorithm_choice(request):
    return render(request, 'Test_Methods/method_performance_premierleague_algorithm_choice.html')  

def method_odds_against_bookmaker_bundesliga_algorithm_choice(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_algorithm_choice.html')   

def method_odds_against_bookmaker_premierleague_algorithm_choice(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_premierleague_algorithm_choice.html')   

def method_performance_bundesliga_randomforest(request):
    return render(request, 'Test_Methods/method_performance_bundesliga_randomforest.html')   

def method_performance_premierleague_randomforest(request):
    return render(request, 'Test_Methods/method_performance_premierleague_randomforest.html') 

def method_performance_bundesliga_ann(request):
    return render(request, 'Test_Methods/method_performance_bundesliga_ann.html')   

def method_performance_premierleague_ann(request):
    return render(request, 'Test_Methods/method_performance_premierleague_ann.html')   

def method_odds_against_bookmaker_bundesliga_randomforest(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_randomforest.html')   

def method_odds_against_bookmaker_premierleague_randomforest(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_premierleague_randomforest.html') 

def method_odds_against_bookmaker_bundesliga_ann(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_ann.html')   

def method_odds_against_bookmaker_premierleague_ann(request):
    return render(request, 'Test_Methods/method_odds_against_bookmaker_premierleague_ann.html')   

def method_mutual_information_bundesliga(request):
    return render(request, 'Test_Methods/method_mutual_information_bundesliga.html')  

def method_mutual_information_premierleague(request):
    return render(request, 'Test_Methods/method_mutual_information_premierleague.html')  

def method_tree_importance_bundesliga(request):
    return render(request, 'Test_Methods/method_tree_importance_bundesliga.html') 

def method_tree_importance_premierleague(request):
    return render(request, 'Test_Methods/method_tree_importance_premierleague.html') 

def method_correlation_bundesliga(request):
    return render(request, 'Test_Methods/method_correlation_bundesliga.html') 

def method_correlation_premierleague(request):
    return render(request, 'Test_Methods/method_correlation_premierleague.html') 

def method_step_forward_bundesliga(request):
    return render(request, 'Test_Methods/method_step_forward_bundesliga.html') 

def method_step_forward_premierleague(request):
    return render(request, 'Test_Methods/method_step_forward_premierleague.html') 

def method_step_backward_bundesliga(request):
    return render(request, 'Test_Methods/method_step_backward_bundesliga.html') 

def method_step_backward_premierleague(request):
    return render(request, 'Test_Methods/method_step_backward_premierleague.html') 

def method_exhaustive_search_bundesliga(request):
    return render(request, 'Test_Methods/method_exhaustive_search_bundesliga.html') 

def method_exhaustive_search_premierleague(request):
    return render(request, 'Test_Methods/method_exhaustive_search_premierleague.html') 

def method_gradient_boost_bundesliga(request):
    return render(request, 'Test_Methods/method_gradient_boost_bundesliga.html') 

def method_gradient_boost_premierleague(request):
    return render(request, 'Test_Methods/method_gradient_boost_premierleague.html') 

def random_forest_results(request):

    if request.GET.get('randomforest') == 'randomforest':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag = int(request.GET.get('Matchday'))
        length = int(request.GET.get('Testlength'))
        n = int(request.GET.get('TreeNumber'))
        Criterion = request.GET.get('Criterion')
        
        df = models.get_training_data()
        variables = models.check_startelf(variables)
            
        df = models.prepare_data(df, saison, spieltag)

        df_variables = df[variables]
        
        
        if 'Heimmannschaft_ID' in variables:
            df_variables, home_teams_encoded = models.encode_variable(df_variables, 'Heimmannschaft_ID')  
            df_variables, away_teams_encoded = models.encode_variable(df_variables, 'Gegner_ID')
            teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
        if 'Trainer_ID' in variables:
            df_variables, home_trainer_encoded = models.encode_variable(df_variables, 'Trainer_ID')  
            df_variables, away_trainer_encoded = models.encode_variable(df_variables, 'Gegner_Trainer_ID')
            trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
        if 'HeimSystem' in variables:
            df_variables, home_system_encoded = models.encode_variable(df_variables, 'HeimSystem')  
            df_variables, away_system_encoded = models.encode_variable(df_variables, 'AuswärtsSystem')  
            system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
            
        
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
    
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = teams_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = trainer_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = system_encoded       
        
        
        
        
        df_variables = df_variables.values
        df_dependant = df['Spiel_Ausgang'].ravel()   
        nbr_games = len(df_dependant)
        
        
        df_variables = np.concatenate((df_variables, all_encoded_variables), axis=1)

        df_dependant = df['Spiel_Ausgang']
            
        nbr_games = len(df_dependant)
        X_train, X_test, y_train, y_test = models.split_data(df_variables, df_dependant, length)
        length_train_x = len(X_train)
        length_test_x = len(X_test)    
        score, recall, precision = models.random_forest_score(X_train, X_test, y_train, y_test, n, Criterion)
        
        df_binary = models.spielausgang_to_binary(df)
        df_variables_binary = df_binary[variables]
        df_dependant_binary = df_binary['Spiel_Ausgang'] 
        
        X_train_binary, X_test_binary, y_train_binary, y_test_binary = models.split_data(df_variables_binary, df_dependant_binary, length)
        score_binary, recall_binary, precision_binary = models.random_forest_scores_binary(X_train_binary, X_test_binary, y_train_binary, y_test_binary, n, 'gini')
        return render(request, 'Test_Methods/method_performance_bundesliga_randomforest_result.html', {
                                                                                                       'nbr_games':nbr_games, 
                                                                                                       'length_train_x':length_train_x,
                                                                                                       'length_test_x':length_test_x,
                                                                                                       'score':score,
                                                                                                       'recall':recall,
                                                                                                       'precision':precision,
                                                                                                       'variables':variables,
                                                                                                       'score_binary':score_binary,
                                                                                                       'recall_binary':recall_binary,
                                                                                                       'precision_binary':precision_binary
                                                                                                       })
    else:
       return render(request, 'Test_Methods/app_choice.html')



def random_forest_premier_league_results(request):

    if request.GET.get('randomforest') == 'randomforest':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag = int(request.GET.get('Matchday'))
        length = int(request.GET.get('Testlength'))
        n = int(request.GET.get('TreeNumber'))
        Criterion = request.GET.get('Criterion')
        
        df = models.get_premierleague_training_data()
        variables = models.check_startelf(variables)
            
        df = models.prepare_data(df, saison, spieltag)
        df_variables = df[variables]
        
        if 'Heimmannschaft_ID' in variables:
            df_variables, home_teams_encoded = models.encode_variable(df_variables, 'Heimmannschaft_ID')  
            df_variables, away_teams_encoded = models.encode_variable(df_variables, 'Gegner_ID')
            teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
        if 'Trainer_ID' in variables:
            df_variables, home_trainer_encoded = models.encode_variable(df_variables, 'Trainer_ID')  
            df_variables, away_trainer_encoded = models.encode_variable(df_variables, 'Gegner_Trainer_ID')
            trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
        if 'HeimSystem' in variables:
            df_variables, home_system_encoded = models.encode_variable(df_variables, 'HeimSystem')  
            df_variables, away_system_encoded = models.encode_variable(df_variables, 'AuswärtsSystem')  
            system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
            
        
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
    
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = teams_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = trainer_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = system_encoded       
        
        
        df_variables = df_variables.values
        df_dependant = df['Spiel_Ausgang'].ravel()   
        nbr_games = len(df_dependant)
        
        df_variables = np.concatenate((df_variables, all_encoded_variables), axis=1)
        
        X_train, X_test, y_train, y_test = models.split_data(df_variables, df_dependant, length)
        
        length_train_x = len(X_train)
        length_test_x = len(X_test)    
        score, recall, precision = models.random_forest_score(X_train, X_test, y_train, y_test, n, Criterion)
        
        df_binary = models.spielausgang_to_binary_premier_league(df)
        df_variables_binary = df_binary[variables]
        df_dependant_binary = df_binary['Spiel_Ausgang'] 
        
        X_train_binary, X_test_binary, y_train_binary, y_test_binary = models.split_data(df_variables_binary, df_dependant_binary, length)
        score_binary, recall_binary, precision_binary = models.random_forest_scores_binary(X_train_binary, X_test_binary, y_train_binary, y_test_binary, n, 'gini')
        return render(request, 'Test_Methods/method_performance_premierleague_randomforest_result.html', {
                                                                                                       'nbr_games':nbr_games, 
                                                                                                       'length_train_x':length_train_x,
                                                                                                       'length_test_x':length_test_x,
                                                                                                       'score':score,
                                                                                                       'recall':recall,
                                                                                                       'precision':precision,
                                                                                                       'variables':variables,
                                                                                                       'score_binary':score_binary,
                                                                                                       'recall_binary':recall_binary,
                                                                                                       'precision_binary':precision_binary
                                                                                                       })
    else:
       return render(request, 'Test_Methods/app_choice.html')
    
    

def ann_results(request):

    if request.GET.get('ann') == 'ann':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag = int(request.GET.get('Matchday'))
        length = int(request.GET.get('Testlength'))
        epochs = int(request.GET.get('Epochs'))
        batch_size = int(request.GET.get('Batch'))
        learning_rate = float(request.GET.get('LearningRate'))
        nbr_layers = int(request.GET.get('Layers'))
        
        df = models.get_training_data()
        
        variables = models.check_startelf(variables)
            
        df = models.prepare_data(df, saison, spieltag)
        #df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 2 if x == 1 else (1 if x == 0 else 0))
        df = models.spielausgang_to_binary(df)
        #df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 2 if x == 1 else (1 if x == 0 else 0))
        uniques, ids = np.unique(df['Spiel_Ausgang'], return_inverse=True)
        df_variables = df[variables]

        
        if 'Heimmannschaft_ID' in variables:
            df_variables, home_teams_encoded = models.encode_variable(df_variables, 'Heimmannschaft_ID')  
            df_variables, away_teams_encoded = models.encode_variable(df_variables, 'Gegner_ID')
            teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
        if 'Trainer_ID' in variables:
            df_variables, home_trainer_encoded = models.encode_variable(df_variables, 'Trainer_ID')  
            df_variables, away_trainer_encoded = models.encode_variable(df_variables, 'Gegner_Trainer_ID')
            trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
        if 'HeimSystem' in variables:
            df_variables, home_system_encoded = models.encode_variable(df_variables, 'HeimSystem')  
            df_variables, away_system_encoded = models.encode_variable(df_variables, 'AuswärtsSystem')  
            system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
            
        
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
    
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = teams_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = trainer_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = system_encoded  
            
        df_variables = df_variables.values
        df_dependant = df['Spiel_Ausgang'].ravel()   
        df_variables = np.concatenate((df_variables, all_encoded_variables), axis=1)
        
        X_train, X_test, y_train, y_test = models.split_data(df_variables, df_dependant, length)
        
        nbr_games = len(df_dependant)
        length_train_x = len(X_train)
        length_test_x = len(X_test)    
        
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.fit_transform(X_test)

        y_categorical_train = np_utils.to_categorical(y_train, num_classes=2)
        score, recall, precision = models.ann_score(X_train, X_test, y_categorical_train, y_test, uniques, epochs, batch_size, learning_rate, nbr_layers)

        
        return render(request, 'Test_Methods/method_performance_bundesliga_ann_result.html', {                                                                                                      'nbr_games':nbr_games, 
                                                                            'length_train_x':length_train_x,
                                                                            'length_test_x':length_test_x,
                                                                            'score':score,
                                                                            'recall':recall,
                                                                            'precision':precision,
                                                                            'variables':variables
#                                                                            'score_binary':score_binary,
#                                                                            'recall_binary':recall_binary,
#                                                                            'precision_binary':precision_binary
                                                                                })
    else:
       return render(request, 'Test_Methods/app_choice.html')

def ann_premierleague_results(request):

    if request.GET.get('ann') == 'ann':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag = int(request.GET.get('Matchday'))
        length = int(request.GET.get('Testlength'))
        epochs = int(request.GET.get('Epochs'))
        batch_size = int(request.GET.get('Batch'))
        learning_rate = float(request.GET.get('LearningRate'))
        nbr_layers = int(request.GET.get('Layers'))
        
        df = models.get_premierleague_training_data()
            
        df = models.prepare_data(df, saison, spieltag)
        #df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 2 if x == 1 else (1 if x == 0 else 0))
        df = models.spielausgang_to_binary_premier_league(df)
        #df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 2 if x == 1 else (1 if x == 0 else 0))
        uniques, ids = np.unique(df['Spiel_Ausgang'], return_inverse=True)
        df_variables = df[variables]

        
        if 'Heimmannschaft_ID' in variables:
            df_variables, home_teams_encoded = models.encode_variable(df_variables, 'Heimmannschaft_ID')  
            df_variables, away_teams_encoded = models.encode_variable(df_variables, 'Gegner_ID')
            teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
        if 'Trainer_ID' in variables:
            df_variables, home_trainer_encoded = models.encode_variable(df_variables, 'Trainer_ID')  
            df_variables, away_trainer_encoded = models.encode_variable(df_variables, 'Gegner_Trainer_ID')
            trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
        if 'HeimSystem' in variables:
            df_variables, home_system_encoded = models.encode_variable(df_variables, 'HeimSystem')  
            df_variables, away_system_encoded = models.encode_variable(df_variables, 'AuswärtsSystem')  
            system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
            
        
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
            
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
    
        if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = teams_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
            
            all_encoded_variables = trainer_encoded 
            
        if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
            
            all_encoded_variables = system_encoded  
            
        df_variables = df_variables.values
        df_dependant = df['Spiel_Ausgang'].ravel()   
        df_variables = np.concatenate((df_variables, all_encoded_variables), axis=1)
        
        X_train, X_test, y_train, y_test = models.split_data(df_variables, df_dependant, length)
        
        nbr_games = len(df_dependant)
        length_train_x = len(X_train)
        length_test_x = len(X_test)    
        
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.fit_transform(X_test)

        y_categorical_train = np_utils.to_categorical(y_train, num_classes=2)
        score, recall, precision = models.ann_score(X_train, X_test, y_categorical_train, y_test, uniques, epochs, batch_size, learning_rate, nbr_layers)

        
        return render(request, 'Test_Methods/method_performance_premierleague_ann_result.html', {                                                                                                      'nbr_games':nbr_games, 
                                                                            'length_train_x':length_train_x,
                                                                            'length_test_x':length_test_x,
                                                                            'score':score,
                                                                            'recall':recall,
                                                                            'precision':precision,
                                                                            'variables':variables
#                                                                            'score_binary':score_binary,
#                                                                            'recall_binary':recall_binary,
#                                                                            'precision_binary':precision_binary
                                                                                })
    else:
       return render(request, 'Test_Methods/app_choice.html')   
   
    
def get_balance_per_team(total, home_teams, away_teams):
    
    right = []
    wrong = []
    for outcome in range(len(total)):
        if total[total] > 0:
            right.append(home_teams[outcome])
            right.append(home_teams[away_teams])
        else:
            wrong.append(home_teams[outcome])
            wrong.append(home_teams[away_teams])            
    return right, wrong



def random_forest_results_odds_against_bookmaker(request):

    if request.GET.get('randomforest_against_bookmaker') == 'randomforest_against_bookmaker':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag_from = int(request.GET.get('From'))
        spieltag_to = int(request.GET.get('To'))
        n = int(request.GET.get('TreeNumber'))
        Criterion = request.GET.get('Criterion')
        
        df = models.get_training_data()
        
        variables = models.check_startelf(variables)
            
        total, df_best_clubs_home, df_odds_home, df_spieltage = models.random_forest_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, n, Criterion)
        total_sum = sum(total)
        score = round(np.sum(np.array(total) >= 0)/len(total), 2)
        
        grouped = df_best_clubs_home.groupby(by=["Home_Team"]).sum()

        balance = grouped['Balance'].tolist()
        best_clubs = df_best_clubs_home['Home_Team'].drop_duplicates().tolist()
      
        best_clubs = json.dumps(best_clubs)
        balance = json.dumps(balance)
        
        best_odds = models.group_by_odds(df_odds_home) 
        grouped_oods = best_odds.groupby(by=["Odds_Threshold"]).sum()   
        
        balance_odds = grouped_oods['Balance'].tolist()
        odds = best_odds['Odds_Threshold'].drop_duplicates().tolist()
        
        odds = json.dumps(odds)
        balance_odds = json.dumps(balance_odds)
        
        
        grouped_spieltag = df_spieltage.groupby(by=["Spieltag"]).sum()
        spieltag = df_spieltage['Spieltag'].drop_duplicates().tolist()
        balance_spieltag = grouped_spieltag['Balance'].tolist()
        spieltag = json.dumps(spieltag)
        balance_spieltag = json.dumps(balance_spieltag)        
        return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_randomforest_result.html', {
                                                                                                        'total_sum':total_sum,
                                                                                                        'score':score, 
                                                                                                        'best_clubs':best_clubs, 
                                                                                                        'balance':balance,
                                                                                                        'balance_odds':balance_odds, 
                                                                                                        'odds':odds,
                                                                                                        'spieltag':spieltag, 
                                                                                                        'balance_spieltag':balance_spieltag,
                                                                                                        })
    else:
        return render(request, 'Test_Methods/app_choice.html')    



def random_forest_results_odds_against_bookmaker_premierleague(request):

    if request.GET.get('randomforest_against_bookmaker') == 'randomforest_against_bookmaker':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag_from = int(request.GET.get('From'))
        spieltag_to = int(request.GET.get('To'))
        n = int(request.GET.get('TreeNumber'))
        Criterion = request.GET.get('Criterion')
        
        df = models.get_premierleague_training_data()
        
            
        total, df_best_clubs_home, df_odds_home, df_spieltage = models.random_forest_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, n, Criterion)
        total_sum = sum(total)
        score = round(np.sum(np.array(total) >= 0)/len(total), 2)
        
        grouped = df_best_clubs_home.groupby(by=["Home_Team"]).sum()

        balance = grouped['Balance'].tolist()
        best_clubs = df_best_clubs_home['Home_Team'].drop_duplicates().tolist()
      
        best_clubs = json.dumps(best_clubs)
        balance = json.dumps(balance)
        
        best_odds = models.group_by_odds(df_odds_home) 
        grouped_oods = best_odds.groupby(by=["Odds_Threshold"]).sum()   
        
        balance_odds = grouped_oods['Balance'].tolist()
        odds = best_odds['Odds_Threshold'].drop_duplicates().tolist()
        
        odds = json.dumps(odds)
        balance_odds = json.dumps(balance_odds)
        
        
        grouped_spieltag = df_spieltage.groupby(by=["Spieltag"]).sum()
        spieltag = df_spieltage['Spieltag'].drop_duplicates().tolist()
        balance_spieltag = grouped_spieltag['Balance'].tolist()
        spieltag = json.dumps(spieltag)
        balance_spieltag = json.dumps(balance_spieltag)        
        return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_randomforest_result.html', {
                                                                                                        'total_sum':total_sum,
                                                                                                        'score':score, 
                                                                                                        'best_clubs':best_clubs, 
                                                                                                        'balance':balance,
                                                                                                        'balance_odds':balance_odds, 
                                                                                                        'odds':odds,
                                                                                                        'spieltag':spieltag, 
                                                                                                        'balance_spieltag':balance_spieltag,
                                                                                                        })
    else:
        return render(request, 'Test_Methods/app_choice.html')  
    
    
def ann_results_odds_against_bookmaker(request):

    if request.GET.get('ann_against_bookmaker') == 'ann_against_bookmaker':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag_from = int(request.GET.get('From'))
        spieltag_to = int(request.GET.get('To'))
        learning_rate = float(request.GET.get('LearningRate'))
        number_layers = int(request.GET.get('Layers'))
        
        df = models.get_training_data()
        
        variables = models.check_startelf(variables)
            #learning rate
        total, df_best_clubs_home, df_odds_home, df_spieltage = models.ann_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, learning_rate, number_layers)
        total_sum = sum(total)
        score = round(np.sum(np.array(total) >= 0)/len(total), 2)
        
        grouped = df_best_clubs_home.groupby(by=["Home_Team"]).sum()

        balance = grouped['Balance'].tolist()
        best_clubs = df_best_clubs_home['Home_Team'].drop_duplicates().tolist()
      
        best_clubs = json.dumps(best_clubs)
        balance = json.dumps(balance)
        
        best_odds = models.group_by_odds(df_odds_home) 
        grouped_oods = best_odds.groupby(by=["Odds_Threshold"]).sum()   
        
        balance_odds = grouped_oods['Balance'].tolist()
        odds = best_odds['Odds_Threshold'].drop_duplicates().tolist()
        
        odds = json.dumps(odds)
        balance_odds = json.dumps(balance_odds)
        
        
        grouped_spieltag = df_spieltage.groupby(by=["Spieltag"]).sum()
        spieltag = df_spieltage['Spieltag'].drop_duplicates().tolist()
        balance_spieltag = grouped_spieltag['Balance'].tolist()
        spieltag = json.dumps(spieltag)
        balance_spieltag = json.dumps(balance_spieltag)        
        return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_ann_results.html', {
                                                                                                        'total_sum':total_sum,
                                                                                                        'score':score, 
                                                                                                        'best_clubs':best_clubs, 
                                                                                                        'balance':balance,
                                                                                                        'balance_odds':balance_odds, 
                                                                                                        'odds':odds,
                                                                                                        'spieltag':spieltag, 
                                                                                                        'balance_spieltag':balance_spieltag,
                                                                                                        })
    else:
        return render(request, 'Test_Methods/app_choice.html')   
    

def ann_results_odds_against_bookmaker_premierleague(request):

    if request.GET.get('ann_against_bookmaker') == 'ann_against_bookmaker':

        variables = request.GET.getlist('selectvariables')

        saison = request.GET.get('Season')
        spieltag_from = int(request.GET.get('From'))
        spieltag_to = int(request.GET.get('To'))
        learning_rate = float(request.GET.get('LearningRate'))
        number_layers = int(request.GET.get('Layers'))
        
        df = models.get_premierleague_training_data()
        
        total, df_best_clubs_home, df_odds_home, df_spieltage = models.ann_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, learning_rate, number_layers)
        total_sum = sum(total)
        score = round(np.sum(np.array(total) >= 0)/len(total), 2)
        
        grouped = df_best_clubs_home.groupby(by=["Home_Team"]).sum()

        balance = grouped['Balance'].tolist()
        best_clubs = df_best_clubs_home['Home_Team'].drop_duplicates().tolist()
      
        best_clubs = json.dumps(best_clubs)
        balance = json.dumps(balance)
        
        best_odds = models.group_by_odds(df_odds_home) 
        grouped_oods = best_odds.groupby(by=["Odds_Threshold"]).sum()   
        
        balance_odds = grouped_oods['Balance'].tolist()
        odds = best_odds['Odds_Threshold'].drop_duplicates().tolist()
        
        odds = json.dumps(odds)
        balance_odds = json.dumps(balance_odds)
        
        
        grouped_spieltag = df_spieltage.groupby(by=["Spieltag"]).sum()
        spieltag = df_spieltage['Spieltag'].drop_duplicates().tolist()
        balance_spieltag = grouped_spieltag['Balance'].tolist()
        spieltag = json.dumps(spieltag)
        balance_spieltag = json.dumps(balance_spieltag)        
        return render(request, 'Test_Methods/method_odds_against_bookmaker_bundesliga_ann_results.html', {
                                                                                                        'total_sum':total_sum,
                                                                                                        'score':score, 
                                                                                                        'best_clubs':best_clubs, 
                                                                                                        'balance':balance,
                                                                                                        'balance_odds':balance_odds, 
                                                                                                        'odds':odds,
                                                                                                        'spieltag':spieltag, 
                                                                                                        'balance_spieltag':balance_spieltag,
                                                                                                        })
    else:
        return render(request, 'Test_Methods/app_choice.html')    

def get_mutual_information(request):

    if request.GET.get('mutual_information') == 'mutual_information':

        variables = request.GET.getlist('selectvariables')
        sample_size = float(request.GET.get('SampleSize'))
        
        df = models.get_training_data()

        y = df[['Spiel_Ausgang']]
        df = df.drop('Spiel_Ausgang', axis =1)
        
        variables = models.check_startelf(variables)
        
        X = df[variables]
        X_train, X_test, y_train, y_test = models.split_train(X, y, sample_size)
        test_size = len(X_train)
        mutual_info = mutual_info_classif(X_train.values, y_train.values)
        
        mutual_info = pd.Series(mutual_info)
        mutual_info.index = X.columns
        
        fig = plt.figure()
        mutual_info.sort_values(ascending=False).plot.bar(figsize=(15,10))
        plt.ylabel('Mutual Information')
        plt.xlabel('xlabel', fontsize=10)   
        plt.subplots_adjust(bottom=0.3)
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return render(request, 'Test_Methods/method_mutual_info_bundesliga_results.html', {'data':data, 'test_size':test_size})
    else:
       return render(request, 'Test_Methods/app_choice.html')
   
    
def get_mutual_information_premierleague(request):

    if request.GET.get('mutual_information') == 'mutual_information':

        variables = request.GET.getlist('selectvariables')
        sample_size = float(request.GET.get('SampleSize'))
        
        df = models.get_premierleague_training_data()

        y = df[['Spiel_Ausgang']]
        df = df.drop('Spiel_Ausgang', axis =1)
              
        X = df[variables]
        X_train, X_test, y_train, y_test = models.split_train(X, y, sample_size)
        test_size = len(X_train)
        mutual_info = mutual_info_classif(X_train.values, y_train.values)
        
        mutual_info = pd.Series(mutual_info)
        mutual_info.index = X.columns
        
        fig = plt.figure()
        mutual_info.sort_values(ascending=False).plot.bar(figsize=(15,10))
        plt.ylabel('Mutual Information')
        plt.xlabel('xlabel', fontsize=10)   
        plt.subplots_adjust(bottom=0.3)
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return render(request, 'Test_Methods/method_mutual_info_premierleague_results.html', {'data':data, 'test_size':test_size})
    else:
       return render(request, 'Test_Methods/app_choice.html')

    
def get_tree_importance(request):

    if request.GET.get('tree_importance') == 'tree_importance':
        
        df = models.get_training_data()
        
        variables = request.GET.getlist('selectvariables')
        sample_size = float(request.GET.get('SampleSize'))
        variables = models.check_startelf(variables)
        selected_features, df_features = models.get_tree_importance(variables, sample_size, df)

        importance = df_features['Importance'].tolist()
        features = df_features['Features'].tolist()
      
        importance = json.dumps(importance)
        features = json.dumps(features)
        return render(request, 'Test_Methods/method_tree_importance_bundesliga_results.html', {'selected_features':selected_features,
                                                                                               'importance':importance,
                                                                                               'features':features})
    else:
       return render(request, 'Test_Methods/method_tree_importance_bundesliga.html')
   
def get_tree_importance_premierleague(request):

    if request.GET.get('tree_importance') == 'tree_importance':
        
        df = models.get_premierleague_training_data()
        
        variables = request.GET.getlist('selectvariables')
        sample_size = float(request.GET.get('SampleSize'))
        variables = models.check_startelf(variables)
        selected_features, df_features = models.get_tree_importance(variables, sample_size, df)
        
        importance = df_features['Importance'].tolist()
        features = df_features['Features'].tolist()
      
        importance = json.dumps(importance)
        features = json.dumps(features)   
        
        return render(request, 'Test_Methods/method_tree_importance_premierleague_results.html', {'selected_features':selected_features,
                                                                                                  'importance':importance,
                                                                                                  'features':features})
    else:
       return render(request, 'Test_Methods/method_tree_importance_premierleague.html')




def get_correlation(request):

    if request.GET.get('tree_importance') == 'tree_importance':
        
        df = models.get_training_data()
        
        variable = request.GET.getlist('selectvariables_1')
        correlated_to = request.GET.getlist('selectvariables_2')
        variables_to_check = variable + correlated_to
        sample_size = float(request.GET.get('SampleSize'))
        cor = models.get_correlation_variables(variables_to_check, sample_size, df)

        return HttpResponse(cor.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_correlation_premierleague(request):

    if request.GET.get('tree_importance') == 'tree_importance':
        
        df = models.get_premierleague_training_data()
        
        variable = request.GET.getlist('selectvariables_1')
        correlated_to = request.GET.getlist('selectvariables_2')
        variables_to_check = variable + correlated_to
        sample_size = float(request.GET.get('SampleSize'))
        cor = models.get_correlation_variables(variables_to_check, sample_size, df)

        return HttpResponse(cor.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_premierleague.html')
   
    
def get_step_forward(request):

    if request.GET.get('step_forward') == 'step_forward':
        
        df = models.get_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features = int(request.GET.get('nbr_features'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_forward = models.forward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring)

        return HttpResponse(step_forward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_step_backward(request):

    if request.GET.get('step_forward') == 'step_backward':
        
        df = models.get_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features = int(request.GET.get('nbr_features'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_backward = models.backward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring)

        return HttpResponse(step_backward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_step_forward_premierleague(request):

    if request.GET.get('step_forward') == 'step_forward':
        
        df = models.get_premierleague_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features = int(request.GET.get('nbr_features'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_forward = models.forward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring)

        return HttpResponse(step_forward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_step_backward_premierleague(request):

    if request.GET.get('step_forward') == 'step_backward':
        
        df = models.get_premierleague_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features = int(request.GET.get('nbr_features'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_forward = models.backward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring)

        return HttpResponse(step_forward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
    
def get_exhaustive(request):

    if request.GET.get('exhaustive') == 'exhaustive':
        
        df = models.get_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features_min = int(request.GET.get('nbr_features_min'))
        nbr_features_max = int(request.GET.get('nbr_features_max'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_forward = models.exhaustive_feature_selection(X, y, nbr_features_min, nbr_features_max, test_size, nbr_trees, scoring)

        return HttpResponse(step_forward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_exhaustive_premierleague(request):

    if request.GET.get('exhaustive') == 'step_backward':
        
        df = models.get_premierleague_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
        
        
        nbr_features_min = int(request.GET.get('nbr_features_min'))
        nbr_features_max = int(request.GET.get('nbr_features_max'))
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        scoring = request.GET.get('scoring')
        
        step_forward = models.exhaustive_feature_selection(X, y, nbr_features_min, nbr_features_max, test_size, nbr_trees, scoring)

        return HttpResponse(step_forward.to_html())
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_gradient_boost(request):

    if request.GET.get('gradient_boost') == 'gradient_boost':
        
        df = models.get_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
    
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        
        df_gradient_boost_importance, chosen_features = models.get_gradient_boost_importance(X, y, test_size, nbr_trees)
        
        importance = df_gradient_boost_importance['Importance'].tolist()
        features = df_gradient_boost_importance['Features'].tolist()
      
        importance = json.dumps(importance)
        features = json.dumps(features)
        
        return render(request, 'Test_Methods/method_gradient_boost_bundesliga_results.html', {'importance':importance,
                                                                                              'features':features,
                                                                                              'chosen_features':chosen_features

                                                                                                        })
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')
   
def get_gradient_boost_premierleague(request):

    if request.GET.get('gradient_boost') == 'gradient_boost':
        
        df = models.get_premierleague_training_data()
        variables = request.GET.getlist('selectvariables')
        
        y = df[['Spiel_Ausgang']]
        X = df[variables]        
    
        test_size = float(request.GET.get('test_size'))
        nbr_trees = int(request.GET.get('nbr_trees'))
        
        df_gradient_boost_importance, chosen_features = models.get_gradient_boost_importance(X, y, test_size, nbr_trees)
        
        importance = df_gradient_boost_importance['Importance'].tolist()
        features = df_gradient_boost_importance['Features'].tolist()
      
        importance = json.dumps(importance)
        features = json.dumps(features)
        
        return render(request, 'Test_Methods/method_gradient_boost_premierleague_results.html', {'importance':importance,
                                                                                              'features':features,
                                                                                              'chosen_features': chosen_features

                                                                                                        })
        #return render(request, 'Test_Methods/method_correlation_bundesliga_results.html', {'cor':cor})
    else:
       return render(request, 'Test_Methods/method_correlation_bundesliga.html')