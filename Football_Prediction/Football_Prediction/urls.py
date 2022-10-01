"""Football_Prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Test_Methods import views as view_test
from dq_check import views as view_dq


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_test.main_page),
    path('methods/', view_test.method_performance),
    
    path('dq/', view_dq.dq),
    path('dq/bundesliga_all_check_matchday', view_dq.bundesliga_all_check_matchday, name='bundesliga_all_check_matchday'),
    path('dq/premierleague_all_check_matchday', view_dq.premierleague_all_check_matchday, name='premierleague_all_check_matchday'), 
    path('dq/bundesliga_all_check_clubs', view_dq.bundesliga_all_check_clubs, name='bundesliga_all_check_clubs'), 
    path('dq/premierleague_all_check_clubs', view_dq.premierleague_all_check_clubs, name='premierleague_all_check_clubs'),

    
    path('methods/leagues/', view_test.method_performance_league_choice),
    path('methods/leagues_odds/', view_test.method_odds_against_bookmaker_league_choice),
    path('methods/leagues_mutual_information/', view_test.method_mutual_information_league_choice),
    path('methods/leagues_tree_importance/', view_test.method_tree_importance_league_choice),
    path('methods/leagues_correlation/', view_test.method_correlation_league_choice),
    path('methods/leagues_step_forward/', view_test.method_step_forward_league_choice),
    path('methods/leagues_step_backward/', view_test.method_step_backward_league_choice),
    path('methods/leagues_exhaustive_search/', view_test.method_exhaustive_search_league_choice),
    path('methods/leagues_gradient_boost/', view_test.method_gradient_boost_league_choice),
    
    path('methods/leagues/bundesliga', view_test.method_performance_bundesliga_algorithm_choice),
    path('methods/leagues/premierleague', view_test.method_performance_premierleague_algorithm_choice),
    path('methods/leagues_odds/bundesliga', view_test.method_odds_against_bookmaker_bundesliga_algorithm_choice),
    path('methods/leagues_odds/premierleague', view_test.method_odds_against_bookmaker_premierleague_algorithm_choice),
    path('methods/leagues_mutual_information/bundesliga', view_test.method_mutual_information_bundesliga),
    path('methods/leagues_mutual_information/premierleague', view_test.method_mutual_information_premierleague),
    path('methods/leagues_tree_importance/bundesliga', view_test.method_tree_importance_bundesliga),
    path('methods/leagues_tree_importance/premierleague', view_test.method_tree_importance_premierleague),
    path('methods/leagues_correlation/bundesliga', view_test.method_correlation_bundesliga),
    path('methods/leagues_correlation/premierleague', view_test.method_correlation_premierleague),
    path('methods/leagues_step_forward/bundesliga', view_test.method_step_forward_bundesliga),
    path('methods/leagues_step_forward/premierleague', view_test.method_step_forward_premierleague),
    path('methods/leagues_step_backward/bundesliga', view_test.method_step_backward_bundesliga),
    path('methods/leagues_step_backward/premierleague', view_test.method_step_backward_premierleague),
    path('methods/leagues_exhaustive_search/bundesliga', view_test.method_exhaustive_search_bundesliga),
    path('methods/leagues_exhaustive_search/premierleague', view_test.method_exhaustive_search_premierleague),
    path('methods/leagues_gradient_boost/bundesliga', view_test.method_gradient_boost_bundesliga),
    path('methods/leagues_gradient_boost/premierleague', view_test.method_gradient_boost_premierleague),
    
    path('methods/leagues/bundesliga/randomforest', view_test.method_performance_bundesliga_randomforest),
    path('methods/leagues/premierleague/randomforest', view_test.method_performance_premierleague_randomforest),
    path('methods/leagues/bundesliga/ann', view_test.method_performance_bundesliga_ann),
    path('methods/leagues/premierleague/ann', view_test.method_performance_premierleague_ann),
    path('methods/leagues_odds/bundesliga/randomforest', view_test.method_odds_against_bookmaker_bundesliga_randomforest),
    path('methods/leagues_odds/premierleague/randomforest', view_test.method_odds_against_bookmaker_premierleague_randomforest),
    path('methods/leagues_odds/bundesliga/ann', view_test.method_odds_against_bookmaker_bundesliga_ann),
    path('methods/leagues_odds/premierleague/ann', view_test.method_odds_against_bookmaker_premierleague_ann),
    
    path('methods/leagues/bundesliga/randomforest/results', view_test.random_forest_results, name='random_forest_results'),
    path('methods/leagues/premierleague/randomforest/results', view_test.random_forest_premier_league_results, name='random_forest_premier_league_results'),
    path('methods/leagues/bundesliga/ann/results', view_test.ann_results, name='ann_results'),
    path('methods/leagues/premierleague/ann/results', view_test.ann_premierleague_results, name='ann_premierleague_results'),
    path('methods/leagues_odds/bundesliga/randomforest/results', view_test.random_forest_results_odds_against_bookmaker, name='random_forest_results_odds_against_bookmaker'),
    path('methods/leagues_odds/premierleague/randomforest/results', view_test.random_forest_results_odds_against_bookmaker_premierleague, name='random_forest_results_odds_against_bookmaker_premierleague'),
    path('methods/leagues_odds/bundesliga/ann/results', view_test.ann_results_odds_against_bookmaker, name='ann_results_odds_against_bookmaker'),
    path('methods/leagues_odds/premierleague/ann/results', view_test.ann_results_odds_against_bookmaker_premierleague, name='ann_results_odds_against_bookmaker_premierleague'),
    path('methods/leagues_mutual_information/bundesliga/results', view_test.get_mutual_information, name='get_mutual_information'),
    path('methods/leagues_mutual_information/premierleague/results', view_test.get_mutual_information_premierleague, name='get_mutual_information_premierleague'),
    path('methods/leagues_tree_importance/bundesliga/results', view_test.get_tree_importance, name='get_tree_importance'),
    path('methods/leagues_tree_importance/premierleague/results', view_test.get_tree_importance_premierleague, name='get_tree_importance_premierleague'),
    path('methods/leagues_correlation/bundesliga/results', view_test.get_correlation, name='get_correlation'),
    path('methods/leagues_correlation/premierleague/results', view_test.get_correlation_premierleague, name='get_correlation_premierleague'),
    path('methods/leagues_step_forward/bundesliga/results', view_test.get_step_forward, name='get_step_forward'),
    path('methods/leagues_step_forward/bundesliga/premierleague', view_test.get_step_forward_premierleague, name='get_step_forward_premierleague'),
    path('methods/leagues_step_backward/bundesliga/results', view_test.get_step_backward, name='get_step_backward'),
    path('methods/leagues_step_backwardward/bundesliga/premierleague', view_test.get_step_backward_premierleague, name='get_step_backward_premierleague'),
    path('methods/leagues_exhaustive_search/bundesliga/results', view_test.get_exhaustive, name='get_exhaustive'),
    path('methods/leagues_exhaustive_search/bundesliga/premierleague', view_test.get_exhaustive_premierleague, name='get_exhaustive_premierleague'),
    path('methods/leagues_gradient_boost/bundesliga/results', view_test.get_gradient_boost, name='get_gradient_boost'),
    path('methods/leagues_gradient_boost/premierleague/results', view_test.get_gradient_boost_premierleague, name='get_gradient_boost_premierleague'),
]
