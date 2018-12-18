CREATE DATABASE IF NOT EXISTS 5db CHARACTER SET 'utf8';

USE 5db;

CREATE TABLE IF NOT EXISTS Nutriscore ( 
    grade CHAR(1) NOT NULL, 
    description TEXT,
    PRIMARY KEY (grade)
) ENGINE = INNODB; 

-- CREATE TABLE IF NOT EXISTS Nova (
--     group_id INT(1) UNSIGNED NOT NULL,
--     description TEXT,
--     PRIMARY KEY (group_id)
-- ) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS Categorie (
    nom VARCHAR(50) NOT NULL,
    description TEXT,
    PRIMARY KEY (nom)
) ENGINE = INNODB; 

CREATE TABLE IF NOT EXISTS Produit (
    -- Changements sur category_name et retailer_name Passage de VARCHAR(50) à VARCHAR(200) 
    id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    nom VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    quantite DECIMAL(5,1) UNSIGNED,
    off_url TEXT,
    category_name VARCHAR(200) NOT NULL, 
    retailer_name VARCHAR(200) NOT NULL,
    nutriscore CHAR(1) NOT NULL,
    -- groupe_nova INT(1) UNSIGNED NOT NULL,
    nutrition_score_100g INT UNSIGNED NOT NULL,
    lipides_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    gras_satures_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    sucres_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    sel_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    -- CONSTRAINT fk_nova_group FOREIGN KEY (groupe_nova) REFERENCES Nova(group_id),
    CONSTRAINT fk_nutriscore_grade FOREIGN KEY (nutriscore) REFERENCES Nutriscore(grade),
    CONSTRAINT fk_category_id FOREIGN KEY (category_name) REFERENCES Categorie(nom)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS Recherche (
    product_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, substitute_id), 
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Produit(id),
    CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Produit(id) 
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS Test (
    -- Table de test sans les contraintes de clés étrangères
    id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    nom VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    quantite DECIMAL(5,1) UNSIGNED,
    off_url TEXT,
    category_name VARCHAR(200) NOT NULL, 
    retailer_name VARCHAR(200) NOT NULL,
    nutriscore CHAR(1) NOT NULL,
    groupe_nova INT(1) UNSIGNED NOT NULL,
    nutrition_score_100g INT UNSIGNED NOT NULL,
    lipides_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    gras_satures_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    sucres_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    sel_100g DECIMAL(4,1) UNSIGNED NOT NULL,
    PRIMARY KEY (id)
) ENGINE = INNODB;