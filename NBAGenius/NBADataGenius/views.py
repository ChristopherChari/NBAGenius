from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame


# Create your views here.
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import commonallplayers



def home(request):
    return render(request, "home.html")


def players_list(request):
    # Create an instance of CommonAllPlayers
    all_players = commonallplayers.CommonAllPlayers()
    
    # Fetch player data
    player_data = all_players.get_data_frames()[0]
    
    # Extract player IDs
    player_ids = player_data['PERSON_ID'].tolist()
    
    # Render the template with player IDs
    return render(request, 'players_list.html', {'player_ids': player_ids})

def player_profile(request, player_id):
    # Use the commonplayerinfo endpoint to get detailed information about a specific player
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_response = player_info.get_data_frames()[0]
    player = player_info_response.to_dict(orient='records')[0]
    return render(request, 'player_profile.html', {'player': player})
