import json
from .database import Database
from tabulate import tabulate
"""Classe joueur"""
class Player:
    """Represents a player"""


    def __init__(self, name: str, first_name: str, elo: int, dob: str, id : int=None) -> None:
        self.name = name
        self.first_name = first_name
        self.elo = elo
        self.dob = dob
        self.id = None
        self.database = Database('players')


    def __str__(self) -> str:
        return self.name
    
    def display_ranking_by_name(cls):
        """
        It takes a class as an argument, and returns a sorted list of the players in the database
        
        :param cls: the class that the method is being called on
        :return: The sorted_by method is being returned.
        """
        return database.sorted_by('name')
    
    @classmethod
    def display_ranking_by_elo(cls):
        return database.load_db(cls.table_name, 'elo')

    @classmethod
    def serialize(self,player) -> dict:
            """Return a dictionnary with the object attribute value"""
            data = {
                'first_name': player.first_name,
                'name': player.name,
                'elo': player.elo,
                'dob': player.dob
            }
            return data        

    def get_player_by_id(player_id):
        database = Database('players')
        return database.get_element_by_id(player_id)
        


    @classmethod    
    def deserialize(self, data: dict) -> "Player":
        """Return a Player from a dictionnary"""
        return Player(**data)


    def save(self):
        print("player sauvegardé")

if __name__ == '__main__':
    """Test a player"""
    database = Database('players')
    data = database.get_all_data()
    players_list = sorted(data, key = lambda doc: doc.get('name'))
    print('')
    print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
    # for player in data:
    #     print(data[player]['first_name'])
    # #print(tabulate(players_list))