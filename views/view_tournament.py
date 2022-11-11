from tabulate import tabulate
from .view_player import ViewPlayer
from models.database import Database
from models.player import Player
class ViewTournament:

    def __init__(self) -> None:
        self.player_database = Database('players')
        self.tournament_database = Database('tournaments')
        self.view_player = ViewPlayer()

    def display_tournament_menu(self):
        """Display the player main menu and return the user choice"""
        
        while True:
            print("\n", " Gestion des tournois ".center(80, "-"), "\n")
            print("1. Création d'un tournoi")
            print("2. Historique des tournois")
            print("3. Revenir au menu précédent")

            choice = input("\nEntrez votre choix : ")

            if choice in ["1", "2", "3"]:
                return choice

            print("Choix invalide.\n")
    
    def get_info_tournament(self):
                while True:
                    tournament_name = input('Nom du tournoi : ')
                    nb_players = input('Nombre de joueurs : ')
                    while True:
                        try:
                            tournament_type = int(input('Type de tournoi (Blitz = 1, Bullet = 2, Rapide = 3) '))
                            break
                        except ValueError:
                            print("La valeur doit être numérique")
                            
                    if tournament_type == '1' or tournament_type == 1:
                        tournament_type = str('Blitz')

                    if tournament_type == '2' or tournament_type == 2:
                        tournament_type = str('Bullet')

                    if tournament_type == '3' or tournament_type == 3:
                        tournament_type = str('Rapide')                        

                    
                    nb_rounds = input('Nombre de rondes : ')    

                    players = []

                    while len(players) != int(nb_players):
                        print(f"{len(players)} / {int(nb_players)}")
                        players_by_name = self.player_database.sorted_by('name')
                        print(self.view_player.display_players_list(players_by_name))
                        player = input('Taper ID du joueur a ajouter')
                        player = Player.get_player_by_id(player)
                        players.append(player)
                    
                    print(players)
                    
                        


                    tournament = {"tournament_name" : tournament_name, "nb_players" : nb_players,"type" : tournament_type, "nb_rounds" : nb_rounds}
                    i = 0
                    print(tournament)
                    for player in players:
                        tournament[f'player{i}'] = players[i]
                        i = i + 1



                    #TODO : Vérification à l'input
                    return tournament

    def choose_tournament_by(self):
        while True:
            choice = input('Voulez-vous afficher l\'ordre par nom ou elo ? (nom / elo / q pour quitter) :')
            if choice == 'nom':
                print('tableau filtré par nom')
                return 'tournament_name'
            elif choice == 'elo':
                print('tableau filtré par elo')
                return 'elo'
            elif choice == 'q':
                break
            else:
                print('Merci choisir un choix proprosé...')
                break
    
    def display_tournament_historic(self, tournaments):
        print(tabulate(tournaments, headers='keys', tablefmt='fancy_grid'))


