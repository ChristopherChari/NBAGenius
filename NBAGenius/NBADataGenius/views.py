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
from django.shortcuts import render
from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import PlayerDashboardByYearOverYear, LeagueDashPlayerStats, LeagueDashPtStats
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.matchupsrollup import MatchupsRollup
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats import endpoints
from nba_api.stats.endpoints import SynergyPlayTypes, leaguedashplayerstats
import pandas as pd
import numpy as np
import json


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

def calculate_player_rates(player_id):
    # Fetch data from the LeagueDashPlayerStats endpoint
    player_stats = LeagueDashPlayerStats(
        measure_type_detailed_defense='Base'
    )
    player_stats_data = player_stats.get_normalized_dict()['LeagueDashPlayerStats']
    
    # Search for the specific player by their ID
    for player_stat in player_stats_data:
        if player_stat['PLAYER_ID'] == player_id:
            # Calculate free throw rate (FTAR) and three-point rate (3PAR) for the player
            fta = player_stat['FTA']
            fga = player_stat['FGA']
            fg3a = player_stat['FG3A']
            
            # Avoid division by zero
            if fga != 0:
                pftar = round((fta / fga) * 100, 1)
            else:
                pftar = None
            
            # Avoid division by zero
            if fga != 0:
                threepar = round((fg3a / fga) * 100, 1)
            else:
                threepar = None
            
            return {'FTAR': pftar, '3PAR': threepar}
    
    # Return None if the player ID is not found
    return None

def calculate_player_rates_percentile(player_id):
    try:
        # Fetch data from the LeagueDashPlayerStats endpoint
        player_stats = LeagueDashPlayerStats(measure_type_detailed_defense='Base')
        player_stats_data = player_stats.get_normalized_dict()['LeagueDashPlayerStats']

        # Initialize lists to store FTAR and 3PAR for all players
        ftar_list = []
        par_list = []

        # Iterate over player stats data
        for player_stat in player_stats_data:
            fta = player_stat['FTA']
            fga = player_stat['FGA']
            fg3a = player_stat['FG3A']

            # Avoid division by zero
            if fga != 0:
                ftar = (fta / fga) * 100
                par = (fg3a / fga) * 100
                ftar_list.append(ftar)
                par_list.append(par)

        # Calculate percentiles for FTAR and 3PAR
        pftar = calculate_player_rates(player_id)['FTAR']
        threepar = calculate_player_rates(player_id)['3PAR']

        ftar_percentile = round( (np.searchsorted(sorted(ftar_list), pftar) / len(ftar_list)) * 100, 1)
        par_percentile = round( (np.searchsorted(sorted(par_list), threepar) / len(par_list)) *100, 1)

        print("players free throw rate: ", pftar, " & ", ftar_percentile)
        print("players 3 point rate: ", threepar, " & ", par_percentile)

        return {'FTAR_percentile': ftar_percentile, '3PAR_percentile': par_percentile}
    
    except Exception as e:
        print("Error calculating player rates percentile:", e)
        return None

def get_league_stats_player(player_id):
    try:
        all_data = []
        # Retrieve hustle stats player data
        response = endpoints.LeagueDashPlayerStats(
            per_mode_detailed="PerGame"
        )

        # Get the JSON response
        response_json = response.get_json()

        # Convert JSON response to dictionary
        response_dict = json.loads(response_json)

        # Check if the response contains the expected structure
        if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
            # Filter the response for the specified player
            filtered_data = []
            for row in response_dict['resultSets'][0]['rowSet']:
                # Convert player_id to string before checking
                if str(player_id) in str(row[0]):  # Check if player_id exists in the row
                    filtered_data.append(row)

            # Add filtered data for this player to the list of all data
            all_data.extend(filtered_data)

        else:
            print("Unexpected response format.")

        return all_data

    except Exception as e:
        print("Error retrieving league hustle stats player data:", e)
        return None

