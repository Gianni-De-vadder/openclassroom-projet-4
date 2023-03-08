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
            print("3. Reprise d'un tournoi")
            print("4. Rapport d'un tournoi")
            print("5. Revenir au menu précédent")

            choice = input("\nEntrez votre choix : ")

            if choice in ["1", "2", "3", "4", "5"]:
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

            while True:
                nb_rounds = input(
                    f"Nombre de rounds ({max_rounds} maximum pour {nb_players} joueurs)  : "
                )
                nb_rounds = int(nb_rounds)
                max_rounds = int(max_rounds)

                if nb_rounds > max_rounds:
                    print(
                        "Merci d'entrer un nombre inferieur au nombre maximum de rounds"
                    )
                    pass
                else:
                    break
            print(nb_players)

            tournament = {
                "tournament_name": tournament_name,
                "nb_players": nb_players,
                "type": tournament_type,
                "nb_rounds": nb_rounds,
                "players_ids": players_ids,
            }

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
                (
                    "Voulez-vous voir les tournois"
                    "en cours ou tous les tournoi ? (1 - En cours / 2 - Tous / q - Quitter) : "
                )
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
            choice = input("Merci de taper l'id du tournoi (q - Quitter )")
            try:
                choice = int(choice)
            except ValueError:
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

    def input_id_verification(self, user_input, validation=False):
        while True:
            if isinstance(int(user_input), int):
                self.display_message(f"Affichage du tournoi {user_input}")
                break
            elif user_input == "q" or user_input == "Q":
                self.display_message("Sortie")
                return False
            else:
                self.display_message("Merci d'entrer un id valable")
        if validation is True:
            self.ask_input("\nAppuyez sur Entreé pour continuer ")
        return True

    def display_matches(self, match):
        p1 = match.player_score1.player
        p2 = match.player_score2.player
        print(f"{p1.first_name} {p1.name}  contre {p2.first_name} {p2.name}")

    def display_tournament_rapport(self, tournament: object):
        print(tournament.tournament_name)
        # print(tournament.players[0].first_name)
        # print(tournament.rounds[0].matches)
        for round in tournament.rounds:
            print(round.name)
            for match in round.matches:
                print(
                    f"{match.p1_full_name} ({match.player_score1.score}) vs {match.p2_full_name} ({match.player_score2.score})"
                )
        # for round in tournament.rounds:
        #     print(round["matches"])

    def display_tournament_final_classment(self, classement):
        print("Classement Final :")
        for player in classement:
            print(f"{player.first_name} {player.name} ({player.score})")

    def display_message(self, message):
        print(message)

    def ask_input(self, message):
        result = input(message)
        return result

    @classmethod
    def input_score(cls, match):
        print(
            f"Indiquer le résultat entre les {match.p1_full_name} et {match.p2_full_name}"
        )
        score = input(
            "Qui est le vainqueur (1 : Joueur 1 / 2 : Joueur 2 / 3 : Match Nul) : "
        )
        return score

    def display_players_list(self, players_list):

        return ViewPlayer.display_players_list(players_list)


if __name__ == "__main__":
    pass
