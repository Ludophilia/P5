import argparse
import time
from classes import *

parser = argparse.ArgumentParser(description="Main script for Projet P5. Help you to improve your diet.")

parser.add_argument('-b', '--build_db', help = "Enable or disable database creation and filling", action = "store_true")
parser.add_argument('-v', '--verbose', help = "Make table filling and data testing talkative", action = "store_true")

args = parser.parse_args()
print(args)

def main() : 
    database = Database("p5", "12345", "127.0.0.1", True, args.verbose)

    if args.build_db == True :  
        
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
                    
    ############################ Test de l'interface utilisateur ##############################
    
    def test_input(user_input, prompt) : #Separer le test et la valeur renvoyée

        while type(user_input) != int : #Prochaine étape, faire en sorte que la fonction
            try :
                user_input = int(user_input)
            
            except ValueError : 
                print(("Le caractère que vous avez entré n'est pas un chiffre ou un nombre.\n"
                "Veuillez entrer un nombre s'il vous plait"))
                time.sleep(2)
                user_input = input(prompt) 

   # Obj : Coder l'interface utilisateur ! On l'a designé dans un document à part, il faut juste réaliser ce qu'on a pensé...
    
    menu_prompt = ("\nBienvenue sur P5!\n"
        "Menu principal :\n"
        "1. Remplacer un aliment\n"
        "2. Retrouver mes aliments remplacés\n\n")

    error_prompt = ("Le caractère que vous avez entré n'est pas un chiffre ou un nombre.\n"
    "Veuillez entrer un nombre s'il vous plait")

    user_input = input(menu_prompt)

    if test_input(user_input, menu_prompt) == 1 :  
        print("OK")
    
    elif test_input(user_input, menu_prompt) == 2 :
        print("OK")
    
    else :
        print("PAS OK")

    database.close_cursor()

if __name__ == "__main__" : 
    main()