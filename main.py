import argparse
from classes import *

parser = argparse.ArgumentParser(description="Main script for Projet P5. Help you to improve your diet.")

parser.add_argument('-b', '--build_db', help = "Enable or disable database creation and filling", action = "store_true")
parser.add_argument('-v', '--verbose', help = "Make table filling and data testing talkative", action = "store_true")

args = parser.parse_args()

def main(): #La pep8, c'est if: et pas if: (80c) #pycodestyle #un fichier requierement.txt (pour que qqn puisse installer le programme) #
    database = Database("p5", "12345", "127.0.0.1", True, args.verbose)
    UI = Ui()

    if args.build_db == True:  
        
        nutriscores = Structural_data("nutriscores.txt") 
        categories = Structural_data("categories-short.txt")

        database.create_database("database.sql", ";")
    
        for nutriscore in nutriscores.listversion:
            database.add_to_table("5db.Nutriscore", nutriscores.prepared_for_insertion(nutriscore))

        for category in categories.listversion: 
            database.add_to_table("5db.Categorie", categories.prepared_for_insertion(category))

            products = Product_data(category,20, 1, args.verbose)

            for product in products.listversion: 
                if products.key_tester(product) == False: 
                    database.add_to_table("5db.Produit", products.prepared_for_insertion(category, product))
                    
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
           
        UI.ask_user(UI.save_menu)  
        UI.test_input(UI.save_menu, 1,2)
        
        if UI.user_input == 1:
            
            database.retrieve_id(UI)
            database.add_to_table("5db.Recherche", UI.id_list)

            print(("Recherche enregistrée !\n"
            "Merci d'avoir utilisé le programme, à une prochaine fois peut-être !!")) #Pas de condition qui déclenche ceci ? Donc ça arrive même si le produit est déjà enregistré
    
        elif UI.user_input == 2:
            
            print(("Bien compris\n"
            "Merci d'avoir utilisé le programme, à une prochaine fois peut-être !!"))

    elif UI.user_input == 2: 
        print("Vous avez choisi de retrouver un aliment déjà remplacé.\n")

        database.retrieve_data("substitution_data", UI)
        UI.build_selection("substitution_menu")
        UI.ask_user(UI.substitution_menu)
        UI.test_input(UI.substitution_menu, 1,len(UI.subtitution_choices))
        UI.set_chosen("substitute_chosen")
        database.retrieve_data("substitute_data", UI)
        UI.display_substitute()

        #Prevoir aussi ce qu'il faut faire si on essaie d'enregistrer une requête qui a déjà été enregistrée.

        print("Merci d'avoir utilisé le programme, à une prochaine fois peut-être !!")
    
    database.close_cursor()

if __name__ == "__main__": 
    main()