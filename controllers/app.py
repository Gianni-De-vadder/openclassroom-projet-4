from controllers.tournament import TournamentController
from controllers.player import PlayerController
from views.view_app import ViewApp


class ApplicationController:
    """Represents the application"""

    def __init__(self) -> None:
        self.view_app = ViewApp()
        self.tournament_controller = TournamentController()
        self.player_controller = PlayerController()

    def start(self):
        """Display the main menu and manage user choice"""
        exit_requested = False
        
        while not exit_requested:
            choice = self.view_app.display_main_menu()

            if choice == "1":
                # gestion des tournois
                self.tournament_controller.handle_tournament()
            elif choice == "2":
                # Gestion des joueurs
                self.player_controller.handle_player()
                # exit
            elif choice == "3":
                exit_requested = True
                

