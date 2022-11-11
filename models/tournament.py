from .database import Database

class Tournament:
    """Represents a tournament"""

    database = Database('tournaments')


    def __init__(self, tournament_name: str, nb_players: str, type: int, nb_rounds: str, player1=None, id : int=None) -> None:
        self.tournament_name = tournament_name
        self.nb_players = nb_players
        self.type = type
        self.nb_rounds = nb_rounds
        self.player1 = player1
        self.id = None

    def __str__(self) -> str:
        return self.name

    @classmethod
    def serialize(self,tournament) -> dict:
            """Return a dictionnary with the object attribute value"""
            data = {
                'tournament_name': tournament.tournament_name,
                'nb_player': tournament.nb_players,
                'type': tournament.type,
                'nb_rounds': tournament.nb_rounds,
                'player1' : tournament.player1
            }
            return data        