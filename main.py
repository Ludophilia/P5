import argparse
from classes import *

parser = argparse.ArgumentParser(description="Main script for Projet P5. Help you to improve your diet.")

parser.add_argument('-b', '--build_db', help = "Enable or disable database creation and filling", action = "store_true")
parser.add_argument('-v', '--verbose', help = "Make table filling and data testing talkative", action = "store_true")

args = parser.parse_args()
print(args)

def main() : 
    database = Database("p5", "12345", "127.0.0.1", True, args.verbose)

    if args.build_db == True :  #Ajoutez en UI. Voulez-vous construire la base ? Voulez-vous remplir les tables ?
        
        nutriscores = Structural_data("nutriscores.txt") 
        categories = Structural_data("categories-short.txt") #On en aura peut être besoin de nouveau, pour le moment, ça reste ici...

        database.create_database("database.sql", ";")
    
        for nutriscore in nutriscores.listversion :
            database.add_to_table("5db.Nutriscore", nutriscores.prepared_for_insertion(nutriscore))

        for category in categories.listversion : 
            database.add_to_table("5db.Categorie", categories.prepared_for_insertion(category))

            products = Product_data(category,20, 1, args.verbose) #On peut prendre plus de pages qu'une seule... afficher plus de produits que 20.

            for product in products.listversion : 
                if products.key_tester(product) == False : 
                    database.add_to_table("5db.Produit", products.prepared_for_insertion(category, product))
                    
    # Obj : Coder l'interface utilisateur ! On l'a designé dans un document à part, il faut juste réaliser ce qu'on a pensé...

    #La suite ?
 
    menu_prompt = ("\nBienvenue sur P5!\n"
        "Menu principal :\n"
        "1. Remplacer un aliment\n"
        "2. Retrouver mes aliments remplacés\n\n")

    uinput = Ui(menu_prompt)
    print("après 1er user_input", uinput.user_input)
    uinput.test_input(menu_prompt)
    print("après test_input", uinput.user_input, type(uinput.user_input))

    if uinput.user_input == 1 :  
        print("OK")
    
    else :
        print("PAS OK")
    
    database.close_cursor()

if __name__ == "__main__" : 
    main()