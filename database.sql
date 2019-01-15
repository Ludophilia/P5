CREATE DATABASE IF NOT EXISTS 5db CHARACTER SET 'utf8';

USE 5db;

CREATE TABLE IF NOT EXISTS Nutriscore ( 
    grade CHAR(1) NOT NULL, 
    PRIMARY KEY (grade)
) ENGINE = INNODB; 

CREATE TABLE IF NOT EXISTS Category (
    name VARCHAR(200) NOT NULL,
    PRIMARY KEY (name)
) ENGINE = INNODB; 

CREATE TABLE IF NOT EXISTS Product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    name VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    quantity VARCHAR(100),
    url TEXT,
    category VARCHAR(200) NOT NULL, 
    retailer VARCHAR(200),
    nutriscore CHAR(1) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_nutriscore_grade FOREIGN KEY (nutriscore) REFERENCES Nutriscore(grade),
    CONSTRAINT fk_category_id FOREIGN KEY (category) REFERENCES Category(name)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS Recherche (
    product_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, substitute_id), 
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Produit(id),
    CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Produit(id) 
) ENGINE = INNODB;