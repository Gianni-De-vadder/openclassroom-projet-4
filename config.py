from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# Directory for the data
DATA_DIR = BASE_DIR / "data"
PLAYER_DB_PATH = f"{DATA_DIR}/players.json"
TOURNAMENT_DB_PATH = f"{DATA_DIR}/tournaments.json"
