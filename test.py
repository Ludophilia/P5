"""Script de test pour insérer le nom des catégories choisies dans la table Categorie 20 produits de chaque catégorie choisie dans la table Produit"""

import mysql.connector
import requests

"""Pour se connecter à mysql"""

connection = mysql.connector.connect(
    user = 'p5',
    password = '12345',
    host = '127.0.0.1', 
    use_unicode = True
) #Such confidentiality, much secure, wow.

"""Pour insérer nom des categorie et """

categories = ["Biscuits et gâteaux"] #Commencer avec juste une catégorie (Biscuits et gâteaux), après charger catégories.txt. To hardcode or not to hardcode, that is the question

for category in categories : 
    pass