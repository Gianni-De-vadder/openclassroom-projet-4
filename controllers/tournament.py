from models.database import Database
from views.view_tournament import ViewTournament
from models.tournament import Tournament
from models.player import Player
from controllers.player import PlayerController
from utils.db import db_tournament
from models.rounds_model import Round, Match, PlayerScore


class TournamentController:
    def __init__(self) -> None:
        self.view = ViewTournament()
        self.database = db_tournament
        self.player_controller = PlayerController()
        self.tournament: Tournament = None

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
        self.tournament = Tournament(
            tournament_name=user_entries["tournament_name"],
            nb_players=user_entries["nb_players"],
            type=user_entries["type"],
            nb_rounds=user_entries["nb_rounds"],
        )

        self.tournament.players = self.tournament.get_players_data(
            user_entries["players_ids"]
        )

        start = self.view.select_start()

        if start == True:
            print("Démarrage du tournoi")
            self.play_tournament()

        else:
            print("Tournoi aborté")
            serialized_tournament = self.tournament.serialize()

            self.database.save_db(serialized_tournament)

        # #Sauvegarde du tournoi dans la database
        return self.tournament

    def play_tournament(self):
        first_round = self.get_first_round()
        print(first_round)
        # Saisir resultat match ou sortir ?
        # Lancer round suivant

    def set_round_scores(self, current_round):
        for match in current_round.matches:
            player_score = ViewTournament.input_score(match)
        return player_score

    def get_first_round(self) -> Round:
        """Return a Round object"""
        # -Trier joueurs par ELO
        print(type(self.tournament.players))

        players = Player.sort_players_list_by(self.tournament.players)

        # -Créer deux listes en répartissant les forces
        Teams = self.tournament.create_desc_lists(players)
        TeamA = Teams[0]
        TeamB = Teams[1]

        # Assigner joueur 0 TeamA avec joueur 0 TeamB ect...
        games = self.tournament.assign_players_from_lists(TeamA, TeamB)

        # Créer liste de match (vide)
        matches = []

        i = 0
        for idx, player in enumerate(games):
            print(
                f"Match entre : {games[i][0].first_name} {games[i][0].name} et {games[i][1].first_name} {games[i][1].name}"
            )
            # Créer Playerscore 1
            ps1 = PlayerScore(games[i][0], self.tournament.ask_score(games[i][0]))

            # Créer Playerscore 2
            ps2 = PlayerScore(games[i][1], self.tournament.ask_score(games[i][1]))
            print(ps1)
            print(ps2)

            # Créer match(Playerscore1, Playerscore2)
            match = Match(ps1, ps1)

            # Ajouter match à la liste de match
            matches.append(match)
            i += 1
        # Créer round
        round = Round("Ronde 1", matches, "13/01/2023", "13/01/2023", "Terminé")
        # Retourner Round
        return round

    def get_next_round(self):
        """Return a Round object"""
        # Trier les joueurs par le score

    def history_tournament(self, validation=False):
        choice = self.view.choose_tournament_by()
        sorted_data = self.database.sorted_by(choice)
        self.view.display_tournament_historic(sorted_data)
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")

    def display_players_order_by_name(self):
        """Print players order by name"""
        return self.player_controller.display_players_order_by_name(validation=False)
