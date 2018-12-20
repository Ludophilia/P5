CREATE DATABASE IF NOT EXISTS 5db CHARACTER SET 'utf8';

USE 5db;

CREATE TABLE IF NOT EXISTS Nutriscore ( 
    grade CHAR(1) NOT NULL, 
    description TEXT,
    PRIMARY KEY (grade)
) ENGINE = INNODB; 

CREATE TABLE IF NOT EXISTS Categorie (
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    PRIMARY KEY (nom)
) ENGINE = INNODB; 

CREATE TABLE IF NOT EXISTS Produit (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    nom VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    quantite VARCHAR(100),
    off_url TEXT,
    category_name VARCHAR(200) NOT NULL, 
    retailer_name VARCHAR(200),
    nutriscore CHAR(1) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_nutriscore_grade FOREIGN KEY (nutriscore) REFERENCES Nutriscore(grade),
    CONSTRAINT fk_category_id FOREIGN KEY (category_name) REFERENCES Categorie(nom)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS Recherche (
    product_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, substitute_id), 
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Produit(id),
    CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Produit(id) 
) ENGINE = INNODB; -- Attention aux lignes vides qui risquent d'être découpées par .split() et considérés comme une requête vide