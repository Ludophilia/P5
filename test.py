"""Script de test pour (1) insérer dans la table Categorie les catégories sélectionnées et (2) insérer dans la table Produit les 20 produits les + populaires de chaque catégorie"""

import mysql.connector
import requests

"""Pour se connecter à mysql et initialiser un curseur"""

connection = mysql.connector.connect(
    user = 'p5',
    password = '12345',
    host = '127.0.0.1', 
    use_unicode = True) 
    # Connexion à la base comme un gros noob. Amazingly secure.  

cursor = connection.cursor() 

"""Pour créer la base de données"""

def create_db() :    
    cursor2 = connection.cursor() 

    with open("database.sql") as f : 
        for x in f.read().split(';') : 
            cursor2.execute(x)
            # print(x)
    cursor2.close()

create_db()

"""Pour effectuer une recherche dans OFF et obtenir un json"""

def search_off(search_term, page_size, page) : 
    param = {"action" : "process", "search_terms" : search_term, "sort_by" : "unique_scans_n", "page_size" : page_size, "page" : page, "json": "true"} 
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = param)
    return r.json()

"""Pour insérer le nom des categories dans la table Categorie et insérer 20 produits de chaque categorie dans la table Produit"""

categories = ["Biscuits et gâteaux"] #Commencer avec juste une catégorie (Biscuits et gâteaux), après charger catégories.txt. To hardcode or not to hardcode, that is the question

nutriscores = ["a", "b", "c", "d", "e"] #A mettre dans le fichier nutriscore.txt ?

def add_to_table(table_name, values) :
    extra_statement = {
        "5db.Categorie" : " (nom) VALUES (%s)", 
        "5db.Nutriscore" : " (grade) VALUES (%s)",
        "5db.Produit" : " (nom, description, quantite, off_url, category_name, retailer_name, nutriscore) VALUES (%(product_name)s, %(ingredients_text)s, %(quantity)s, %(url)s, %(categories)s, %(stores)s, %(nutrition_grade_fr)s)"} #%s peut-être utilisé avec des listes plutôt que les tuples de l'exemple de la doc ? Oui. 

    addtotable_statement = ("INSERT INTO " + table_name + extra_statement[table_name]) 
    cursor.execute(addtotable_statement, values)

def vacuum_tester(product) : 
    keys_to_test = ["product_name", "ingredients_text", "quantity", "url", "categories", "stores", "nutrition_grade_fr"]
    keys_missing = dict() 
    for value_tested in keys_to_test :
        try : 
            if len(product[value_tested]) == 0 : 
                keys_missing[value_tested] = "missing for " + product["product_name"]
                print(keys_missing) 

        except KeyError : 
            try :
                keys_missing[value_tested] = "missing for " + product["product_name"] 
                print("Exception raised for", keys_missing)
            except : 
                keys_missing[value_tested] = "missing" 
                print("Exception raised for ", keys_missing, ". Unable to give product_name because its key is missing")
    
    return True if "nutrition_grade_fr" in keys_missing or "product_name" in keys_missing else False

def values_for_nutricat(value) : #args : product["nutrition_grade_fr"] or category
    values_to_process = []
    values_to_process += [value] 
    return values_to_process 
    
def values_for_produit(product, category) : 
    keys_to_check = ["product_name", "ingredients_text", "quantity", "url", "categories", "stores", "nutrition_grade_fr"] #Cette liste apparait maintenant à deux endroits différents : ici et dans vaccuum_tester().

    values_to_process = dict()
    for key in keys_to_check : 
        if key == "categories" :
            values_to_process[key] = category 
        else :    
            values_to_process[key] = product[key]
    return values_to_process 

#Obj : Ajouter les nutriscores 

try :
    for nutriscore in nutriscores : 
        add_to_table("5db.Nutriscore", values_for_nutricat(nutriscore))
        connection.commit() #Sans ça, les données n'étaient pas insérés dans la base, jeez
    
except :
    print("Nutriscore already inserted, moving on...")

for category in categories : 

    #Obj : ajouter la catégorie selectionnée à la table categorie
    
    try :
        add_to_table("5db.Categorie", values_for_nutricat(category)) 
        connection.commit()

    except : #Type de l'erreur? ValueError?
        print("Category already inserted, moving on...")
    
    #Obj : Ajouter les 20 produits les plus pop de la catégorie select à la table Produit
    
    for product in search_off(category, 20, 1)['products'] :
        
        if vacuum_tester(product) == False :
           
            try : 
                add_to_table("5db.Produit", values_for_produit(product, category))
                connection.commit()

            except mysql.connector.errors.IntegrityError : 

                print("Product already inserted, moving on...")

cursor.close()
connection.close()
