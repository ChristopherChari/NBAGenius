from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
from nba_api.stats.endpoints import commonplayerinfo
import requests
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from .models import Player  # Assuming you have a Player model defined
from .models import Player, CommonPlayerInfo  # Assuming you have a Player model defined
import csv
from django.shortcuts import render
from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import PlayerDashboardByYearOverYear

from nba_api.stats.endpoints import commonallplayers


# Create your views here.




def home(request):
    return render(request, "home.html")



def player_list(request):
    # Retrieve all NBA players using nba_api
    all_nba_players = nba_players.get_players()

    # Process player data
    players = []
    for player in all_nba_players:
        # Assuming 'is_active' is not available directly from nba_api
        # You can add additional fields if needed
        players.append({
            'id': player['id'],
            'full_name': player['full_name'],
            'status': 'Active' if player['is_active'] else 'Inactive'
        })

    context = {
        'players': players
    }

    return render(request, 'player_list.html', context)


from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.playerdashboardbyyearoveryear import PlayerDashboardByYearOverYear

def player_profile(request, player_id):
    try:
        # Retrieve player information from the NBA API
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

        # Retrieve player career stats from the NBA API with measure type set to 'Advanced'
        player_dashboard = PlayerDashboardByYearOverYear(player_id=player_id)
        player_dashboard_Advanced = PlayerDashboardByYearOverYear(player_id=player_id, measure_type_detailed='Advanced')

        # Convert the responses to dictionary format
        player_info_dict = player_info.get_normalized_dict()
        player_dashboard_dict = player_dashboard.get_normalized_dict()
        player_dashboard_advanced_dict = player_dashboard_Advanced.get_normalized_dict()

        # Check if player data is found
        if player_info_dict and 'CommonPlayerInfo' in player_info_dict:
            # Extract player info from the response
            player_data = player_info_dict['CommonPlayerInfo'][0]

            # Extract player headline stats
            player_stats = None
            if 'PlayerHeadlineStats' in player_info_dict:
                player_stats = player_info_dict['PlayerHeadlineStats'][0]
                # Multiply PIE by 100
                if 'PIE' in player_stats:
                   player_stats['PIE'] =  round(player_stats['PIE'] * 100, 1)

            # Extract player dashboard stats
            player_dashboard_data = None
            if player_dashboard_dict and 'ByYearPlayerDashboard' in player_dashboard_dict:
                player_dashboard_data = player_dashboard_dict['ByYearPlayerDashboard']

                # Calculate Stats/GP
                for season_stats in player_dashboard_data:
                    if season_stats['GP'] != 0:
                        season_stats['MIN_PER_GP'] = round(season_stats['MIN'] / season_stats['GP'], 1)

                        for key in season_stats:
                            if key in ['FG_PCT', 'FG3_PCT', 'FT_PCT']:
                                season_stats[key] = round(season_stats[key] * 100, 1)

                        for key in season_stats:
                            if key in ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST',
                                       'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS']:
                                season_stats[key] = round(season_stats[key] / season_stats['GP'], 1)
                    else:
                        season_stats['MIN_PER_GP'] = 0

            # Extract advanced stats
            advanced_stats = None
            if  player_dashboard_advanced_dict and 'ByYearPlayerDashboard' in  player_dashboard_advanced_dict:
                advanced_stats =  player_dashboard_advanced_dict['ByYearPlayerDashboard']

            # Print advanced stats to console
            if advanced_stats:
                print("Advanced Stats:")
                print(advanced_stats)

            # Pass the player data, headline stats, dashboard stats, and advanced stats to the template context
            context = {
                'player': player_data,
                'player_stats': player_stats,
                'player_dashboard': player_dashboard_data,
                'advanced_stats': advanced_stats
            }
            return render(request, 'player_profile.html', context)
        else:
            # Player not found, render "player not found" template
            return render(request, 'player_not_found.html')
    except Exception as e:
        print(e)
        # Render "player not found" template if an exception occurs
        return render(request, 'player_not_found.html')