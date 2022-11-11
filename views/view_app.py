class ViewApp:

    def display_main_menu(self):
        """Display the main menu and return the user choice"""
        
        while True:
            print("\n", " Bienvenue dans chess manager ".center(80, '-'))
            print("\n1. Gestion des tournois")
            print("2. Gestion des joueurs")
            print("3. Quitter")

            choice = input("\nEntrez votre choix : ")

            if choice in ["1", "2", "3"]:
                if choice == "3":
                    print("Au revoir")
                    
                return choice

            print("Choix invalide.\n")