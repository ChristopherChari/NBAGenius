from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
from nba_api.stats.endpoints import commonplayerinfo
from django.http import JsonResponse
from nba_api.stats.static import players as nba_players
import requests
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from .models import Player, CommonPlayerInfo  # Assuming you have a Player model defined
from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import PlayerDashboardByYearOverYear, LeagueDashPlayerStats, LeagueDashPtStats, LeagueDashPtDefend
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.matchupsrollup import MatchupsRollup
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats import endpoints
from nba_api.stats.endpoints import SynergyPlayTypes, leaguedashplayerstats, LeagueHustleStatsPlayer
from nba_api.stats.endpoints import leaguedashptdefend
import pandas as pd
import numpy as np
import json


def home(request):
    return render(request, "home.html")

def player_list(request):
    search_query = request.GET.get('search', '').strip()
    all_nba_players = nba_players.get_players()

    # Filter active players if the search query is provided
    filtered_players = [
        player for player in all_nba_players
        if search_query.lower() in player['full_name'].lower() and player['is_active']
    ]

    # If this is an AJAX request, only return JSON data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        players_data = [{
            'id': player['id'],
            'full_name': player['full_name'],
            'image_url': f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player['id']}.png"
        } for player in filtered_players]
        return JsonResponse({'players': players_data})

    # Otherwise, return full page with context
    players = [{'id': player['id'], 'full_name': player['full_name'], 'status': 'Active'} for player in filtered_players]
    context = {'players': players}
    return render(request, 'player_list.html', context)

def calculate_player_rates(player_id):
    try:
        # Fetch data from the LeagueDashPlayerStats endpoint
        player_stats = LeagueDashPlayerStats(measure_type_detailed_defense='Base')
        player_stats_data = player_stats.get_normalized_dict()['LeagueDashPlayerStats']

        # Initialize lists to store FTAR and 3PAR for all players
        ftar_list = []
        par_list = []
        player_ftar = None
        player_par = None

        # Iterate over player stats data to fill lists and find the specific player's rates
        for player_stat in player_stats_data:
            fta = player_stat['FTA']
            fga = player_stat['FGA']
            fg3a = player_stat['FG3A']

            # Calculate rates avoiding division by zero
            if fga > 0:
                ftar = (fta / fga) * 100
                par = (fg3a / fga) * 100
                ftar_list.append(ftar)  # Only add to list if valid
                par_list.append(par)    # Only add to list if valid
            else:
                ftar = None
                par = None

            # Check if this is the player we're interested in
            if player_stat['PLAYER_ID'] == player_id:
                player_ftar = round(ftar,1)
                player_par = round(par,1)

        # Calculate percentiles if the player's data was found
        if player_ftar is not None and player_par is not None:
            # Sort lists and calculate percentiles ignoring None values
            ftar_sorted = sorted([x for x in ftar_list if x is not None])
            par_sorted = sorted([x for x in par_list if x is not None])
            
            ftar_percentile = round((np.searchsorted(ftar_sorted, player_ftar) / len(ftar_sorted)) * 100, 1)
            par_percentile = round((np.searchsorted(par_sorted, player_par) / len(par_sorted)) * 100, 1)
            
            return {
                'FTAR': player_ftar,
                '3PAR': player_par,
                'FTAR_percentile': ftar_percentile,
                '3PAR_percentile': par_percentile
            }
        else:
            print("Player ID not found in data or player data is incomplete.")
            return None
    except Exception as e:
        print(f"Error calculating player rates and percentiles: {e}")
        return None

