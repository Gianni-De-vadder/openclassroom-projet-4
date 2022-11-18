from tabulate import tabulate
from .view_player import ViewPlayer
from models.database import Database
from models.player import Player
from utils.db import db_player, db_tournament
from controllers.tournament import display_players_order_by_name


tabulate.PRESERVE_WHITESPACE = False


class ViewTournament:
    def __init__(self) -> None:

        self.tournament_database = Database("tournaments")

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
            tournament_name = input("Nom du tournoi : ")
            nb_players = input("Nombre de joueurs : ")
            while True:
                try:
                    tournament_type = int(
                        input("Type de tournoi (Blitz = 1, Bullet = 2, Rapide = 3) ")
                    )
                    break
                except ValueError:
                    print("La valeur doit être numérique")

            if tournament_type == "1" or tournament_type == 1:
                tournament_type = str("Blitz")

            if tournament_type == "2" or tournament_type == 2:
                tournament_type = str("Bullet")

            if tournament_type == "3" or tournament_type == 3:
                tournament_type = str("Rapide")

            players_ids = self.get_tournament_players(int(nb_players))
            print(players_ids)

            nb_rounds = input("Nombre de rondes : ")
            print(nb_players)

            tournament = {
                "tournament_name": tournament_name,
                "nb_players": nb_players,
                "type": tournament_type,
                "nb_rounds": nb_rounds,
                "players_ids": players_ids,
            }
            i = 0

            print(tournament)

            # TODO : Vérification à l'input
            return tournament

    def choose_tournament_by(self):
        while True:
            choice = input(
                "Voulez-vous afficher l'ordre par nom ou elo ? (nom / elo / q pour quitter) :"
            )
            if choice == "nom":
                print("tableau filtré par nom")
                return "tournament_name"
            elif choice == "elo":
                print("tableau filtré par elo")
                return "elo"
            elif choice == "q":
                break
            else:
                print("Merci choisir un choix proprosé...")
                break

    def display_tournament_historic(self, tournaments):
        print(
            tabulate(
                tournaments,
                headers="keys",
                tablefmt="github",
                colalign=(
                    "center",
                    "center",
                    "center",
                    "center",
                ),
            )
        )

    def get_tournament_players(self, nb_players):
        players_ids = []

        while True:
            print(nb_players)
            player_id = input(
                "Taper les IDs des joueur a ajouter en les séparant par un espace"
            )
            players_ids = player_id.split(" ")
            if len(players_ids) == nb_players:
                return players_ids

    def select_start(self):
        while True:
            start = input("Souhaitez vous démarrer le tournoi de suite ? (Oui/Non)")
            if start == "Oui" or start == "oui" or start == "o":
                return True
            elif start == "Non" or start == "non" or start == "n":
                return False
            else:
                continue


if __name__ == "__main__":
    pass
