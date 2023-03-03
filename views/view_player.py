from tabulate import tabulate


class ViewPlayer:
    def display_player_menu(self):
        """Display the player main menu and return the user choice"""

        while True:
            print("\n", " Gestion des joueurs ".center(80, "-"), "\n")
            print("1. Création d'un joueur")
            print("2. Modification d'un joueur")
            print("3. Liste des joueurs classée par nom")
            print("4. Liste des joueurs classée par rang")
            print("5. Revenir au menu précédent")

            choice = input("\nEntrez votre choix : ")

            if choice in ["1", "2", "3", "4", "5"]:
                return choice

            print("Choix invalide.\n")

    def get_info_player(self):
        while True:
            name = input("Nom : ")
            first_name = input("Prénom : ")
            dob = input("Date de naissance (Format JJ-MM-AAAA) : ")
            while True:
                try:
                    elo = int(input("ELO : "))
                    break
                except ValueError:
                    print("La valeur doit être numérique")

            # TODO : Vérification à l'input
            return {"name": name, "first_name": first_name, "rank": elo, "dob": dob}

    def display_players_list(self, players_list):
        print(tabulate(players_list, headers="keys", tablefmt="fancy_grid"))


if __name__ == "__main__":
    """Test a player"""
