import time
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

SEASONS = ['2021-22', '2022-23', '2023-24', '2024-25']


def fetch_scores(seasons=SEASONS):
    """One row per game with home/away points and win flags."""
    all_games = []
    for season in seasons:
        print(f"Fetching {season}...")
        log = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Regular Season')
        df = log.get_data_frames()[0]
        df['season'] = season
        all_games.append(df)
        time.sleep(1)

    full_df = pd.concat(all_games, ignore_index=True)

    home = full_df[full_df['MATCHUP'].str.contains(r'vs\.')].copy()
    away = full_df[full_df['MATCHUP'].str.contains('@')].copy()
    merged = home.merge(away, on='GAME_ID', suffixes=('_home', '_away'))

    return pd.DataFrame({
        'game_id':     merged['GAME_ID'],
        'season':      merged['season_home'],
        'date':        merged['GAME_DATE_home'].astype(str),
        'home_team':   merged['TEAM_ABBREVIATION_home'],
        'away_team':   merged['TEAM_ABBREVIATION_away'],
        'home_points': merged['PTS_home'],
        'away_points': merged['PTS_away'],
        'home_won':    (merged['WL_home'] == 'W').astype(float),
        'away_won':    (merged['WL_away'] == 'W').astype(float),
    })


def fetch_player_games(seasons=SEASONS):
    """One row per (player, game) with basic box score stats."""
    all_games = []
    for season in seasons:
        print(f"Fetching players {season}...")
        log = leaguegamelog.LeagueGameLog(
            season=season,
            season_type_all_star='Regular Season',
            player_or_team_abbreviation='P',
        )
        df = log.get_data_frames()[0]
        df['season'] = season
        all_games.append(df)
        time.sleep(1)

    df_player = pd.concat(all_games, ignore_index=True)
    return df_player.rename(columns={
        'GAME_ID':            'game_id',
        'PLAYER_ID':          'player_id',
        'PLAYER_NAME':        'player_name',
        'TEAM_ABBREVIATION':  'team',
        'PTS':                'points',
        'REB':                'rebounds',
        'AST':                'assists',
        'MIN':                'minutes',
        'WL':                 'wl',
    })