def calculate_rebound_and_defense_stats(player_id):
    try:
        # Fetch data from the LeagueDashPlayerStats endpoint
        player_stats = LeagueDashPlayerStats(per_mode_detailed='PerGame', measure_type_detailed_defense='Base')
        player_stats_data = player_stats.get_normalized_dict()['LeagueDashPlayerStats']

        # Initialize lists for each statistic for percentile calculation
        oreb_list, dreb_list, blk_list, stl_list = [], [], [], []
        player_data = {}

        # Collect stats from all players and identify the target player's stats
        for player_stat in player_stats_data:
            oreb = player_stat.get('OREB', 0)
            dreb = player_stat.get('DREB', 0)
            blk = player_stat.get('BLK', 0)
            stl = player_stat.get('STL', 0)

            # Append data to lists
            oreb_list.append(oreb)
            dreb_list.append(dreb)
            blk_list.append(blk)
            stl_list.append(stl)

            # Check if the current data belongs to the target player
            if player_stat['PLAYER_ID'] == player_id:
                player_data = {
                    'OREB': oreb,
                    'DREB': dreb,
                    'BLK': blk,
                    'STL': stl
                }

        # Calculate percentiles for the retrieved player stats
        for stat in ['OREB', 'DREB', 'BLK', 'STL']:
            stat_list = locals()[f"{stat.lower()}_list"]
            if stat_list:
                sorted_list = sorted(stat_list)
                if player_data.get(stat) is not None:
                    percentile_index = np.searchsorted(sorted_list, player_data[stat], side="right")
                    percentile = (percentile_index / len(sorted_list)) * 100
                    player_data[f"{stat}_percentile"] = round(percentile, 1)

        return player_data

    except Exception as e:
        print(f"Error calculating rebound and defense stats: {e}")
        return None

def calculate_player_efficiency(player_id):
    try:
        # Fetch data from the LeagueDashPtStats endpoint
        player_stats = LeagueDashPtStats(
            per_mode_simple='PerGame',
            player_or_team='Player',
            pt_measure_type='Efficiency'
        )
        player_stats_data = player_stats.get_normalized_dict()['LeagueDashPtStats']

        # Initialize variables and lists for player and all players' stats
        player_data = None
        drivepts_list, cnspts_list, pullupspts_list = [], [], []

        # Extract player data and populate lists for percentile calculation
        for player_stat in player_stats_data:
            if player_stat['PLAYER_ID'] == player_id:
                player_data = player_stat  # Save specific player's data
            # Collect data for percentile calculations
            if player_stat.get('DRIVE_PTS') is not None:
                drivepts_list.append(player_stat['DRIVE_PTS'])
            if player_stat.get('CATCH_SHOOT_PTS') is not None:
                cnspts_list.append(player_stat['CATCH_SHOOT_PTS'])
            if player_stat.get('PULL_UP_PTS') is not None:
                pullupspts_list.append(player_stat['PULL_UP_PTS'])

        if not player_data:
            print("Player not found in the data.")
            return None

        # Extract specific points from player data
        drive_points = player_data.get('DRIVE_PTS')
        shoot_points = player_data.get('CATCH_SHOOT_PTS')
        pull_up_points = player_data.get('PULL_UP_PTS')

        # Calculate percentiles
        def calc_percentile(data_list, value):
            if value is None:
                return None
            sorted_list = sorted(data_list)
            index = np.searchsorted(sorted_list, value)
            percentile = round((index / len(sorted_list)) * 100, 1)
            return percentile

        efficiency_data = {
            'Drive_points': drive_points,
            'Shoot_points': shoot_points,
            'pull_up_points': pull_up_points,
            'Drive_percentile': calc_percentile(drivepts_list, drive_points),
            'CNS_percentile': calc_percentile(cnspts_list, shoot_points),
            'pull_up_percentile': calc_percentile(pullupspts_list, pull_up_points)
        }
        return efficiency_data

    except Exception as e:
        print(f"Error calculating player efficiency and percentiles: {e}")
        return None

def get_league_stats_player(player_id):
    try:
        # Fetch data for all players
        response = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame")
        data = response.get_normalized_dict()
        
        if 'LeagueDashPlayerStats' in data:
            # Filter the data to find stats for the specific player
            player_stats = [item for item in data['LeagueDashPlayerStats'] if item['PLAYER_ID'] == player_id]
            return player_stats if player_stats else []
        else:
            print("No data found for any players.")
            return []
    except Exception as e:
        print(f"Error retrieving league stats for player {player_id}: {str(e)}")
        return []
    
