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
        rounds=None,
        meetings=None,
        id: int = None,
    ) -> None:
        self.tournament_name = tournament_name
        self.nb_players = nb_players
        self.type = type
        self.nb_rounds = nb_rounds
        self.players = None
        self.current_round = 1
        self.rounds = []
        self.meetings = {}
        self.id = None

    def __str__(self) -> str:
        return self.name

    def serialize(self) -> dict:
        """Return a dictionnary with the object attribute value"""
        rounds = []
        data = {
            "tournament_name": self.tournament_name,
            "nb_player": self.nb_players,
            "type": self.type,
            "nb_rounds": self.nb_rounds,
            "players": [player.id for player in self.players],
            "current_round": self.current_round,
            "rounds": [rounds.append(round.serialize()) for round in self.rounds],
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
