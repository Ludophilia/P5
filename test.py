"""Script de test pour (1) insérer dans la table Categorie les catégories sélectionnées et (2) insérer dans la table Produit les 20 produits les + populaires de chaque catégorie"""

import mysql.connector
import requests

"""Pour se connecter à mysql et initialiser un curseur"""

connection = mysql.connector.connect(
    user = 'p5',
    password = '12345',
    host = '127.0.0.1', 
    use_unicode = True
    # Connexion à la base comme un gros noob. Amazingly secure.) 

cursor = connection.cursor() 

"""Pour créer la base de données"""

def create_db() :    
    with open("database.sql") as f : 
        for x in f.read().split(';') : 
            cursor.execute(x)

create_db()

"""Pour effectuer une recherche dans OFF et obtenir un json"""

def off_search(search_term, page_size, page) : 
    
    #Possible d'appeler une fonction "function()" et de la manipuler comme une variable si la fonction return une donnée exploitable

    param = {"action" : "process", "search_terms" : search_term, "sort_by" : "unique_scans_n", "page_size" : page_size, "page" : page, "json": "true"} 

    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = param)

    return r.json()

"""Pour insérer le nom des categories dans la table Categorie et insérer 20 produits de chaque categorie dans la table Produit"""

categories = ["Biscuits et gâteaux"] #Commencer avec juste une catégorie (Biscuits et gâteaux), après charger catégories.txt. To hardcode or not to hardcode, that is the question

def add_database(nom_table, *values) :
    
    add_stmt = ("INSERT INTO " + nom_table + " "
                "VALUES " + str(values)) #Version simple sans valeurs remplacés par %s ou %(name)s à améliorer
    print(add_stmt)
    cursor.execute(add_stmt)

def vacuum_test(product, keys_to_test) : 
    
    a = dict() # product est un dict
    # print(keys_to_test)
    for value_tested in keys_to_test :
        print(value_tested)
        try : 
            # print((product[value_tested]))
            if len(product[value_tested]) == 0 : a[value_tested] = "missing" 

        except KeyError : 
            a[value_tested] = "missing"
    
    print(a)
    return True if "nutrition_grade_fr" in a else False

for category in categories : 
    
    #Obj : ajouter la catégorie selectionnée à la table categorie
    
    try :
        add_database("5db.Categorie", category, "NULL") 
        connection.commit() # Il y avait une solution à base de cursor.execute("Select nom FROM 5db.Categorie"), mais c'est plus cher.
    except : 
        print("Category already inserted, moving on...")
    
    #Obj : Ajouter les 20 produits les plus pop de la catégorie select à la table Produit

    for product in off_search(category, 20, 1)['products'] :
        
        #Il faut vérifier si les données importantes sont en place et passer à une autre produit si ce n'est pas le cas.

        #print(type(product)) On itère sur une liste de dict. Chaque itm est un dict, il faut lire certaines clés et verifier leurs valeurs.

        keys_to_test = ["product_name_fr", "ingredients_text", "quantity", "url", "categories", "stores", "nutrition_grade_fr"]
        list2 = ["nutrition-score-fr", "fat_100g", "saturated-fat_100g", "sugars_100g", "salt_100g"]
        
        if vacuum_test(product, keys_to_test) == False :
            print("IT WORKS")
        else : 
            print("IT DOESNT WORK GEEZ")
        # vacuum_test(product, keys_to_test)

        # print (product)
    
        # Pourquoi ne pas executer directement l'instruction d'insertion du produit dans la table ? Faut vérifier pour sûr avant...

cursor.close()
connection.close()
