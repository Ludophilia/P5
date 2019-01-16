# P5

*P5* permet de **trouver un substitut de meilleure qualité nutritionnelle** à une liste d’aliments de tous les jours

## Dépendances

- Mysql 14.14 distrib 5.7.24
- Mysql-connector-python 8.0.13
- Requests 2.21.0

## Fonctionnalités

- Recherche d’un substitut de meilleure qualité nutritionnelle à un produit choisi
- Classification des produits par catégorie pour une recherche de produit facilitée.
- Accès à des informations pratiques sur le substitut sain pour en savoir plus et faciliter son achat
- Enregistrement de la recherche et de son résultat
- Accès aux recherches enregistrées
- Navigation ergonomique : navigation par touche du clavier

## Démarrage

> python3 main.py

## Installation de la base de données et remplissage

Créer la base de données et la remplir :
> python3 main.py -b [--build_db]

Bénéficier d'un retour d'informations lors du remplissage :
> python3 main.py -v [--verbose]
