from .database import Database
from models.player import Player
from utils.db import db_tournament


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
        rounds=None,
        meetings=None,
        status=None,
        winner=None,
        id: int = None,
    ) -> None:
        self.tournament_name = tournament_name
        self.nb_players = nb_players
        self.type = type
        self.nb_rounds = nb_rounds
        self.players = None
        self.current_round = 0
        self.rounds = []
        self.meetings = {}
        self.status = 0
        self.winner = ""
        self.id = None

    def __str__(self) -> str:
        return self.name

    def serialize(self) -> dict:
        """Return a dictionnary with the object attribute value"""
        rounds = []
        [rounds.append(round.serialize()) for round in self.rounds]
        print(rounds)
        data = {
            "tournament_name": self.tournament_name,
            "nb_player": self.nb_players,
            "type": self.type,
            "nb_rounds": self.nb_rounds,
            "players": [player.id for player in self.players],
            "current_round": self.current_round,
            "rounds": rounds,
            "meetings": self.meetings,
            "vainqueur": "Undefined",
            "status": self.status,
        }
        current_round = int(data["current_round"])
        print(current_round)
        try:
            if current_round >= self.nb_rounds:
                data["vainqueur"] = self.winner.first_name
        except:
            pass
        return data

    @classmethod
    def deserialize(cls, data):
        data["meetings"] = "rencontres"
        data["vainqueur"] = "undifined"
        tournament = Tournament(
            data["tournament_name"],
            data["nb_player"],
            data["type"],
            data["nb_rounds"],
            "0",
            int(data["current_round"]),
            data["rounds"],
            data["meetings"],
            int(data["status"]),
            str(data["vainqueur"]),
            data["id"],
        )
        players_id = Tournament.deserialize_players(data["players"])
        players = tournament.get_players_data(players_id)
        tournament.players = players
        return tournament

    @classmethod
    def deserialize_players(self, players_id):
        print(players_id)
        return players_id

    def get_players_data(self, players_ids: list[int]) -> list[Player]:
        """Return a players list from db (object)"""
        print(f" list d'id de players {players_ids}")
        players_list = []
        for player_id in players_ids:
            player_id = int(player_id)
            player_data = Player.get_player_by_id(player_id)
            player = Player.create_from_document(player_data)
            players_list.append(player)

        return players_list

    def create_desc_lists(self, list) -> list:
        """
        It takes a list of players and returns a list of two lists, each containing the players for each
        team

        :param list: The list of players that will be split into two teams
        :return: A list of lists.
        """
        i = 0
        TeamA = []
        TeamB = []
        for element in list:
            if i == 0:
                TeamA.append(element)
                i = 1
            else:
                TeamB.append(element)
                i = 0
        Teams = []
        Teams.append(TeamA)
        Teams.append(TeamB)
        return Teams

    def assign_players_from_lists(self, listA, listB):
        i = 0
        games = []
        for player in listA:
            game = []
            game.append(listA[i])
            game.append(listB[i])
            games.append(game)
            i += 1
        return games

    def ask_score(self, player):
        score = input(
            f"Quel est le score de {player.first_name} {player.name} ? (1 = Gagnant 0 = Perdant 0.5 = Egalité) "
        )
        try:
            score = int(score)
        except:
            score = float(score)
        return score

    def sort_players_score_next_round(self):
        final_list = []
        sorted_list = Player.sort_players_list_by(self.players)
        selected_player = sorted_list
        while len(selected_player) > 0:
            match = {}
            player = selected_player[0]
            opponent = selected_player[1]
            players_met = self.meetings.get(player.id, [])
            if opponent.id not in players_met:
                match[player] = opponent
                final_list.append(match)
                selected_player.remove(player)
                selected_player.remove(opponent)
        return final_list

    @classmethod
    def in_progress_tournament(cls):
        search = db_tournament.get_in_progress(0)
        parse = cls.parse_in_progress(search)
        return parse

    @classmethod
    def parse_in_progress(cls, data):
        for element in data:
            element["rounds"] = "Trop long pour afficher"
            element["status"] = "En cours"
        return data

    @classmethod
    def wrap(cls, data):
        data = str(data)
        count = len(str(data)) / 4
        count = round(count)
        print(count)
        i = 0
        while i != 4:
            result = data[:count] + f"\n" + data[count:]
            i += 1
        return result
