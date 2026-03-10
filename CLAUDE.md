# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

Pull historical NBA data to study the correlation between player points and team winning. Uses the `nba_api` library to fetch stats from the NBA stats API.

## Setup

```bash
pip install nba_api pandas
```

## Running Code

Run the Python script directly:
```bash
python test.py
```

Open the notebook for interactive exploration:
```bash
jupyter notebook test.ipynb
```

## Key Libraries

- `nba_api` — wrapper around the NBA stats API (`stats.nba.com`). Key endpoints in `nba_api.stats.endpoints`: `leaguegamelog` (team-level game results), `playergamelog` (player-level game results)
- `pandas` — data manipulation and analysis

## Data Patterns

`LeagueGameLog` returns one row per team per game. The `MATCHUP` column uses `vs.` for home games and `@` for away games — this is used to split and merge on `GAME_ID` to get head-to-head scores in a single row.
