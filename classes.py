import mysql.connector
import requests

class Database : 
    
    def __init__(self, user, password, host, use_unicode) : 
        
        self.connection = mysql.connector.connect(
            user = user,
            password = password,
            host = host, 
            use_unicode = use_unicode)
          
        self.cursor = self.connection.cursor()

    def create_database(self, sql_file, sep) : 
        with open(sql_file) as f : 
            for statement in f.read().split(sep) : 
                self.cursor.execute(statement) 
    def add_to_table(self, table_name, values) : 
        extra_statement = {
        "5db.Categorie" : " (nom) VALUES (%s)", 
        "5db.Nutriscore" : " (grade) VALUES (%s)",
        "5db.Produit" : " (nom, description, quantite, off_url, category_name, retailer_name, nutriscore) VALUES (%(product_name)s, %(ingredients_text)s, %(quantity)s, %(url)s, %(categories)s, %(stores)s, %(nutrition_grade_fr)s)"} 
        addtotable_statement = ("INSERT INTO " + table_name + extra_statement[table_name]) 

        self.cursor.execute(addtotable_statement, values)

    def close_cursor(self) : 
        return self.cursor.close()

class Structural_data :
    
    def __init__(self, data_file) : 
        self.data_file = data_file
    
    @property
    def listversion (self) : 
        data_list = []
        with open(self.data_file) as f : 
            for data in f.read().splitlines() :
                data_list += [data]
        return data_list
    
    def prepared_for_insertion(self, value) :
        data_to_insert = []
        data_to_insert += [value] 
        return data_to_insert

class Product_data :
    
    def __init__ (self, search_terms, page_size, page_number) : 
        self.search_pr = {"action" : "process", "search_terms" : search_terms, "sort_by" : "unique_scans_n", "page_size" : page_size, "page" : page_number, "json": "true"}
        self.data = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = self.search_pr)
        self.keys_to_check = ["product_name", "ingredients_text", "quantity", "url", "categories", "stores", "nutrition_grade_fr"]

    @property    
    def listversion (self) :
        return self.data.json()['products']

    def prepared_for_insertion(self, category, product) : 
        data_to_insert = dict()
        for key in self.keys_to_check : 
            if key == "categories" :
                data_to_insert[key] = category 
            else :    
                data_to_insert[key] = product[key] #Attention au KeyError !
        return data_to_insert

    def key_tester (self, product) : 
        keys_missing = dict() 
        key_problem = False
        for value_tested in self.keys_to_check :
            try :
                if len(product[value_tested]) == 0 :
                    keys_missing[value_tested] = "this key returns no value for product " + product["product_name"]
                    print(keys_missing) 

            except KeyError : 
                try :
                    key_problem = True
                    keys_missing[value_tested] = "WARNING : this key does not exist in product " + product["product_name"] 
                    print(keys_missing)
                except KeyError : 
                    key_problem = True
                    keys_missing[value_tested] = "WARNING : this key does not exist in this product. Unable to give product's name because its key does not exist."
                    print(keys_missing)

        return True if "nutrition_grade_fr" in keys_missing or "product_name" in keys_missing or key_problem == True else False