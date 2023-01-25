from secrets import choice
from turtle import update
from views.view_player import ViewPlayer
from models.player import Player
from models.database import Database
from utils.db import db_player
import json


class PlayerController:
    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def __init__(self) -> None:
        self.view = ViewPlayer()
        self.database = db_player

    def handle_player(self):
        exit_requested = False

        while not exit_requested:
            choice = self.view.display_player_menu()

            if choice == "1":
                # creation d'un joueur
                self.create_player()
            elif choice == "2":
                # Update player
                self.update_player()
            elif choice == "3":
                self.display_players_order_by_name(validation=True)
            elif choice == "4":
                load_players_by_elo = self.display_players_order_by_elo(validation=True)
                print(load_players_by_elo)
            elif choice == "5":
                # Retour au menu précédent
                exit_requested = True

    def create_player(self):

        # Récupération des infos du joueur
        user_entries = self.view.get_info_player()

        # Création du joueur
        player = Player(
            user_entries["name"],
            user_entries["first_name"],
            user_entries["rank"],
            user_entries["dob"],
        )

        # Serialization
        serialized_player = player.serialize()
        print(serialized_player)

        # #Sauvegarde du joueur dans la database
        db_player.save_db(serialized_player)
        return player

    # def auto_increment_player():
    #     if(Database. == ):

    def update_player(self):
        """Manage player update"""
        choice = input(
            'Afficher les joueur par rang ou nom ? (Rang = 0 , Nom = 1, Quitter = "q") :'
        )
        if choice == "0":
            players_list_by_elo = self.display_players_order_by_elo()
            print(players_list_by_elo)
            player_id = int(input("Entez l'identifiant du joueur souhaité : "))

        elif choice == "1":
            self.display_players_order_by_name()
            player_id = int(input("Entez l'identifiant du joueur souhaité : "))

        elif choice == "q":
            return None

        else:
            print("Entrez un choix de la liste.")
            self.update_player()

        user_entries = self.view.get_info_player()

        player = Player(
            user_entries["name"],
            user_entries["first_name"],
            user_entries["rank"],
            user_entries["dob"],
        )

        serialized_player = self.database.serialize(player)

        self.database.update_db(serialized_player, [player_id])

        print("Mis à jour avec succès")

        input("\nAppuyez sur Entreé pour continuer ")

    def display_players_order_by_name(self, validation=False):
        """Print players order by name"""
        players_by_name = self.database.sorted_by("name")
        print(players_by_name)
        self.view.display_players_list(players_by_name)
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")

    @classmethod
    def second_display_players_order_by_name(self, validation=False):
        """Print players order by name"""
        players_by_name = db_player.sorted_by("name")
        ViewPlayer.display_players_list(self, players_by_name)
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")

    def display_players_order_by_elo(self, validation=False):
        """Print players order by rank"""
        players_by_elo = self.database.sorted_by("elo")
        self.view.display_players_list(players_by_elo)
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")
