# from dataclasses import dataclass
# from datetime import date

# from .player import Player

# # from typing import NamedTuple
# # class nPlayerScore(NamedTuple):
# #     player: Player
# #     score: int = 0


# class PlayerScore:
#     """Represents a player with a score"""

#     def __init__(self, player: Player, score: int = 0) -> None:
#         self.player = player
#         self.score = score

#     @property
#     def score(self):
#         return self._score

#     @score.setter
#     def score(self, value: int):
#         self._score = value
#         self.player.score += value

#     def __str__(self) -> str:
#         return f"Joueur : {self.player.name}, score : {self.score}"

#     def __lt__(self, other_player: "PlayerScore"):
#         return self.score < other_player.score


# # match = ([P1, score], [P2, score])
# @dataclass
# class Match:
#     """Represents a match between two player"""

#     # player_score1: PlayerScore
#     player_score1: PlayerScore
#     player_score2: PlayerScore

#     @property
#     def p1_full_name(self):
#         """Return firstname and name of player 1"""
#         return self.player_score1.player.full_name

#     @property
#     def p2_full_name(self):
#         """Return firstname and name of player 2"""
#         return self.player_score2.player.full_name

#     def __str__(self) -> str:
#         msg = f"{self.p1_full_name} : {self.player_score1.score} VS {self.p2_full_name} : {self.player_score2.score}"
#         return msg

#     def serialize(self) -> list[tuple, tuple]:
#         """Return a list of tuple with id and score for the player"""
#         # [(idPlayer1, 0), (idPlayer2, 0)]
#         player_score1 = (self.player_score1.player.id, self.player_score1.score)
#         player_score2 = (self.player_score2.player.id, self.player_score2.score)
#         return [player_score1, player_score2]

#     @classmethod
#     def create_from_document(cls, data: list, player_table) -> "Match":
#         """Return a Match object from a list"""

#         matches: list[Match] = []
#         # each element of data is a list of 2 list : [[1, 1], [5, 0]]
#         # the first élement of each list is the id of player, the second the score
#         for element in data:
#             # First: Get the player
#             id1 = element[0][0]
#             id2 = element[1][0]
#             player1 = Player.create_from_document(player_table.get_by_id(id1))
#             player2 = Player.create_from_document(player_table.get_by_id(id2))

#             # Second: Create the PlayerScore
#             score_p1 = element[0][1]
#             score_p2 = element[1][1]
#             ps1 = PlayerScore(player1, score_p1)
#             ps2 = PlayerScore(player2, score_p2)

#             # create the Match object and add it to the list
#             matches.append(cls(ps1, ps2))

#         return matches


# @dataclass
# class Round:
#     """Represents a round of matches"""

#     name: str
#     matches: list[Match]
#     start: str = str(date.today())
#     end: str = ""
#     status: str = "En cours"

#     def __str__(self) -> str:
#         msg = f"Round {self.name} - Début : {self.start} - "
#         if self.end == "":
#             msg += "En cours ..."
#         else:
#             msg += f"Fini le : {self.end}"
#         return msg

#     def serialize(self) -> dict:
#         """Return serialize data for the round in a dictionnary."""
#         matches = [match.serialize() for match in self.matches]

#         data = {
#             "name": self.name,
#             "start": self.start,
#             "end": self.end,
#             "matches": matches,
#         }
#         return data

#     @classmethod
#     def create_from_document(csl, data: dict, player_table) -> "Round":
#         """Return a Round object from a dict"""
#         # create the round unpacking the simple data
#         round = csl(**data)

#         # create the more complex object (Match object)
#         round.matches = Match.create_from_document(data["matches"], player_table)
#         return round


# if __name__ == "__main__":
#     from datetime import date

#     p1 = Player("Carlsen", "Magnus", date(1990, 10, 15), "M", 2850, id=1)
#     p2 = Player("Vachier", "Max", date(1990, 12, 25), "M", 2800, id=2)

#     ps1 = PlayerScore(p1)
#     ps2 = PlayerScore(p2)

#     # p1 win
#     ps1.score = 1

#     m1 = Match(ps1, ps2)
#     m2 = Match(ps2, ps1)

#     r1 = Round("Round 1", [m1, m2])

#     print(r1)
#     for m in r1.matches:
#         msg = f"{m.player_score1} Vs {m.player_score2}"
#         print(msg)

#     print(m1.serialize())