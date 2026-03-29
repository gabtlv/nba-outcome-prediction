# 🏀 NBA Game Predictor

An AI-powered web application that predicts NBA game winners using machine learning.

## Features

- **Live Game Selection**: Automatically fetches today's NBA games
- **AI Predictions**: 83% accuracy using XGBoost machine learning model
- **Win Probabilities**: See percentage chances for each team
- **Modern UI**: Clean, minimal dark design built with React
- **Real-time Stats**: Fetches current season team statistics from NBA API

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **XGBoost** - Machine learning model
- **NBA API** - Live NBA data
- **Scikit-learn** - Model training
- **Pandas** - Data processing

### Frontend
- **React** - UI framework
- **Axios** - API calls
- **CSS3** - Modern styling

## Project Structure
```
nba-outcome-prediction-ml/
├── api/
│   └── main.py              # FastAPI backend
├── data/
│   ├── raw/                 # Original NBA data
│   └── processed/           # Cleaned training data
├── models/
│   ├── game_winner_v1.pkl   # Trained ML model
│   └── feature_names_v1.pkl # Model features
├── notebooks/
│   └── games.ipynb          # Model training notebook
└── frontend-react/
    └── src/
        ├── App.js           # React application
        └── App.css          # Styling
```

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- pip

### Backend Setup
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/nba-game-predictor.git
cd nba-game-predictor

# Install Python dependencies
pip install fastapi uvicorn nba_api joblib xgboost scikit-learn pandas

# Start API server
uvicorn api.main:app --reload
```

The API will run at `http://127.0.0.1:8000`

### Frontend Setup
```bash
# Navigate to frontend
cd frontend-react

# Install dependencies
npm install

# Start React app
npm start
```

The app will open at `http://localhost:3000`

## Usage

1. Start both the API server and React app
2. The app automatically loads today's NBA games
3. Click on any game to see the prediction
4. View win probabilities and predicted winner

## Model Details

- **Algorithm**: XGBoost Classifier
- **Accuracy**: 83.73%
- **Training Data**: Historical NBA games (2004-2024)
- **Features Used**:
  - Field Goal Percentage (FG%)
  - Free Throw Percentage (FT%)
  - 3-Point Percentage (FG3%)
  - Assists per game
  - Rebounds per game

## API Endpoints

- `GET /` - Health check
- `GET /games/today` - Fetch today's NBA games
- `POST /predict?home_team={team}&away_team={team}` - Get prediction

## Future Improvements

- [ ] Add more features (injuries, rest days, recent form)
- [ ] Improve model accuracy to 70%+
- [ ] Add point spread predictions
- [ ] Player stat predictions
- [ ] Historical prediction tracking
- [ ] Deploy to cloud (Vercel + Render)

## Screenshots

## Contributing

Pull requests welcome! For major changes, please open an issue first.

## License

MIT

## Acknowledgments

- NBA API for providing game data
- Kaggle for historical NBA datasets
- FastAPI and React communities

---

**Built as a learning project to explore machine learning and full-stack development.**
