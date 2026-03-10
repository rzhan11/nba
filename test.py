from nba_api.stats.endpoints import leaguegamelog
import pandas as pd

# Get all games for a season
gamelog = leaguegamelog.LeagueGameLog(season='2023-24', season_type_all_star='Regular Season')
df = gamelog.get_data_frames()[0]

# Each row is a team's game result
print(df[['GAME_DATE', 'MATCHUP', 'WL', 'PTS']].head(20))

from nba_api.stats.endpoints import leaguegamelog

gamelog = leaguegamelog.LeagueGameLog(season='2023-24')
df = gamelog.get_data_frames()[0]

# Split home/away, then merge on GAME_ID to get both scores
home = df[df['MATCHUP'].str.contains('vs\.')].copy()
away = df[df['MATCHUP'].str.contains('@')].copy()

scores = home.merge(away, on='GAME_ID', suffixes=('_home', '_away'))
scores = scores[['GAME_DATE_home', 'MATCHUP_home', 'PTS_home', 'PTS_away', 'WL_home']]
scores.columns = ['Date', 'Matchup', 'Home_PTS', 'Away_PTS', 'Result']
print(scores.head(10))