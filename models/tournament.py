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
        players=None,
        current_round=0,
        id: int = None,
    ) -> None:
        self.tournament_name = tournament_name
        self.nb_players = nb_players
        self.type = type
        self.nb_rounds = nb_rounds
        self.players = None
        self.current_round = 0
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
            "players": [player.id for player in self.players],
        }
        return data

    def get_players_data(self, players_ids: list[int]) -> list[Player]:
        """Return a players list from db (object)"""
        print(players_ids)
        players_list = []
        for player_id in players_ids:
            player_data = Player.get_player_by_id(player_id)
            player = Player.create_from_document(player_data)
            players_list.append(player)

        return players_list
