from tabulate import tabulate
from .view_player import ViewPlayer
from controllers.player import PlayerController


tabulate.PRESERVE_WHITESPACE = False


class ViewTournament:
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

            max_rounds = int(nb_players) - 1

            nb_rounds = input(
                f"Nombre de rounds ({max_rounds} maximum pour {nb_players} joueurs)  : "
            )
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
                "Voulez-vous afficher l'ordre par nom ou elo ? (nom / elo / q pour quitter) : "
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

    def ask_tournaments(self):
        while True:
            choice = input(
                "Voulez-vous voir les tournois en cours ou tous les tournoi ? (1 - En cours / 2 - Tous / q - Quitter) : "
            )
            if choice == "1":
                print("Voici les tournois en cours : ")
                return "en cours"
            elif choice == "2":
                print("Voici tous les tournois : ")
                return "tous"
            elif choice == "q":
                return "q"
            else:
                print("Merci choisir un choix proprosé...")
                break

    def display_running_ask_id(self):
        while True:
            choice = input("Merci de taper l'id du tournoi à reprendre (q - Quitter )")
            try:
                choice = int(choice)
            except:
                pass
            print(choice)
            if choice == "q" or choice == "Q":
                print("Sortie")
                return False
            elif isinstance(choice, int):
                print("Reprise du tournoi ")
                return choice
            else:
                print("Merci choisir un choix proprosé...")
                continue

    def display_tournament_historic(self, tournaments):
        print(
            tabulate(
                tournaments,
                headers="keys",
                tablefmt="github",
                colalign=("center",),
            )
        )

    def get_tournament_players(self, nb_players):
        players_ids = []
        PlayerController.second_display_players_order_by_name()
        # self.display_players_list(players_list)
        while True:
            print(nb_players)
            player_id = input(
                "Taper les IDs des joueurs a ajouter en les séparant par un espace : "
            )
            players_ids = player_id.split(" ")
            players_ids = [int(id) for id in players_ids]
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

    @classmethod
    def input_score(cls, match):
        print(
            f"Indiquer le résultat entre les {match.p1_full_name} et {match.p2_full_name}"
        )
        score = input(
            f"Qui est le vainqueur (1 : Joueur 1 / 2 : Joueur 2 / 3 : Match Nul) : "
        )
        return score

    def display_players_list(self, players_list):

        return ViewPlayer.display_players_list(players_list)


if __name__ == "__main__":
    pass
