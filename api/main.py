from fastapi import FastAPI
from nba_api.live.nba.endpoints import scoreboard
import joblib
import time

app = FastAPI(title="NBA Prediction API")

# Load your trained model
model = joblib.load('models/game_winner_v1.pkl')
feature_names = joblib.load('models/feature_names_v1.pkl')

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
        # Get team stats (placeholder - you'll need to implement get_team_stats)
        # home_stats = get_team_stats(home_team)
        # away_stats = get_team_stats(away_team)
        
        # For now, return placeholder
        return {
            "home_team": home_team,
            "away_team": away_team,
            "predicted_winner": "To be implemented",
            "message": "Stats fetching coming next"
        }
    except Exception as e:
        return {"error": str(e)}