# Preferences
- Name DataFrame variables with the `df_` prefix (e.g. `df_scores`, `df_player_games`)
- Date columns should be strings, not `datetime` objects
- Fail loudly: no silent fallbacks, defaults, or recovery paths. If something is misconfigured, raise an error or let it crash.
