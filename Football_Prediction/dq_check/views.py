from django.shortcuts import render
from dq_check import models
# Create your views here.
from django.http import HttpResponse



def dq(request):
    return render(request, 'dq_check/dq_query.html')

def bundesliga_all_check_matchday(request):

    if request.GET.get('check_matchday_bl1') == 'check_matchday_bl1':
    
        df = models.get_bundesliga_all_saison_spieltag_check()

        return HttpResponse(df.to_html())
    else:
       return render(request, 'dq_check/dq_query.html')
   
def premierleague_all_check_matchday(request):

    if request.GET.get('check_matchday_pl') == 'check_matchday_pl':
    
        df = models.get_premierleague_all_saison_spieltag_check()

        return HttpResponse(df.to_html())
    else:
       return render(request, 'dq_check/dq_query.html')   
   
def bundesliga_all_check_clubs(request):

    if request.GET.get('check_club_nbr_bl1') == 'check_club_nbr_bl1':
    
        df = models.get_bundesliga_all_club_count()

        return HttpResponse(df.to_html())
    else:
       return render(request, 'dq_check/dq_query.html')
   
def premierleague_all_check_clubs(request):

    if request.GET.get('check_club_nbr_pl') == 'check_club_nbr_pl':
    
        df = models.get_premierleague_all_club_count()

        return HttpResponse(df.to_html())
    else:
       return render(request, 'dq_check/dq_query.html')   


