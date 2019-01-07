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

    #Pourquoi l'UI ne serait-elle pas composée de fonctions avec une fonction pour chaque menu 
 
    main_menu = ("\nBienvenue sur P5!\n"
        "Menu principal :\n"
        "1. Remplacer un aliment\n"
        "2. Retrouver mes aliments remplacés\n\n")

    UI = Ui(main_menu)
    
    UI.test_input(main_menu, 1,2) #Là, test_imp ne fait rien si user_imp est déjà un int
   
    if UI.user_input == 1 :  
        print("Parfait. Vous avez choisi de remplacer un aliment, c'est bien. Très bien même.")

        #Obj : Afficher la liste de la liste des categories à choisir 

        database.cursor.execute("SELECT nom FROM 5db.Categorie")
        results = database.cursor.fetchall() #Une liste de tuples  
        
        category_choices = list()

        for category, in results : category_choices += [category]
        category_choices = list(enumerate(category_choices, start = 1))

        category_menu = ("Choisissez désormais votre catégorie : \n")
        
        for number, choice in category_choices :
            category_menu += "{} : {} \n".format(number, choice)
        category_menu += "Votre choix ?\n"

        UI = Ui(category_menu) 

        #Obj : Faire en sorte que quand on choisit un chiffre (quand on fait un choix de catégorie) on obtienne la liste de produits associés. 

        #if ça va pas être terrible avec 36 choix, mais lancer une fonction qui prend en argument l'user_input serait sans doute meilleur

        #Retrouver le nom de la category à partir de l'input. Comment faire ? category_choices[user_input-1][1]

        UI.test_input(category_menu, 0+1, len(category_choices))

        category_chosen = category_choices[UI.user_input-1][1]

        def load_products (user_input) :
            
            product_choices = []

            database.cursor.execute("SELECT nom FROM 5db.Produit WHERE category_name = %s", [category_chosen]) 
            results = database.cursor.fetchall()

            for product, in results : product_choices += [product]
            product_choices = list(enumerate(product_choices, start = 1))

            return product_choices
        
        print("Vous avez choisi de remplacer de la, des, ou du {} et puis m*, je sé plus comment on di. Hum, choix intéressant... Très intéressant...\n".format(category_chosen))

        product_menu = ("Choisissez désormais l'aliment à remplacer : \n")

        product_choices = load_products (UI.user_input)

        for number, choice in product_choices :
            product_menu += "{} : {} \n".format(number, choice)
        product_menu += "Alors Alors ??\n"

        UI = Ui(product_menu)
        
        UI.test_input(product_menu, 0+1, len(product_choices))

        product_chosen = product_choices[UI.user_input-1][1]
        substitute_obtained = ""

        print("Vous avez choisi \"{}\"".format(product_chosen))

        #Obj/Que faire ensuite ? Donner à l'utilisateur un substitut au produit selectionné. 

        # Comment on fait ? 

        # On va partir sur une nouvelle fonction dont l'arg principal pourrait être l'user_imput.
        
        """Elle devra determiner le substitut à l'aliment, et récupérer des données  sur ce subsitut, description (ok), magasin où l'acheter (le cas échéant) (ok) et un lien vers la page d'Open Food Facts concernant cet aliment.(ok)""" 
        
        def determine_substitute () :
            
            database.cursor.execute("SELECT nom, description, off_url, category_name, retailer_name, nutriscore FROM 5db.Produit WHERE category_name = %s ORDER BY nutriscore LIMIT 1", [category_chosen])
            results = database.cursor.fetchall()

            #infos recherchées : nom, description,retailer_name, off_url, nutriscore, 
            
            #Pas besoin de retraiter les données. Il suffit juste d'explorer la liste results et d'appeler la bonne valeur au bon endroit. 

            values = dict(name = results[0][0],
                    description = results[0][1],
                    url = results[0][2],
                    retailer = results[0][4],
                    nutriscore = results[0][5],
                    choice = product_chosen)
            
            substitute_obtained = values["name"] 

            final_result = ("Voici un subtitut plus sain au produit \"{choice}\" que vous avez choisi :\n"
            "Nom : {name}\n"
            "Nutriscore : {nutriscore}\n"
            "Composition : {description}\n"
            "Vous pouvez acheter le produit ici : {retailer}\n"
            "Plus d'infos sur OpenFoodFacts à cette adresse : {url}\n"
            ).format(choice = values['choice'], url = values['url'], name = values['name'], nutriscore = values["nutriscore"], description = values["description"], retailer = values["retailer"])
            
            print(final_result)
           
            # Cette fonction determine en fait le produit le plus sain à partir de la categorie du produit et donc sans se soucier plus que ça du produit choisi...        
               
                # Pourquoi ne pas quand même afficher un message si le produit choisi n'est pas plus sain que l'alternative proposée ? 
                # Et proposer un autre message si le produit choisi est exactement celui qui est considéré comme l'alternative la meilleure. 

        determine_substitute()
        print("what is it", substitute_obtained) 


        #Qu'est-ce qu'on doit faire ? 

        #L'utilisateur doit pouvoir enregistrer dans la table le résultat qu'il a obtenu. 

        register_prompt = ("Voulez-vous enregistrer votre recherche pour la retrouver plus tard ?\n"
        "Astuce : il suffit pour cela de choisir la deuxième option depuis le menu principal\n"
        "1. Oui, je le veux!\n"
        "2. Non ! Et puis quoi encore !!\n")

        UI = Ui(register_prompt)
        
        UI.test_input(register_prompt, 1,2)
        
        if UI.user_input == 1 :
            print("nom substitut : ",substitute_obtained,
            "nom produit :", product_chosen)

            #On a le nom du produit mais pas celui du substitut car il a été défini dans une fonction. J'ai essayé de l'appeler avec globals mais la variable a été définie au niveau de la fonction main()...

            #Mieux vaut passer ce qu'on a fait en orienté objet et revenir ici pour le reste... Plus facile ensuite d'appeler l'attribut de l'ui : product chosen, subsitute determined...

            #Et attention au design de l'objet Ui. Mieux vaut une méthode pour prompt ce qu'on attend de l'utilisateur plutôt que de créer un nouvel objet à chaque fois. 

            #Obj :refactorer le code existant vers le paradigme orienté objet histoire de pouvoir manipuler plus facilement. 




        if UI.user_input == 2 :
            print(("Bien compris\n"
            "Merci d'avoir utilisé le programme, à une prochaine fois peut-être !!"))



        #Comment on fait ? 
        # Poser une question, attendre un chiffre
        # Tester l'input
        # Une requête SQL pour sûr. 
            # Laquelle ? Il faut le product_id et le substitute_id ? Comment les obtenir ? Requête de l'id avec le nom produit et nom substitut : 
            # SELECT id FROM Produit WHERE nom = "Pain au lait" ; > 96
            # SELECT id FROM Produit WHERE nom = "Pitch brioches Pépites de Chocolat (x 8)" ; > 82
            #Reste à savoir où récupérer le nom produit.

    elif UI.user_input == 2 : 
        #Choix retrouver mes aliments remplacés

        #Obj, qu'est ce qu'on doit faire ? 

        #Charger les requêtes que l'utilisateur a enregistré.

        #Comment on fait ?

        #Au minimum, une requête SQL.

        #Prevoir aussi ce qu'il faut faire si une requête a déjà été enregistrée.

        print("Choix 2. En construction.")
    
    database.close_cursor()

if __name__ == "__main__" : 
    main()