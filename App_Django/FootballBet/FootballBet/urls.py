"""FootballBet URL Configuration

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
from RandomForestApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page),
    path('Methods/', views.methods, name='methods'),
    path('Methods/ForecastLeagues/', views.forecast_leagues, name='forecast_leagues'), 
    path('Methods/ForecastLeagues/RandomForest/', views.randomforest, name='RandomForest'), 
    path('Methods/ForecastLeagues/RandomForestPremierLeague/', views.randomforest_premierleague, name='randomforest_premierleague'), 
    path('random_forest_results_premier_league/', views.random_forest_results_premier_league, name='random_forest_results_premier_league'),
    path('random_forest_results/', views.random_forest_results, name='random_forest_results'),
    path('Dataquality/', views.dataquality_leagues, name='dataquality_leagues'),
    path('Dataquality/PremierLeauge/', views.dq_premierleauge, name='dq_premierleauge'),
    path('Dataquality/Bundesliga/', views.dq_bundesliga, name='dq_bundesliga'),
    path('Dataquality/PremierLeauge/Duplicates', views.dq_premierleauge_duplicates, name='dq_premierleauge_duplicates'),
    path('Dataquality/PremierLeauge/Matchdays', views.dq_premierleauge_matchdays, name='dq_premierleauge_matchdays'),
    path('Dataquality/PremierLeauge/Clubs', views.dq_premierleauge_clubs, name='dq_premierleauge_clubs'),
    path('Dataquality/Bundesliga/Duplicates', views.dq_bundesliga_duplicates, name='dq_bundesliga_duplicates'),
    path('Dataquality/Bundesliga/Matchdays', views.dq_bundesliga_matchdays, name='dq_bundesliga_matchdays'),
    path('Dataquality/Bundesliga/Clubs', views.dq_bundesliga_clubs, name='dq_bundesliga_clubs'),
    path('Dataquality/PremierLeauge/dq_results', views.check_duplicates_premierleague, name='check_duplicates_premierleague'),
    path('Dataquality/PremierLeauge/dq_results_matchdays', views.check_matchdays_premierleague, name='check_matchdays_premierleague'),
    path('Dataquality/PremierLeauge/dq_results_clubs', views.check_clubs_premier_league, name='check_clubs_premier_league'),
    path('Dataquality/Bundesliga/dq_results', views.check_duplicates_bundesliga, name='check_duplicates_bundesliga'),
    path('Dataquality/Bundesliga/dq_results_bundesliga_matchdays', views.check_matchdays_bundesliga, name='check_matchdays_bundesliga'),
    path('Dataquality/Bundesliga/dq_results_bundesliga_clubs', views.check_clubs_bundesliga, name='check_clubs_bundesliga'),
    path('Featurecheck/', views.feature_check_leagues, name='feature_check_leagues'),
    path('Featurecheck/Bundesliga/', views.feature_check_bundesliga, name='feature_check_bundesliga'),
    path('Featurecheck/Bundesliga/OddsVsBookamker/', views.feature_check_odds_vs_bookmaker_method, name='feature_check_odds_vs_bookmaker_method'), 
    path('Featurecheck/Bundesliga/Score/', views.feature_check_score_method, name='feature_check_score_method'), 
    path('Featurecheck/Bundesliga/OddsVsBookamker/RandomForest', views.feature_check_odds_vs_bookmaker, name='feature_check_odds_vs_bookmaker'),
    path('Featurecheck/Bundesliga/Score/RandomForest', views.feature_check_score_randomforest, name='feature_check_score_randomforest'), 
    path('Featurecheck/Bundesliga/OddsVsBookamker/Method/RandomForest/Results', views.get_random_forest_odds_vs_bookmaker, name='get_random_forest_odds_vs_bookmaker'),
    path('Featurecheck/Bundesliga/OddsVsBookamker/Method/RandomForest/Results', views.get_random_forest_score, name='get_random_forest_score')
    ]
