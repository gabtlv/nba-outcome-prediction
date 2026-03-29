from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits

import joblib
import time

app = FastAPI(title="NBA Prediction API")

# ADD THESE LINES:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your trained model
model = joblib.load('models/game_winner_v1.pkl')
feature_names = joblib.load('models/feature_names_v1.pkl')

def get_team_stats(team_name, season="2024-25"):

    all_teams = teams.get_teams()
    team = None
    
    for t in all_teams:
        if (team_name.lower() in t['full_name'].lower() or
            team_name.lower() in t['nickname'].lower() or
            team_name.upper() == t['abbreviation']):
            team = t
            break
    if not team:
        return None
    
    time.sleep(0.6)
    team_stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
        team_id=team['id'],
        season=season
    )

    df = team_stats.get_data_frames()[0]
    gp = df['GP'][0]

    return {
        'FG_PCT': df['FG_PCT'][0],
        'FT_PCT': df['FT_PCT'][0],
        'FG3_PCT': df['FG3_PCT'][0],
        'AST': df['AST'][0] / gp,
        'REB': df['REB'][0] / gp
    }

@app.get("/")
def home():
    return {"message": "NBA Prediction API is running!"}

@app.get("/games/today")
def get_todays_games():
    try:
        time.sleep(1)
        board = scoreboard.ScoreBoard()
        games = board.games.get_dict()
        
        matchups = []
        for game in games:
            matchups.append({
                "home_team": game["homeTeam"]["teamName"],
                "away_team": game["awayTeam"]["teamName"],
                "game_time": game["gameTimeUTC"]
            })
        
        return {"games": matchups}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict")
def predict_game(home_team: str, away_team: str):
    try:
        # Get team stats
        home_stats = get_team_stats(home_team)
        away_stats = get_team_stats(away_team)
        
        if not home_stats or not away_stats:
            return {"error": "Team not found"}

        # Features for the model
        # 'FG_PCT_home',      # Shooting percentage - very important
        # 'FG_PCT_away',
        # 'FT_PCT_home',      # Free throw percentage
        # 'FT_PCT_away', 
        # 'FG3_PCT_home',     # 3-point percentage
        # 'FG3_PCT_away',
        # 'AST_home',         # Assists
        # 'AST_away',
        # 'REB_home',         # Rebounds
        # 'REB_away'

        features = [
            home_stats['FG_PCT'],
            away_stats['FG_PCT'],
            home_stats['FT_PCT'],
            away_stats['FT_PCT'],
            home_stats['FG3_PCT'],
            away_stats['FG3_PCT'],
            home_stats['AST'],
            away_stats['AST'],
            home_stats['REB'],
            away_stats['REB']
        ]
        
        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]

        winner = home_team if prediction == 1 else away_team

        home_win_prob = probabilities[1] * 100
        away_win_prob = probabilities[0] * 100

        return {
            "home_team": home_team,
            "away_team": away_team,
            "predicted_winner": winner,
            "home_win_probability": round(home_win_prob,1),
            "away_win_probability": round(away_win_prob,1)
        }
    except Exception as e:
        return {"error": str(e)}