import argparse
from classes import *

parser = argparse.ArgumentParser(description="Main script for Projet P5. Help you to improve your diet.")

parser.add_argument('-b', '--build_db', help = "Enable or disable database creation and filling", action = "store_true")
parser.add_argument('-v', '--verbose', help = "Make table filling and data testing talkative", action = "store_true")

args = parser.parse_args()
# print(args)

def main() : 
    database = Database("p5", "12345", "127.0.0.1", True, args.verbose)
    
    nutriscores = Structural_data("nutriscores.txt")
    categories = Structural_data("categories-short.txt")

    if args.build_db == True : #il faut peut-être utiliser argparser pour activer et desactiver la création et le remplissage de la db sur commande 
        database.create_database("database.sql", ";")
    
        for nutriscore in nutriscores.listversion :
            database.add_to_table("5db.Nutriscore", nutriscores.prepared_for_insertion(nutriscore))

        for category in categories.listversion : 
            database.add_to_table("5db.Categorie", categories.prepared_for_insertion(category))

            products = Product_data(category,20, 1, args.verbose) #On peut prendre plus de pages qu'une seule... afficher plus de produits que 20.

            for product in products.listversion : 
                if products.key_tester(product) == False : 
                    database.add_to_table("5db.Produit", products.prepared_for_insertion(category, product))
                    
    """ Test de l'interface utilisateur """ #A poor use of docstrings, isn't it?

    print('') 

    database.close_cursor()

if __name__ == "__main__" : 
    main()