I want to pull historical nba data to see the correlation between player points and team winning

pip install nba_api



1. Pull game-level data, so that you have a df_game with one row per (team, game)
2. Pull player-level data, so that you have a df_player with one row per (player on team, game)
3. Create a prediction for game outcomes. First, let's investigate how much of an advantage it is to be a home team. By-game, compute a 250-game EWMA of the home team win%. What's the r2 of this model (compared to a baseline of guessing 50/50)? 