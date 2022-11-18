from models.database import Database

from config import PLAYER_DB_PATH, TOURNAMENT_DB_PATH

db_player = Database(PLAYER_DB_PATH)
db_tournament = Database(TOURNAMENT_DB_PATH)
