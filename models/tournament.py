from .database import Database
from models.player import Player
from models.rounds_model import PlayerScore, Match
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
        return self.tournament_name

    def serialize(self) -> dict:
        """Return a dictionnary with the object attribute value"""
        rounds = []
        [rounds.append(round.serialize()) for round in self.rounds]
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
        try:
            if current_round >= self.nb_rounds:
                data["vainqueur"] = self.winner.first_name
        except KeyError:
            pass
        return data

    @classmethod
    def deserialize(cls, data):
        if data["meetings"] == "[]":
            data["meetings"] = "rencontres"

        data["vainqueur"] = "undifined"
        tournament = Tournament(
            data["tournament_name"],
            data["nb_player"],
            data["type"],
            data["nb_rounds"],
            "0",
            int(data["current_round"]),
            [],
            data["meetings"],
            int(data["status"]),
            str(data["vainqueur"]),
            data["id"],
        )
        for round in data["rounds"]:
            tournament.rounds.append(round)

        players_id = Tournament.deserialize_players(data["players"])
        players = tournament.get_players_data(players_id)
        tournament.players = players
        return tournament

    @classmethod
    def deserialize_players(self, players_id):
        return players_id

    def get_players_data(self, players_ids: list[int]) -> list[Player]:
        """Return a players list from db (object)"""
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

    def ask_score(self):
        valid_input = (1, 2, 3)
        while True:
            score = input(
                "Entrez le vainqueur (1 : Joueur 1   2 : Joueur 2   3 : Nul) "
            )
            try:
                score = int(score)
            except ValueError:
                score = float(score)

            if score in valid_input:
                return score

            print("Merci d'entrer une valeur proposée ")

    def get_matches(self):
        """
        It takes a list of players, sorts them by their rating, and then creates a list of matches where
        each player is paired with the next player in the list, as long as they haven't played each
        other before
        :return: A list of dictionaries.
        """
        matches = []
        sorted_list = Player.sort_players_list_by(self.players)
        selected_player = sorted_list.copy()
        while len(selected_player) > 0:
            player = selected_player[0]
            opponent = selected_player[1]
            players_met = self.meetings.get(player.id, [])
            if opponent.id not in players_met:
                selected_player.remove(player)
                selected_player.remove(opponent)
                ps1 = PlayerScore(player)
                ps2 = PlayerScore(opponent)
                match = Match(ps1, ps2)
                matches.append(match)
        return matches

    def deserialize_matches(self):
        print(self.rounds)
        for round in self.rounds:
            print(round["matches"][0])

    @classmethod
    def sort_tournament_data(cls, data):
        sorted_data = []
        tournament = {}
        for element in data:
            tournament["tournament_name"] = element["tournament_name"]
            tournament["type"] = element["type"]
            tournament["nb_rounds"] = element["nb_rounds"]
            tournament["id"] = element["id"]
            sorted_data.append(tournament)
        return sorted_data

    @classmethod
    def in_progress_tournament(cls):
        search = db_tournament.get_in_progress(0)
        parse = cls.parse_in_progress(search)
        return parse

    @classmethod
    def done_tournament(cls):
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
            result = data[:count] + "\n" + data[count:]
            i += 1
        return result