def advanced_stats_player_percentile(player_id):
    try:
        response = endpoints.LeagueDashPlayerStats(
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Advanced"
        )
        data = response.get_normalized_dict()

        if 'LeagueDashPlayerStats' in data:
            players_data = data['LeagueDashPlayerStats']
            player_data = next((item for item in players_data if item['PLAYER_ID'] == player_id), None)
            
            if player_data:
                ts = round(player_data['TS_PCT'] * 100, 1)  # Assuming TS% is provided like this
                ast = round(player_data['AST_PCT'] * 100,1)  # Assuming AST% is provided like this

                ts_sorted = sorted([p['TS_PCT'] * 100 for p in players_data])
                ast_sorted = sorted([p['AST_PCT'] * 100 for p in players_data])

                ts_percentile = round((np.searchsorted(ts_sorted, ts) / len(ts_sorted)) * 100, 1)
                ast_percentile = round((np.searchsorted(ast_sorted, ast) / len(ast_sorted)) * 100, 1)

                return {
                    'player_ts': ts,
                    'player_ast': ast,
                    'ts_percentile': ts_percentile,
                    'ast_percentile': ast_percentile
                }
            else:
                print("Player not found in the data.")
        else:
            print("Unexpected response format.")
        return {}

    except Exception as e:
        print(f"Error retrieving league advanced stats player data: {e}")
        return {}
    
def get_league_advanced_stats_player(player_id):
    try:
        # Fetch data for all players with advanced metrics
        response = leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense="Advanced", per_mode_detailed="PerGame")
        data = response.get_normalized_dict()
        
        if 'LeagueDashPlayerStats' in data:
            # Filter the data to find advanced stats for the specific player
            player_stats = [item for item in data['LeagueDashPlayerStats'] if item['PLAYER_ID'] == player_id]
            return player_stats if player_stats else []
        else:
            print("No advanced data found for any players.")
            return []
    except Exception as e:
        print(f"Error retrieving advanced league stats for player {player_id}: {str(e)}")
        return []
    
def format_stat_name(name):
    return ' '.join(word.capitalize() for word in name.split('_'))



def calculate_defensive_metrics(player_id):
    try:
        response = leaguedashptdefend.LeagueDashPtDefend(
            per_mode_simple='PerGame',
            defense_category='Less Than 6Ft',
            league_id='00',
            season_type_all_star='Regular Season'
        )

        defense_data = response.get_normalized_dict()
        players_data = defense_data['LeagueDashPTDefend']

        # Extracting data ensuring no null values are processed
        freq_list = [float(player['FREQ']) for player in players_data if 'FREQ' in player and player['FREQ'] is not None]
        d_fg_pct_list = [float(player['PLUSMINUS']) for player in players_data if 'PLUSMINUS' in player and player['PLUSMINUS'] is not None]

        # Convert all values to percentage
        freq_list_percent = [x * 100 for x in freq_list]
        d_fg_pct_list_percent = [x * 100 for x in d_fg_pct_list]

        player_data = next((item for item in players_data if item['CLOSE_DEF_PERSON_ID'] == player_id), None)

        if player_data:
            player_freq = round(float(player_data['FREQ']) * 100, 1)
            player_d_fg_pct = round(float(player_data['PLUSMINUS']) * 100, 1)
            player_age = int(round(player_data['AGE'], 0))

            # Calculate percentiles using sorted lists and searchsorted
            freq_percentile = round((np.searchsorted(sorted(freq_list_percent), player_freq) / len(freq_list_percent)) * 100, 1)
            d_fg_pct_percentile = 100 - round((np.searchsorted(sorted(d_fg_pct_list_percent), player_d_fg_pct) / len(d_fg_pct_list_percent)) * 100, 1)

            result = {
                'Rim_Frequency': player_freq,
                'Rim_Defense': player_d_fg_pct,
                'freq_percentile': freq_percentile,
                'd_fg_pct_percentile': d_fg_pct_percentile,
                'age' : player_age
            }
            return result
        else:
            print(f"Player with ID {player_id} not found in defensive stats.")
            return None

    except Exception as e:
        print(f"Error in calculate_defensive_metrics: {e}")
        return None



