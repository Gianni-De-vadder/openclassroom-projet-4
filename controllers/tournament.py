from models.database import Database
from models.player import Player
from models.rounds_model import Match, PlayerScore, Round
from models.tournament import Tournament
from utils.db import db_tournament
from views.view_tournament import ViewTournament
from controllers.player import PlayerController
from datetime import date


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
                self.create_tournament()
            elif choice == "2":
                self.history_tournament()

            elif choice == "3":
                self.show_running_tournament()

            elif choice == "4":
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
            print("Tournoi Sauvegardé, voir historique pour reprendre")
            serialized_tournament = self.tournament.serialize()
            self.database.save_db(serialized_tournament)

        # #Sauvegarde du tournoi dans la database
        return self.tournament

    def play_tournament(self, resume=False):
        first_round = self.get_first_round()
        first_round.serialize()
        if resume == True:
            print(self.tournament.meetings)
        self.tournament.nb_rounds = int(self.tournament.nb_rounds)
        while self.tournament.current_round <= self.tournament.nb_rounds:
            continue_rounds = input(
                f"Round {self.tournament.current_round + 1} : Souhaitez-vous continuer le tournoi ou reprendre plus tard ? ( 1 - Oui/ 2 - Non) "
            )
            if continue_rounds == "1":
                self.get_next_round()
            elif continue_rounds == "2":
                serialize = self.tournament.serialize()
                db_tournament.update_db(serialize, self.tournament.id, tournament=True)
                break
            else:
                print("Merci d'entrer un choix proposé (1 ou 2)")

        classment = Player.sort_players_list_by(self.tournament.players)
        print(f"{classment[0]} est le vainqueur")
        self.tournament.winner = classment[0]
        if self.tournament.current_round >= self.tournament.nb_rounds:
            self.tournament.status = 1

        else:
            self.tournament.status = 0
        serialize = self.tournament.serialize()
        if resume == False:
            db_tournament.save_db(serialize)
        if resume == True:
            db_tournament.update_db(serialize, self.tournament.id, tournament=True)

        print(f"tournament_data : {serialize}")

        # Saisir resultat match ou sortir ?
        # Lancer round suivant

    def set_round_scores(self, current_round):
        for match in current_round.matches:
            player_score = ViewTournament.input_score(match)
        return player_score

    def get_first_round(self) -> Round:
        """Return a Round object"""
        # -Trier joueurs par ELO

        players = Player.sort_players_list_by(self.tournament.players)

        # -Créer deux listes en répartissant les forces
        Teams = self.tournament.create_desc_lists(players)
        TeamA = Teams[0]
        TeamB = Teams[1]

        # Assigner joueur 0 TeamA avec joueur 0 TeamB ect...
        games = self.tournament.assign_players_from_lists(TeamA, TeamB)

        # Créer liste de match (vide)
        matches = []

        # Créer liste de rencontres
        self.meetings = {}

        i = 0
        for idx, player in enumerate(games):
            print(
                f"Match entre : {games[i][0].first_name} {games[i][0].name} et {games[i][1].first_name} {games[i][1].name} :"
            )
            total_score = 1
            p1_score = self.tournament.ask_score()
            p2_score = total_score - p1_score
            # Créer Playerscore 1
            ps1 = PlayerScore(games[i][0], p1_score)

            # Créer Playerscore 2
            ps2 = PlayerScore(games[i][1], p2_score)
            print(ps1)
            print(ps2)

            # Créer match(Playerscore1, Playerscore2)
            match = Match(ps1, ps1)

            self.tournament.meetings[ps1.player.id] = [ps2.player.id]
            print(self.tournament.meetings)

            # Ajouter match à la liste de match
            matches.append(match)
            i += 1
        # Créer round
        self.tournament.current_round += 1
        round = Round("Round 1", matches, "13/01/2023", "13/01/2023", "Terminé")
        self.tournament.rounds.append(round)
        print(f" Round numéro : {self.tournament.current_round}")

        # Retourner Round
        return round

    def get_next_round(self):
        """Return a Round object"""
        # -Trier joueurs par ELO

        matches: list[Match] = self.tournament.get_matches()
        # Créer liste de match (vide)

        for match in matches:
            player1 = match.player_score1
            player2 = match.player_score2
            print(
                f"Match entre : {player1.player.first_name} {player1.player.name} et {player2.player.first_name} {player2.player.name} :"
            )
            match_result = self.tournament.ask_score()
            if match_result == 1:
                match.player_score1.score = 1
            elif match_result == 2:
                match.player_score2.score = 1
            else:
                match.player_score1.score = 0.5
                match.player_score2.score = 0.5

            # Créer round
        self.tournament.current_round += 1
        print(f" Round numéro : {self.tournament.current_round} terminé")

        round = Round(
            f"Round {self.tournament.current_round} ",
            matches,
            str(date.today),
            str(date.today),
            "Terminé",
        )
        self.tournament.rounds.append(round)
        # Retourner Round
        return round

    def history_tournament(self, validation=False):
        choice = self.view.choose_tournament_by()
        sorted_data = db_tournament.sorted_by(choice)
        if sorted_data != []:
            for element in sorted_data:
                element["rounds"] = "Trop long pour afficher"
            self.view.display_tournament_historic(sorted_data)
        else:
            print("Pas de tournois à afficher")
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")

    def show_running_tournament(self, validation=False):
        sorted_data = Tournament.in_progress_tournament()
        if sorted_data != []:
            self.view.display_tournament_historic(sorted_data)
            result = self.view.display_running_ask_id()
            if isinstance(result, int):
                self.resume_tournament(result)
        else:
            print("Pas de tournois à afficher")
        if validation == True:
            input("\nAppuyez sur Entreé pour continuer ")

    def display_players_order_by_name(self):
        """Print players order by name"""
        return self.player_controller.display_players_order_by_name(validation=False)

    def resume_tournament(self, id):
        data = db_tournament.get_element_by_id(id)
        data["id"] = id
        self.tournament = Tournament.deserialize(data)
        self.play_tournament(resume=True)
