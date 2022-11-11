from models.database import Database
from views.view_tournament import ViewTournament
from models.tournament import Tournament
import models

class TournamentController:

    def __init__(self) -> None:
        self.view = ViewTournament()
        self.database = Database('tournaments')
    def handle_tournament(self):
        exit_requested = False
        
        while not exit_requested:
            choice = self.view.display_tournament_menu()

            if choice == "1":
                # creation d'un joueur
                self.create_tournament()
            elif choice == "2":
                # Update player
                self.history_tournament()
            elif choice == "3":
                exit_requested = True


    def create_tournament(self):

    # Récupération des infos du joueur
        user_entries = self.view.get_info_tournament()

    # Création du tournoi
        tournament = Tournament(user_entries['tournament_name'],user_entries['nb_players'],user_entries['type'],user_entries['nb_rounds'],user_entries['player1'])


    #Serialization
        serialized_tournament = tournament.serialize(tournament)
        print(serialized_tournament)

    # #Sauvegarde du tournoi dans la database
        self.database.save_db(serialized_tournament)
        return tournament   

    def history_tournament(self, validation=False):
            choice = self.view.choose_tournament_by()
            sorted_data = self.database.sorted_by(choice)
            self.view.display_tournament_historic(sorted_data)
            if(validation == True):
                input('\nAppuyez sur Entreé pour continuer ')       


    def display_players_order_by_name(self, validation=False):
        """Print players order by name"""
               
