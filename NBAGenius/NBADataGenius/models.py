# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CommonPlayerInfo(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    display_first_last = models.TextField(blank=True, null=True)
    display_last_comma_first = models.TextField(blank=True, null=True)
    display_fi_last = models.TextField(blank=True, null=True)
    player_slug = models.TextField(blank=True, null=True)
    birthdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    school = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    last_affiliation = models.TextField(blank=True, null=True)
    height = models.TextField(blank=True, null=True)
    weight = models.TextField(blank=True, null=True)
    season_exp = models.FloatField(blank=True, null=True)
    jersey = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    rosterstatus = models.TextField(blank=True, null=True)
    games_played_current_season_flag = models.TextField(blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    team_name = models.TextField(blank=True, null=True)
    team_abbreviation = models.TextField(blank=True, null=True)
    team_code = models.TextField(blank=True, null=True)
    team_city = models.TextField(blank=True, null=True)
    playercode = models.TextField(blank=True, null=True)
    from_year = models.FloatField(blank=True, null=True)
    to_year = models.FloatField(blank=True, null=True)
    dleague_flag = models.TextField(blank=True, null=True)
    nba_flag = models.TextField(blank=True, null=True)
    games_played_flag = models.TextField(blank=True, null=True)
    draft_year = models.TextField(blank=True, null=True)
    draft_round = models.TextField(blank=True, null=True)
    draft_number = models.TextField(blank=True, null=True)
    greatest_75_flag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_player_info'


class DraftCombineStats(models.Model):
    season = models.TextField(blank=True, null=True)
    player_id = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    player_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    height_wo_shoes = models.FloatField(blank=True, null=True)
    height_wo_shoes_ft_in = models.TextField(blank=True, null=True)
    height_w_shoes = models.FloatField(blank=True, null=True)
    height_w_shoes_ft_in = models.TextField(blank=True, null=True)
    weight = models.TextField(blank=True, null=True)
    wingspan = models.FloatField(blank=True, null=True)
    wingspan_ft_in = models.TextField(blank=True, null=True)
    standing_reach = models.FloatField(blank=True, null=True)
    standing_reach_ft_in = models.TextField(blank=True, null=True)
    body_fat_pct = models.TextField(blank=True, null=True)
    hand_length = models.TextField(blank=True, null=True)
    hand_width = models.TextField(blank=True, null=True)
    standing_vertical_leap = models.FloatField(blank=True, null=True)
    max_vertical_leap = models.FloatField(blank=True, null=True)
    lane_agility_time = models.FloatField(blank=True, null=True)
    modified_lane_agility_time = models.FloatField(blank=True, null=True)
    three_quarter_sprint = models.FloatField(blank=True, null=True)
    bench_press = models.FloatField(blank=True, null=True)
    spot_fifteen_corner_left = models.TextField(blank=True, null=True)
    spot_fifteen_break_left = models.TextField(blank=True, null=True)
    spot_fifteen_top_key = models.TextField(blank=True, null=True)
    spot_fifteen_break_right = models.TextField(blank=True, null=True)
    spot_fifteen_corner_right = models.TextField(blank=True, null=True)
    spot_college_corner_left = models.TextField(blank=True, null=True)
    spot_college_break_left = models.TextField(blank=True, null=True)
    spot_college_top_key = models.TextField(blank=True, null=True)
    spot_college_break_right = models.TextField(blank=True, null=True)
    spot_college_corner_right = models.TextField(blank=True, null=True)
    spot_nba_corner_left = models.TextField(blank=True, null=True)
    spot_nba_break_left = models.TextField(blank=True, null=True)
    spot_nba_top_key = models.TextField(blank=True, null=True)
    spot_nba_break_right = models.TextField(blank=True, null=True)
    spot_nba_corner_right = models.TextField(blank=True, null=True)
    off_drib_fifteen_break_left = models.TextField(blank=True, null=True)
    off_drib_fifteen_top_key = models.TextField(blank=True, null=True)
    off_drib_fifteen_break_right = models.TextField(blank=True, null=True)
    off_drib_college_break_left = models.TextField(blank=True, null=True)
    off_drib_college_top_key = models.TextField(blank=True, null=True)
    off_drib_college_break_right = models.TextField(blank=True, null=True)
    on_move_fifteen = models.TextField(blank=True, null=True)
    on_move_college = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'draft_combine_stats'


class DraftHistory(models.Model):
    person_id = models.TextField(blank=True, null=True)
    player_name = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    round_number = models.IntegerField(blank=True, null=True)
    round_pick = models.IntegerField(blank=True, null=True)
    overall_pick = models.IntegerField(blank=True, null=True)
    draft_type = models.TextField(blank=True, null=True)
    team_id = models.TextField(blank=True, null=True)
    team_city = models.TextField(blank=True, null=True)
    team_name = models.TextField(blank=True, null=True)
    team_abbreviation = models.TextField(blank=True, null=True)
    organization = models.TextField(blank=True, null=True)
    organization_type = models.TextField(blank=True, null=True)
    player_profile_flag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'draft_history'


class Game(models.Model):
    season_id = models.TextField(blank=True, null=True)
    team_id_home = models.TextField(blank=True, null=True)
    team_abbreviation_home = models.TextField(blank=True, null=True)
    team_name_home = models.TextField(blank=True, null=True)
    game_id = models.TextField(blank=True, null=True)
    game_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    matchup_home = models.TextField(blank=True, null=True)
    wl_home = models.TextField(blank=True, null=True)
    min = models.IntegerField(blank=True, null=True)
    fgm_home = models.FloatField(blank=True, null=True)
    fga_home = models.FloatField(blank=True, null=True)
    fg_pct_home = models.FloatField(blank=True, null=True)
    fg3m_home = models.FloatField(blank=True, null=True)
    fg3a_home = models.FloatField(blank=True, null=True)
    fg3_pct_home = models.FloatField(blank=True, null=True)
    ftm_home = models.FloatField(blank=True, null=True)
    fta_home = models.FloatField(blank=True, null=True)
    ft_pct_home = models.FloatField(blank=True, null=True)
    oreb_home = models.FloatField(blank=True, null=True)
    dreb_home = models.FloatField(blank=True, null=True)
    reb_home = models.FloatField(blank=True, null=True)
    ast_home = models.FloatField(blank=True, null=True)
    stl_home = models.FloatField(blank=True, null=True)
    blk_home = models.FloatField(blank=True, null=True)
    tov_home = models.FloatField(blank=True, null=True)
    pf_home = models.FloatField(blank=True, null=True)
    pts_home = models.FloatField(blank=True, null=True)
    plus_minus_home = models.IntegerField(blank=True, null=True)
    video_available_home = models.IntegerField(blank=True, null=True)
    team_id_away = models.TextField(blank=True, null=True)
    team_abbreviation_away = models.TextField(blank=True, null=True)
    team_name_away = models.TextField(blank=True, null=True)
    matchup_away = models.TextField(blank=True, null=True)
    wl_away = models.TextField(blank=True, null=True)
    fgm_away = models.FloatField(blank=True, null=True)
    fga_away = models.FloatField(blank=True, null=True)
    fg_pct_away = models.FloatField(blank=True, null=True)
    fg3m_away = models.FloatField(blank=True, null=True)
    fg3a_away = models.FloatField(blank=True, null=True)
    fg3_pct_away = models.FloatField(blank=True, null=True)
    ftm_away = models.FloatField(blank=True, null=True)
    fta_away = models.FloatField(blank=True, null=True)
    ft_pct_away = models.FloatField(blank=True, null=True)
    oreb_away = models.FloatField(blank=True, null=True)
    dreb_away = models.FloatField(blank=True, null=True)
    reb_away = models.FloatField(blank=True, null=True)
    ast_away = models.FloatField(blank=True, null=True)
    stl_away = models.FloatField(blank=True, null=True)
    blk_away = models.FloatField(blank=True, null=True)
    tov_away = models.FloatField(blank=True, null=True)
    pf_away = models.FloatField(blank=True, null=True)
    pts_away = models.FloatField(blank=True, null=True)
    plus_minus_away = models.IntegerField(blank=True, null=True)
    video_available_away = models.IntegerField(blank=True, null=True)
    season_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'


class GameInfo(models.Model):
    game_id = models.TextField(blank=True, null=True)
    game_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    attendance = models.IntegerField(blank=True, null=True)
    game_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_info'


class GameSummary(models.Model):
    game_date_est = models.TextField(blank=True, null=True)  # This field type is a guess.
    game_sequence = models.IntegerField(blank=True, null=True)
    game_id = models.TextField(blank=True, null=True)
    game_status_id = models.IntegerField(blank=True, null=True)
    game_status_text = models.TextField(blank=True, null=True)
    gamecode = models.TextField(blank=True, null=True)
    home_team_id = models.TextField(blank=True, null=True)
    visitor_team_id = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    live_period = models.IntegerField(blank=True, null=True)
    live_pc_time = models.TextField(blank=True, null=True)
    natl_tv_broadcaster_abbreviation = models.TextField(blank=True, null=True)
    live_period_time_bcast = models.TextField(blank=True, null=True)
    wh_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_summary'


class InactivePlayers(models.Model):
    game_id = models.TextField(blank=True, null=True)
    player_id = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    jersey_num = models.TextField(blank=True, null=True)
    team_id = models.TextField(blank=True, null=True)
    team_city = models.TextField(blank=True, null=True)
    team_name = models.TextField(blank=True, null=True)
    team_abbreviation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inactive_players'


class LineScore(models.Model):
    game_date_est = models.TextField(blank=True, null=True)  # This field type is a guess.
    game_sequence = models.IntegerField(blank=True, null=True)
    game_id = models.TextField(blank=True, null=True)
    team_id_home = models.TextField(blank=True, null=True)
    team_abbreviation_home = models.TextField(blank=True, null=True)
    team_city_name_home = models.TextField(blank=True, null=True)
    team_nickname_home = models.TextField(blank=True, null=True)
    team_wins_losses_home = models.TextField(blank=True, null=True)
    pts_qtr1_home = models.TextField(blank=True, null=True)
    pts_qtr2_home = models.TextField(blank=True, null=True)
    pts_qtr3_home = models.TextField(blank=True, null=True)
    pts_qtr4_home = models.TextField(blank=True, null=True)
    pts_ot1_home = models.IntegerField(blank=True, null=True)
    pts_ot2_home = models.IntegerField(blank=True, null=True)
    pts_ot3_home = models.IntegerField(blank=True, null=True)
    pts_ot4_home = models.IntegerField(blank=True, null=True)
    pts_ot5_home = models.IntegerField(blank=True, null=True)
    pts_ot6_home = models.IntegerField(blank=True, null=True)
    pts_ot7_home = models.IntegerField(blank=True, null=True)
    pts_ot8_home = models.IntegerField(blank=True, null=True)
    pts_ot9_home = models.IntegerField(blank=True, null=True)
    pts_ot10_home = models.IntegerField(blank=True, null=True)
    pts_home = models.FloatField(blank=True, null=True)
    team_id_away = models.TextField(blank=True, null=True)
    team_abbreviation_away = models.TextField(blank=True, null=True)
    team_city_name_away = models.TextField(blank=True, null=True)
    team_nickname_away = models.TextField(blank=True, null=True)
    team_wins_losses_away = models.TextField(blank=True, null=True)
    pts_qtr1_away = models.IntegerField(blank=True, null=True)
    pts_qtr2_away = models.TextField(blank=True, null=True)
    pts_qtr3_away = models.TextField(blank=True, null=True)
    pts_qtr4_away = models.IntegerField(blank=True, null=True)
    pts_ot1_away = models.IntegerField(blank=True, null=True)
    pts_ot2_away = models.IntegerField(blank=True, null=True)
    pts_ot3_away = models.IntegerField(blank=True, null=True)
    pts_ot4_away = models.IntegerField(blank=True, null=True)
    pts_ot5_away = models.IntegerField(blank=True, null=True)
    pts_ot6_away = models.IntegerField(blank=True, null=True)
    pts_ot7_away = models.IntegerField(blank=True, null=True)
    pts_ot8_away = models.IntegerField(blank=True, null=True)
    pts_ot9_away = models.IntegerField(blank=True, null=True)
    pts_ot10_away = models.IntegerField(blank=True, null=True)
    pts_away = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'line_score'


class Officials(models.Model):
    game_id = models.TextField(blank=True, null=True)
    official_id = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    jersey_num = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'officials'


class OtherStats(models.Model):
    game_id = models.TextField(blank=True, null=True)
    league_id = models.TextField(blank=True, null=True)
    team_id_home = models.TextField(blank=True, null=True)
    team_abbreviation_home = models.TextField(blank=True, null=True)
    team_city_home = models.TextField(blank=True, null=True)
    pts_paint_home = models.IntegerField(blank=True, null=True)
    pts_2nd_chance_home = models.IntegerField(blank=True, null=True)
    pts_fb_home = models.IntegerField(blank=True, null=True)
    largest_lead_home = models.IntegerField(blank=True, null=True)
    lead_changes = models.IntegerField(blank=True, null=True)
    times_tied = models.IntegerField(blank=True, null=True)
    team_turnovers_home = models.IntegerField(blank=True, null=True)
    total_turnovers_home = models.IntegerField(blank=True, null=True)
    team_rebounds_home = models.IntegerField(blank=True, null=True)
    pts_off_to_home = models.IntegerField(blank=True, null=True)
    team_id_away = models.TextField(blank=True, null=True)
    team_abbreviation_away = models.TextField(blank=True, null=True)
    team_city_away = models.TextField(blank=True, null=True)
    pts_paint_away = models.IntegerField(blank=True, null=True)
    pts_2nd_chance_away = models.IntegerField(blank=True, null=True)
    pts_fb_away = models.IntegerField(blank=True, null=True)
    largest_lead_away = models.IntegerField(blank=True, null=True)
    team_turnovers_away = models.IntegerField(blank=True, null=True)
    total_turnovers_away = models.IntegerField(blank=True, null=True)
    team_rebounds_away = models.IntegerField(blank=True, null=True)
    pts_off_to_away = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_stats'


class PlayByPlay(models.Model):
    game_id = models.TextField(blank=True, null=True)
    eventnum = models.IntegerField(blank=True, null=True)
    eventmsgtype = models.IntegerField(blank=True, null=True)
    eventmsgactiontype = models.IntegerField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    wctimestring = models.TextField(blank=True, null=True)
    pctimestring = models.TextField(blank=True, null=True)
    homedescription = models.TextField(blank=True, null=True)
    neutraldescription = models.TextField(blank=True, null=True)
    visitordescription = models.TextField(blank=True, null=True)
    score = models.TextField(blank=True, null=True)
    scoremargin = models.TextField(blank=True, null=True)
    person1type = models.FloatField(blank=True, null=True)
    player1_id = models.TextField(blank=True, null=True)
    player1_name = models.TextField(blank=True, null=True)
    player1_team_id = models.TextField(blank=True, null=True)
    player1_team_city = models.TextField(blank=True, null=True)
    player1_team_nickname = models.TextField(blank=True, null=True)
    player1_team_abbreviation = models.TextField(blank=True, null=True)
    person2type = models.FloatField(blank=True, null=True)
    player2_id = models.TextField(blank=True, null=True)
    player2_name = models.TextField(blank=True, null=True)
    player2_team_id = models.TextField(blank=True, null=True)
    player2_team_city = models.TextField(blank=True, null=True)
    player2_team_nickname = models.TextField(blank=True, null=True)
    player2_team_abbreviation = models.TextField(blank=True, null=True)
    person3type = models.FloatField(blank=True, null=True)
    player3_id = models.TextField(blank=True, null=True)
    player3_name = models.TextField(blank=True, null=True)
    player3_team_id = models.TextField(blank=True, null=True)
    player3_team_city = models.TextField(blank=True, null=True)
    player3_team_nickname = models.TextField(blank=True, null=True)
    player3_team_abbreviation = models.TextField(blank=True, null=True)
    video_available_flag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'play_by_play'


class Player(models.Model):
    player_id = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class Team(models.Model):
    team_id = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    abbreviation = models.TextField(blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    year_founded = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class TeamDetails(models.Model):
    team_id = models.TextField(blank=True, null=True)
    abbreviation = models.TextField(blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
    yearfounded = models.FloatField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    arena = models.TextField(blank=True, null=True)
    arenacapacity = models.FloatField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    generalmanager = models.TextField(blank=True, null=True)
    headcoach = models.TextField(blank=True, null=True)
    dleagueaffiliation = models.TextField(blank=True, null=True)
    facebook = models.TextField(blank=True, null=True)
    instagram = models.TextField(blank=True, null=True)
    twitter = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_details'


class TeamHistory(models.Model):
    team_id = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
    year_founded = models.IntegerField(blank=True, null=True)
    year_active_till = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_history'


class TeamInfoCommon(models.Model):
    team_id = models.TextField(blank=True, null=True)
    season_year = models.TextField(blank=True, null=True)
    team_city = models.TextField(blank=True, null=True)
    team_name = models.TextField(blank=True, null=True)
    team_abbreviation = models.TextField(blank=True, null=True)
    team_conference = models.TextField(blank=True, null=True)
    team_division = models.TextField(blank=True, null=True)
    team_code = models.TextField(blank=True, null=True)
    team_slug = models.TextField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    pct = models.FloatField(blank=True, null=True)
    conf_rank = models.IntegerField(blank=True, null=True)
    div_rank = models.IntegerField(blank=True, null=True)
    min_year = models.IntegerField(blank=True, null=True)
    max_year = models.IntegerField(blank=True, null=True)
    league_id = models.TextField(blank=True, null=True)
    season_id = models.TextField(blank=True, null=True)
    pts_rank = models.IntegerField(blank=True, null=True)
    pts_pg = models.FloatField(blank=True, null=True)
    reb_rank = models.IntegerField(blank=True, null=True)
    reb_pg = models.FloatField(blank=True, null=True)
    ast_rank = models.IntegerField(blank=True, null=True)
    ast_pg = models.FloatField(blank=True, null=True)
    opp_pts_rank = models.IntegerField(blank=True, null=True)
    opp_pts_pg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_info_common'
