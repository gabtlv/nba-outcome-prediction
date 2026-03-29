import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predicting, setPredicting] = useState(false);

  useEffect(() => {
    fetchTodaysGames();
  }, []);

  const fetchTodaysGames = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:8000/games/today');
      setGames(response.data.games || []);
    } catch (error) {
      console.error('Error fetching games:', error);
      setGames([]);
    }
    setLoading(false);
  };

  const predictGame = async (game) => {
    setSelectedGame(game);
    setPredicting(true);
    setPrediction(null);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/predict?home_team=${game.home_team}&away_team=${game.away_team}`
      );
      setPrediction(response.data);
    } catch (error) {
      console.error('Prediction error:', error);
    }
    setPredicting(false);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>NBA Game Predictor</h1>
          <p>Select a game to see AI predictions</p>
        </header>

        {loading ? (
          <div className="loading-state">
            <div className="spinner-large"></div>
            <p>Loading today's games...</p>
          </div>
        ) : games.length === 0 ? (
          <div className="empty-state">
            <span className="icon">📅</span>
            <h3>No games today</h3>
            <p>Check back on game days</p>
          </div>
        ) : (
          <div className="games-grid">
            {games.map((game, index) => (
              <div
                key={index}
                className={`game-card ${selectedGame === game ? 'selected' : ''}`}
                onClick={() => predictGame(game)}
              >
                <div className="game-teams">
                  <div className="team">{game.away_team}</div>
                  <div className="vs">@</div>
                  <div className="team">{game.home_team}</div>
                </div>
                <div className="game-time">
                  {new Date(game.game_time).toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            ))}
          </div>
        )}

        {predicting && (
          <div className="prediction-loading">
            <div className="spinner-large"></div>
            <p>Analyzing matchup...</p>
          </div>
        )}

        {prediction && !predicting && (
          <div className="prediction-panel">
            <div className="prediction-header">
              <h2>Prediction</h2>
              <div className="matchup">
                {selectedGame.away_team} @ {selectedGame.home_team}
              </div>
            </div>

            <div className="winner-section">
              <div className="label">Predicted Winner</div>
              <div className="winner">{prediction.predicted_winner}</div>
            </div>

            <div className="probabilities">
              <div className="prob-row">
                <div className="prob-label">{prediction.home_team}</div>
                <div className="prob-bar-container">
                  <div
                    className="prob-bar home"
                    style={{ width: `${prediction.home_win_probability}%` }}
                  ></div>
                </div>
                <div className="prob-percent">{prediction.home_win_probability}%</div>
              </div>

              <div className="prob-row">
                <div className="prob-label">{prediction.away_team}</div>
                <div className="prob-bar-container">
                  <div
                    className="prob-bar away"
                    style={{ width: `${prediction.away_win_probability}%` }}
                  ></div>
                </div>
                <div className="prob-percent">{prediction.away_win_probability}%</div>
              </div>
            </div>

            <div className="confidence">
              Confidence: {Math.max(prediction.home_win_probability, prediction.away_win_probability) > 70 ? 'High' : 'Medium'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;