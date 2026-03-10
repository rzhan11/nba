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
from datetime import datetime
from lib.data import fetch_scores, fetch_player_games
from lib.modeling import lagged_ewma
from lib.plots import vcv
from lib.stats import zmr2
import matplotlib.pyplot as plt

SEASONS = [f"{y}-{str(y+1)[-2:]}" for y in range(2015, 2025)]
FETCH_FRESH = False  # True = fetch from NBA API; False = load from parquet

# Only used when FETCH_FRESH = False.
SCORES_PATH = "data/scores_20260310_003419.parquet"
PLAYER_PATH = "data/player_20260310_003419.parquet"

# %%
if FETCH_FRESH:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    df_scores = fetch_scores(SEASONS)
    scores_path = f"data/scores_{ts}.parquet"
    df_scores.to_parquet(scores_path)
    print(f"Saved: {scores_path}")

    df_player = fetch_player_games(SEASONS)
    player_path = f"data/player_{ts}.parquet"
    df_player.to_parquet(player_path)
    print(f"Saved: {player_path}")
else:
    print(f"Loading: {SCORES_PATH}")
    print(f"Loading: {PLAYER_PATH}")
    df_scores = pd.read_parquet(SCORES_PATH)
    df_player = pd.read_parquet(PLAYER_PATH)

print(f"\ndf_scores:  {len(df_scores):,} rows")
print(f"df_player:  {len(df_player):,} rows")

# %%
df_player_games = df_player[['game_id', 'player_id', 'player_name', 'team', 'points', 'rebounds', 'assists', 'minutes', 'wl', 'season']].copy()

df_player_games = df_player_games.merge(
    df_scores[['game_id', 'date', 'home_team', 'away_team', 'home_points', 'away_points', 'home_won', 'away_won']],
    on='game_id',
    how='left',
)

df_player_games['is_home'] = (df_player_games['team'] == df_player_games['home_team']).astype(int)
df_player_games['won'] = (df_player_games['wl'] == 'W').astype(float)

print(f"df_player_games: {len(df_player_games):,} rows")
df_player_games[['date', 'player_name', 'team', 'is_home', 'points', 'won']].head(10)

# %%
df_scores['home_adv'] = df_scores['home_won'] - 0.5

df_scores['home_adv_ewma'] = lagged_ewma(df_scores, 'home_adv', span=250, fill=0.0, prior_weight=250)

print(f"Home adv EWMA zmr2: {zmr2(df_scores['home_adv'], df_scores['home_adv_ewma']):.6f}")
print(f"Overall home adv: {df_scores['home_adv'].mean():.4f}")

# %%
SPANS = [100, 300, 1000, 3000, 10000, 30000]

for span in SPANS:
    df_scores[f'home_adv_ewma_{span}'] = lagged_ewma(
        df_scores, 'home_adv', span=span, fill=0.0, prior_weight=span
    )
    r2 = zmr2(df_scores['home_adv'], df_scores[f'home_adv_ewma_{span}'])
    print(f"span={span:>6}  zmr2={r2:.6f}")

# %%
for span in SPANS:
    ax = vcv(df_scores, sort='date', pred=f'home_adv_ewma_{span}', resps=['home_adv'])
    ax.set_title(f'vcv: home_adv_ewma span={span} vs home_adv, sorted by date')

# Time series: ewma values over time
_, ax2 = plt.subplots(figsize=(10, 3))
df_plot = df_scores.sort_values('date')
for span in SPANS:
    ax2.plot(pd.to_datetime(df_plot['date']).dt.date, df_plot[f'home_adv_ewma_{span}'], label=f'span={span}')
ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax2.set_title('home_adv_ewma over time')
ax2.set_xlabel('date')
ax2.set_ylabel('home_adv_ewma')
ax2.legend()
plt.tight_layout()

# %%