# Function to retrieve player stats
def advanced_stats_player_percentile(player_id):
    try:
        # Retrieve hustle stats player data
        response = endpoints.LeagueDashPlayerStats(
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Advanced"
        )

        # Get the JSON response
        response_json = response.get_json()

        # Convert JSON response to dictionary
        response_dict = json.loads(response_json)

        

        # Check if the response contains the expected structure
        if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
            # Extract deflections data for all players
            trueshooting = [row[28] for row in response_dict['resultSets'][0]['rowSet']]

            # Find the player's row in the response data
            player_ts = None
            for row in response_dict['resultSets'][0]['rowSet']:
                if str(player_id) in str(row[0]):
                    player_ts = row[28]
                    break

            if player_ts is not None:
                # Calculate percentile
                ts_sorted = sorted(trueshooting)
                player_percentile = np.searchsorted(ts_sorted, player_ts) / len(ts_sorted)

                print("Player's ts percentile:", round(player_percentile*100, 1))
            else:
                print("Player not found in the data.")

        else:
            print("Unexpected response format.")

    except Exception as e:
        print("Error retrieving league hustle stats player data:", e)

def get_league_advanced_stats_player(player_id):
    try:
        all_data = []
        # Retrieve hustle stats player data
        response = endpoints.LeagueDashPlayerStats(
            measure_type_detailed_defense="Advanced",
            per_mode_detailed="PerGame"
        )

        # Get the JSON response
        response_json = response.get_json()

        # Convert JSON response to dictionary
        response_dict = json.loads(response_json)

        # Check if the response contains the expected structure
        if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
            # Filter the response for the specified player
            filtered_data = []
            for row in response_dict['resultSets'][0]['rowSet']:
                # Convert player_id to string before checking
                if str(player_id) in str(row[0]):  # Check if player_id exists in the row
                    filtered_data.append(row)

            # Add filtered data for this player to the list of all data
            all_data.extend(filtered_data)

        else:
            print("Unexpected response format.")

        return all_data

    except Exception as e:
        print("Error retrieving league hustle stats player data:", e)
        return None

def get_league_hustle_stats_player_percentile(player_id):
    try:
        # Retrieve hustle stats player data
        response = endpoints.LeagueHustleStatsPlayer(
            per_mode_time="Per36",
        )

        # Get the JSON response
        response_json = response.get_json()

        # Convert JSON response to dictionary
        response_dict = json.loads(response_json)

        # Check if the response contains the expected structure
        if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
            # Extract deflections data for all players
            deflections = [row[10] for row in response_dict['resultSets'][0]['rowSet']]

            # Find the player's row in the response data
            player_deflections = None
            for row in response_dict['resultSets'][0]['rowSet']:
                if str(player_id) in str(row[0]):
                    player_deflections = row[10]
                    break

            if player_deflections is not None:
                # Calculate percentile
                deflections_sorted = sorted(deflections)
                player_percentile = np.searchsorted(deflections_sorted, player_deflections) / len(deflections_sorted)

                print("Player's deflections percentile:", round(player_percentile*100, 1))
            else:
                print("Player not found in the data.")

        else:
            print("Unexpected response format.")

    except Exception as e:
        print("Error retrieving league hustle stats player data:", e)

def get_league_hustle_stats_player(player_id):
    try:
        all_data = []
        # Retrieve hustle stats player data
        response = endpoints.LeagueHustleStatsPlayer(
            per_mode_time="PerGame",
        )

        # Get the JSON response
        response_json = response.get_json()

        # Convert JSON response to dictionary
        response_dict = json.loads(response_json)

        # Check if the response contains the expected structure
        if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
            # Filter the response for the specified player
            filtered_data = []
            for row in response_dict['resultSets'][0]['rowSet']:
                # Convert player_id to string before checking
                if str(player_id) in str(row[0]):  # Check if player_id exists in the row
                    filtered_data.append(row)

            # Add filtered data for this player to the list of all data
            all_data.extend(filtered_data)

        else:
            print("Unexpected response format.")

        return all_data

    except Exception as e:
        print("Error retrieving league hustle stats player data:", e)
        return None
    