def get_league_hustle_stats_player(player_id):
    try:
        response = LeagueHustleStatsPlayer(per_mode_time="PerGame")
        hustle_stats = response.get_normalized_dict()['HustleStatsPlayer']

        player_hustle_stats = None
        metrics = {
            'DEFLECTIONS': [],
            'SCREEN_ASSISTS': [],
            'CONTESTED_SHOTS': [],
            'LOOSE_BALLS_RECOVERED': []
        }

        for player in hustle_stats:
            for key in metrics:
                if player[key] is not None:
                    metrics[key].append(player[key])
            if player['PLAYER_ID'] == player_id:
                player_hustle_stats = player

        if player_hustle_stats:
            percentiles = {}
            hustle_data = {}
            for key in metrics:
                if player_hustle_stats[key] is not None:
                    sorted_data = sorted(metrics[key])
                    value = player_hustle_stats[key]
                    index = np.searchsorted(sorted_data, value, side='right')
                    percentile = (index / len(sorted_data)) * 100
                    percentiles[key] = round(percentile, 1)
                    hustle_data[key] = {
                        'value': value,
                        'percentile': percentiles[key]
                    }
            
            return hustle_data
        else:
            print("Player not found in the data.")
            return {}
       
    except Exception as e:
        print(f"Error retrieving league hustle stats player data: {str(e)}")
        return {}
    
def get_synergy_playtype_data(player_id):
    try:
        play_types = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollman', 'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound', 'Misc']
        all_data = []

        # Fetch all play types at once if the API allows, otherwise loop through each
        for play_type in play_types:
            response = SynergyPlayTypes(
                play_type_nullable=play_type,
                player_or_team_abbreviation='P',
                type_grouping_nullable='Offensive'  # Ensure to specify the season or other required parameters
            ).get_normalized_dict()

            # Check if response contains SynergyPlayType data
            playtype_data = response.get('SynergyPlayType', [])
            for item in playtype_data:
                if item['PLAYER_ID'] == player_id:  # Match based on player ID directly
                    all_data.append({
                        'play_type': play_type,
                        **item  # Expand all other data of the play type into the dictionary
                    })
        return all_data

    except Exception as e:
        print(f"Error retrieving synergy playtype data for player ID {player_id}: {e}")
        return None
    
def player_profile(request, player_id):
    try:
        # Retrieve player information from the NBA API
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_dashboard = PlayerDashboardByYearOverYear(per_mode_detailed='PerGame', player_id=player_id)
        player_dashboard_advanced = PlayerDashboardByYearOverYear(player_id=player_id, measure_type_detailed='Advanced')
        matchup_rollups = MatchupsRollup(def_player_id_nullable=player_id)
        synergy_data = get_synergy_playtype_data(player_id)
        hustle_data = get_league_hustle_stats_player(player_id)
        advanced_league_data = get_league_advanced_stats_player(player_id)
        advanced_percentile_data = advanced_stats_player_percentile(player_id)
        basic_league_data = get_league_stats_player(player_id)
        player_rate_data = calculate_player_rates(player_id)
        effiency_data = calculate_player_efficiency(player_id)
        defensive_data = calculate_defensive_metrics(player_id) # Check output in the console
        player_randd_data = calculate_rebound_and_defense_stats(player_id)




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
                'player_rate_data': player_rate_data,
                'player_stats': player_stats,
                'player_dashboard': player_dashboard_data,
                'advanced_stats': advanced_stats,
                'matchup_rollups': matchup_rollups_data,
                'synergy_data': synergy_data,
                'hustle_data' : hustle_data,
                'advanced_data': advanced_percentile_data,
                'efficieny_data': effiency_data,
                'defensive_data' : defensive_data,
                'rebound_defense_data' : player_randd_data
            }
            return render(request, 'player_profile.html', context)
        else:
            # Player not found, render "player not found" template
            return render(request, 'player_not_found.html')
    except Exception as e:
        print(e)
        # Render "player not found" template if an exception occurs
        return render(request, 'player_not_found.html')
