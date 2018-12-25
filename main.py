
from classes import *


def main() : 
    database = Database("p5", "12345", "127.0.0.1", True)
    connection = database.connection
    database.create_database("database.sql", ";")

    nutriscores = Structural_data("nutriscores.txt")
    categories = Structural_data("categories-short.txt")

    try :
        for nutriscore in nutriscores.listversion :
            database.add_to_table("5db.Nutriscore", nutriscores.prepared_for_insertion(nutriscore))
            connection.commit()
    except : 
        print("Nutriscore already inserted, moving on...")

    for category in categories.listversion : 
        try : 
            database.add_to_table("5db.Categorie", categories.prepared_for_insertion(category))
            connection.commit()
        except : 
            print("Category already inserted, moving on...")

        products = Product_data(category,20, 1) #On peut prendre plus de pages qu'une seule... afficher plus de produits que 20.

        for product in products.listversion : 
            if products.key_tester(product) == False : 
                try : 
                    database.add_to_table("5db.Produit", products.prepared_for_insertion(category, product))
                    connection.commit()
                except mysql.connector.errors.IntegrityError :
                    print("Product already inserted, moving on...") 
                    
    database.close_cursor()
    connection.close()

if __name__ == "__main__" : 
    main()