def get_synergy_playtype_data(player_id):
    try:
        play_types = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollman', 'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound', 'Misc']
        all_data = []

        for play_type in play_types:
            # Retrieve synergy playtype data for the specified player and play type
            response = endpoints.SynergyPlayTypes(
                play_type_nullable=play_type,
                player_or_team_abbreviation='P',
                type_grouping_nullable='Offensive',
            )

            # Get the JSON response
            response_json = response.get_json()

            # Convert JSON response to dictionary
            response_dict = json.loads(response_json)

            # Check if the response contains the expected structure
            if 'resultSets' in response_dict and len(response_dict['resultSets']) > 0:
                # Filter the response for the specified player
                filtered_data = []
                for row in response_dict['resultSets'][0]['rowSet']:
                    # Convert player_id to string before checking
                    if str(player_id) in str(row[1]):  # Check if player_id exists in the row
                        filtered_data.append(row)

                # Add filtered data for this play type to the list of all data
                all_data.extend(filtered_data)
            else:
                print("Unexpected response format for play type '{}':".format(play_type), response_dict)

        return all_data

    except Exception as e:
        print("Error retrieving synergy playtype data:", e)
        return None
    
def player_profile(request, player_id):
    try:
        # Retrieve player information from the NBA API
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

        # Retrieve player career stats from the NBA API with measure type set to 'Advanced'
        player_dashboard = PlayerDashboardByYearOverYear(per_mode_detailed='PerGame', player_id=player_id)
        player_dashboard_advanced = PlayerDashboardByYearOverYear(player_id=player_id, measure_type_detailed='Advanced')

        # Retrieve matchup rollups to see the percentage of time a player guards a position
        matchup_rollups = MatchupsRollup(def_player_id_nullable=player_id)

        # Get synergy playtype data for the specific player
        synergy_data = get_synergy_playtype_data(player_id)

        hustle_data = get_league_hustle_stats_player(player_id)
        hustle_percentile_data = get_league_hustle_stats_player_percentile(player_id)
        advanced_league_data = get_league_advanced_stats_player(player_id)
        advanced_percentile_data = advanced_stats_player_percentile(player_id)
        basic_league_data = get_league_stats_player(player_id)
        player_rate_data = calculate_player_rates_percentile(player_id)
        player_rate_data = calculate_player_rates(player_id)
        



        # Convert the responses to dictionary format
        player_info_dict = player_info.get_normalized_dict()
        player_dashboard_dict = player_dashboard.get_normalized_dict()
        player_dashboard_advanced_dict = player_dashboard_advanced.get_normalized_dict()
        matchup_rollups_dict = matchup_rollups.get_normalized_dict()

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

                # Turn into percentage
                for season_stats in player_dashboard_data:

                        for key in season_stats:
                            if key in ['FG_PCT', 'FG3_PCT', 'FT_PCT']:
                                season_stats[key] = round(season_stats[key] * 100, 1)

            # Extract advanced stats
            advanced_stats = None
            if player_dashboard_advanced_dict and 'ByYearPlayerDashboard' in player_dashboard_advanced_dict:
                advanced_stats = player_dashboard_advanced_dict['ByYearPlayerDashboard']

            # Extract matchup rollups data
            matchup_rollups_data = None
            if matchup_rollups_dict and 'MatchupsRollup' in matchup_rollups_dict:
                matchup_rollups_data = matchup_rollups_dict['MatchupsRollup']
            
            # Pass the player data, headline stats, dashboard stats, advanced stats, and matchup rollups to the template context
            context = {
                'player': player_data,
                'player_stats': player_stats,
                'player_dashboard': player_dashboard_data,
                'advanced_stats': advanced_stats,
                'matchup_rollups': matchup_rollups_data,
                'synergy_data': synergy_data,
                'hustle_data' : hustle_data
    
            }
            return render(request, 'player_profile.html', context)
        else:
            # Player not found, render "player not found" template
            return render(request, 'player_not_found.html')
    except Exception as e:
        print(e)
        # Render "player not found" template if an exception occurs
        return render(request, 'player_not_found.html')