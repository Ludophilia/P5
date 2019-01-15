from classes import *
import config as cfg

def main():
    
    UI = Ui(1.5)

    UI.add_argument_to_parser('-b', '--build_db', "Enable or disable database creation and filling", "store_true")
    UI.add_argument_to_parser('-v', '--verbose', "Make table filling and data testing talkative", "store_true")

    database = Database(
        cfg.mysql['user'], 
        cfg.mysql['password'],
        cfg.mysql['host'], 
        cfg.mysql['database'], 
        cfg.mysql['use_unicode'],
        UI.parser_args.verbose)
    
    if UI.parser_args.build_db is True:  
        
        nutriscores = Structural_data("nutriscores.txt") 
        categories = Structural_data("categories-short.txt")

        database.create_database("database.sql", ";")
    
        for nutriscore in nutriscores.listversion:
            database.add_to_table("5db.Nutriscore", nutriscores.prepared_for_insertion(nutriscore))

        for category in categories.listversion: 
            database.add_to_table("5db.Category", categories.prepared_for_insertion(category))

            products = Product_data(category, 20, 1, UI.parser_args.verbose)

            for product in products.listversion: 
                if products.key_tester(product) == False: 
                    database.add_to_table("5db.Product", products.prepared_for_insertion(category, product))
    
    while UI.user_motivated is True :
        
        UI.ask_user(UI.main_menu)
        
        UI.test_input(UI.main_menu, 1,2)
    
        if UI.user_input == 1:  
            
            print("Parfait. Vous avez choisi de remplacer un aliment, c'est bien. Très bien même.")

            database.retrieve_data("category_data", UI)
            UI.build_selection("category_menu")
            UI.ask_user(UI.category_menu) 
            UI.test_input(UI.category_menu, 0, len(UI.category_choices))
            UI.set_chosen("category_chosen") 

            print("Vous avez choisi de remplacer un aliment de la catégorie \"{}\". Hum, choix très intéressant...\n".format(UI.category_chosen))

            database.retrieve_data("product_data", UI)
            UI.build_selection("product_menu")
            UI.ask_user(UI.product_menu) 
            UI.test_input(UI.product_menu, 0, len(UI.product_choices))
            UI.set_chosen("product_chosen")

            print("Vous avez choisi \"{}\". C'est un choix qui se défend.".format(UI.product_chosen))

            database.retrieve_data("substitute_data", UI)
            UI.display_substitute()
            
            if UI.substitute_name != UI.product_chosen:
                UI.ask_user(UI.save_menu)  
                UI.test_input(UI.save_menu, 1,2)
            
                if UI.user_input == 1:
                    
                    database.retrieve_id(UI)
                    database.add_to_table("5db.Research", UI.id_list)

                    print(("Recherche enregistrée !\n")) #Pas de condition qui déclenche ceci ? Donc ça arrive même si le produit est déjà enregistré
            
                elif UI.user_input == 2:
                    
                    print("Bien compris !\n")

        elif UI.user_input == 2: 
            
            print("Vous avez choisi de retrouver un aliment déjà remplacé.\n")

            #Faut mettre une condition dans le cas où la database est vide !!

            database.retrieve_data("substitution_data", UI)
            UI.build_selection("substitution_menu")
            UI.ask_user(UI.substitution_menu)
            UI.test_input(UI.substitution_menu, 1, len(UI.subtitution_choices))
            UI.set_chosen("substitute_chosen")
            database.retrieve_data("substitute_data", UI)
            UI.display_substitute()

            #Prevoir aussi ce qu'il faut faire si on essaie d'enregistrer une requête qui a déjà été enregistrée.
        
        UI.ask_user(UI.retry_menu)
        UI.test_input(UI.retry_menu, 1,2)

        if UI.user_input == 1: 
            print("Bien compris! C'est reparti alors!!\n")
            UI.reset_attributes()
        
        elif UI.user_input == 2 :
            print("C'est bien dommage :(\n")
            UI.user_motivated = False

    print("Merci d'avoir utilisé P5, à une prochaine fois peut-être !!")
    
    database.close_cursor()

if __name__ == "__main__": 
    main()