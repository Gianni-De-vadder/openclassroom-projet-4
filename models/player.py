import json
from tabulate import tabulate
from utils.db import db_player

"""Classe joueur"""


class Player:
    """Represents a player"""

    def __init__(
        self, name: str, first_name: str, elo: int, dob: str, id: int = None
    ) -> None:
        self.name = name
        self.first_name = first_name
        self.elo = elo
        self.dob = dob
        self.score = 0
        self.id = id

    def __str__(self) -> str:
        return self.name

    def __lt__(self, other_player: "Player"):
        """Useful to sort a list of player on their score or rank"""
        if self.score == other_player.score:
            return self.elo < other_player.elo
        return self.score < other_player.score

    def display_ranking_by_name(cls):
        """
        It takes a class as an argument, and returns a sorted list of the players in the database

        :param cls: the class that the method is being called on
        :return: The sorted_by method is being returned.
        """
        return db_player.sorted_by("name")

    @classmethod
    def display_ranking_by_elo(cls):
        return db_player.load_db(cls.table_name, "elo")

    def serialize(self) -> dict:
        """Return a dictionnary with the object attribute value"""
        data = {
            "first_name": self.first_name,
            "name": self.name,
            "elo": self.elo,
            "dob": self.dob,
        }
        return data

    @classmethod
    def get_player_by_id(cls, player_id):
        return db_player.get_element_by_id(player_id)

    @classmethod
    def create_from_document(cls, doc: dict) -> "Player":
        """Return a player from a document object or dict compatible"""
        return Player(**doc)

    @classmethod
    def deserialize(self, data: dict) -> "Player":
        """Return a Player from a dictionnary"""
        return Player(**data)

    def save(self):
        db_player.save_db(self.serialize())
        print("player sauvegardé")


if __name__ == "__main__":
    """Test a player"""
    data = db_player.get_all_data()
    players_list = sorted(data, key=lambda doc: doc.get("name"))
    print("")
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
    # for player in data:
    #     print(data[player]['first_name'])
    # #print(tabulate(players_list))
