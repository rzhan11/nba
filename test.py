# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: sports
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
from sklearn.metrics import r2_score
from data import fetch_scores, fetch_player_games

# %%
seasons = ['2021-22', '2022-23', '2023-24', '2024-25']

scores = fetch_scores(seasons)
print(f"Total games: {len(scores)}")
print(scores.head(10))


# %%
def zmr2(ytrue, ypred):
    return 1 - ((ytrue - ypred)**2).sum() / (ytrue ** 2).sum()


# %%

# %%
player_df = fetch_player_games(seasons)
print(f"Total player-game rows: {len(player_df)}")
print(player_df[['game_id', 'player_name', 'team', 'points', 'rebounds', 'assists', 'wl', 'season']].head(10))

# %%

# Merge player data with game scores
# Each player row gets home/away context from scores

player_games = player_df[['game_id', 'player_id', 'player_name', 'team', 'points', 'rebounds', 'assists', 'minutes', 'wl', 'season']].copy()

player_games = player_games.merge(
    scores[['game_id', 'date', 'home_team', 'away_team', 'home_points', 'away_points', 'home_won', 'away_won']],
    on='game_id',
    how='left'
)

player_games['is_home'] = (player_games['team'] == player_games['home_team']).astype(int)
player_games['won'] = (player_games['wl'] == 'W').astype(float)

print(f"Player-game rows with game context: {len(player_games)}")
display(player_games[['date', 'player_name', 'team', 'is_home', 'points', 'won']])


# %%

# 250-game EWMA of home win%, R² vs 50/50 baseline
scores_sorted = scores.sort_values('date').reset_index(drop=True)

# Shift(1) to avoid look-ahead: prediction for game N uses only games 0..N-1
scores_sorted['home_win_ewma'] = (
    scores_sorted['home_won'].ewm(span=250, adjust=False).mean().shift(1).fillna(0.5)
)

ytrue = scores_sorted['home_won']
ypred = scores_sorted['home_win_ewma']

ss_res  = ((ytrue - ypred) ** 2).sum()
ss_base = ((ytrue - 0.5)   ** 2).sum()
r2 = 1 - ss_res / ss_base

print(f"Home win EWMA R² vs 50/50 baseline: {r2:.6f}")
print(f"Overall home win rate: {ytrue.mean():.4f}")

scores_sorted[['date', 'home_win_ewma']].set_index('date').plot(
    title='250-game EWMA of home win %', figsize=(10, 3), ylim=(0.45, 0.65)
)


# %%
