"""Script de test pour insérer le nom des catégories choisies dans la table Categorie 20 produits de chaque catégorie choisie dans la table Produit"""

import mysql.connector
import requests

"""Pour se connecter à mysql et initialiser un curseur"""

connection = mysql.connector.connect(
    #Much confidentiality, such secure, wow.
    user = 'p5',
    password = '12345',
    host = '127.0.0.1', 
    use_unicode = True) 

cursor = connection.cursor() 

"""Pour créer la base de données"""

def create_db() :    
    with open("database.sql") as f : 
        for x in f.read().split(';') : 
            cursor.execute(x)

create_db()

"""Pour insérer nom des categorie et donnes des catégories"""

categories = ["Biscuits et gâteaux"] #Commencer avec juste une catégorie (Biscuits et gâteaux), après charger catégories.txt. To hardcode or not to hardcode, that is the question

def add_database(nom_table, *values) :

    add_stmt = ("INSERT INTO " + nom_table + " "
                "VALUES " + str(values)) #Version simple sans valeurs remplacés par %s ou %(name)s à améliorer
    print(add_stmt)
    cursor.execute(add_stmt)

for category in categories : 
    #J'aimerais bien ajouter la catégorie à la table categorie
    add_database("5db.Categorie", category, "NULL") 

    connection.commit() 

cursor.close()
connection.close()