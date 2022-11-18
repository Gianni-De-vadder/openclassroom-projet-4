from .database import Database
from models.player import Player


class Tournament:
    """Represents a tournament"""

    database = Database("tournaments")

    def __init__(
        self,
        tournament_name: str,
        nb_players: str,
        type: int,
        nb_rounds: str,
        players_id,
        players_list=None,
        id: int = None,
    ) -> None:
        self.tournament_name = tournament_name
        self.nb_players = nb_players
        self.type = type
        self.nb_rounds = nb_rounds
        self.players_ids = players_id
        self.players_list = players_list
        self.id = None

    def __str__(self) -> str:
        return self.name

    def serialize(self) -> dict:
        """Return a dictionnary with the object attribute value"""
        data = {
            "tournament_name": self.tournament_name,
            "nb_player": self.nb_players,
            "type": self.type,
            "nb_rounds": self.nb_rounds,
            "players_ids": self.players_ids,
            "players_data": self.players_list,
        }
        return data

    def get_players_data(self):
        """It takes players_ids attribute, create a player object from player data (dict)"""
        self.players_list = []
        for player_id in self.players_ids:
            player_data = Player.get_player_by_id(player_id)
            player = Player.create_from_document(player_data)
            self.players_list.append(player)

        return self.players_list
        
