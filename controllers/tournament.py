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
                self.show_tournaments_rapports()

            elif choice == "5":
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

        play = self.view.select_start()

        if play is True:
            self.view.display_message("Démarrage du tournoi")
            self.play_tournament()

        else:
            self.view.display_message(
                "Tournoi Sauvegardé, voir menu reprise d'un tournoi"
            )
            serialized_tournament = self.tournament.serialize()
            self.database.save_db(serialized_tournament)

        # #Sauvegarde du tournoi dans la database
        return self.tournament

    def play_tournament(self, resume=False):
        first_round = self.get_first_round()
        first_round.serialize()
        if resume is True:
            self.view.display_message(self.tournament.meetings)
        self.tournament.nb_rounds = int(self.tournament.nb_rounds)
        while self.tournament.current_round <= self.tournament.nb_rounds:
            msg = (
                f"Round {self.tournament.current_round + 1} : Souhaitez-vous continuer le tournoi ou sauvegarder"
                "et reprendre plus tard ? ( 1 - Continuer/ 2 - Sauvegarder)"
            )
            continue_rounds = self.view.ask_input(msg)
            if continue_rounds == "1":
                self.get_next_round()
            elif continue_rounds == "2":
                serialize = self.tournament.serialize()
                db_tournament.update_db(serialize, self.tournament.id, tournament=True)
                break
            else:
                self.view.display_message("Merci d'entrer un choix proposé (1 ou 2)")

        classment = Player.sort_players_list_by(self.tournament.players)
        self.view.display_message(f"{classment[0]} est le vainqueur")
        self.tournament.winner = classment[0]
        if self.tournament.current_round >= self.tournament.nb_rounds:
            self.tournament.status = 1

        else:
            self.tournament.status = 0
        serialize = self.tournament.serialize()
        if resume is False:
            db_tournament.save_db(serialize)
        if resume is True:
            db_tournament.update_db(serialize, self.tournament.id, tournament=True)

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
        for game in games:
            player1 = games[i][0]
            player2 = games[i][1]
            self.view.display_message(
                f"{player1.first_name} {player1.name} jouera contre {player2.first_name} {player2.name}"
            )
            i += 1

        i = 0
        for idx, player in enumerate(games):
            p1 = games[i][0]
            p2 = games[i][1]
            self.view.display_message(
                f"Match entre : {p1.first_name} {p1.name} et {p2.first_name} {p2.name} :"
            )
            total_score = 1
            p1_score = self.tournament.ask_score()
            p2_score = total_score - p1_score

            ps1 = PlayerScore(games[i][0], p1_score)

            ps2 = PlayerScore(games[i][1], p2_score)
            self.view.display_message(ps1)
            self.view.display_message(ps2)

            match = Match(ps1, ps1)

            self.tournament.meetings[ps1.player.id] = [ps2.player.id]
            self.view.display_message(self.tournament.meetings)

            matches.append(match)
            i += 1
        # Créer round
        self.tournament.current_round += 1
        round = Round("Round 1", matches, "13/01/2023", "13/01/2023", "Terminé")
        self.tournament.rounds.append(round)
        self.view.display_message(f" Round numéro : {self.tournament.current_round}")

        # Retourner Round
        return round

    def get_next_round(self):
        """Return a Round object"""
        # -Trier joueurs par ELO

        matches: list[Match] = self.tournament.get_matches()

        # Créer liste de match (vide)
        for match in matches:
            self.view.display_message("\nMatches : ")
            self.view.display_matches(match)

        for match in matches:
            player1 = match.player_score1
            player2 = match.player_score2
            self.view.display_message(
                (
                    f"\nMatch entre : {player1.player.first_name} {player1.player.name} "
                    f"et {player2.player.first_name} {player2.player.name} :"
                )
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
        self.view.display_message(
            f" Round numéro : {self.tournament.current_round} terminé"
        )

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
            self.view.display_message("Pas de tournois à afficher")
        if validation is True:
            self.view.ask_input("\nAppuyez sur Entreé pour continuer ")

    def show_running_tournament(self, validation=False):
        sorted_data = Tournament.in_progress_tournament()
        if sorted_data != []:
            self.view.display_tournament_historic(sorted_data)
            result = self.view.display_running_ask_id()
            if result == False:
                exit
            elif isinstance(result, int):
                self.resume_tournament(result)
        else:
            self.view.display_message("Pas de tournois à afficher")
        if validation is True:
            self.view.ask_input("\nAppuyez sur Entreé pour continuer ")

    def show_tournaments_rapports(self):
        data = db_tournament.sorted_by("tournament_name")
        sorted_data = Tournament.sort_tournament_data(data)
        self.view.display_tournament_historic(sorted_data)
        user_input = self.view.display_running_ask_id()
        verification = self.view.input_id_verification(user_input, validation=False)
        if verification is True:
            tournament_data = db_tournament.get_element_by_id(user_input)
            self.tournament = Tournament.deserialize(tournament_data)
            self.view.display_tournament_rapport(self.tournament)
            classment = Player.sort_players_list_by(self.tournament.players)
            self.view.display_tournament_final_classment(classment)

    def display_players_order_by_name(self):
        """Print players order by name"""
        return self.player_controller.display_players_order_by_name(validation=False)

    def resume_tournament(self, id):
        data = db_tournament.get_element_by_id(id)
        data["id"] = id
        self.tournament = Tournament.deserialize(data)
        self.play_tournament(resume=True)
