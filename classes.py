import mysql.connector
import requests
import time

class Ui:
    def __init__(self):
        self.user_input = str()
        self.freeze_time = int()
        self.main_menu = ("Bienvenue sur P5!\n" "Menu principal:\n" "1. Remplacer un aliment\n"
        "2. Retrouver mes aliments remplacés\n")
        self.names_retrieved = list()
        self.category_menu = ("Choisissez désormais votre catégorie: \n")
        self.category_choices = list()
        self.category_chosen = str()
        self.product_menu = ("Choisissez désormais l'aliment à remplacer: \n")
        self.product_choices = list()
        self.product_chosen = str()
        self.substitute_data = dict()
        self.substitute_name = str()
        self.substitute_prompt = str()
        self.save_menu = ("Voulez-vous enregistrer votre recherche pour la retrouver plus tard ?\n"
        "Astuce: pour retrouver votre recherche, choisissez la deuxième option depuis le menu principal\n"
        "1. Oui, je le veux !\n"
        "2. Non ! Et puis quoi encore !!\n")
        self.id_list = list()
        self.subtitution_choices = list() 
        self.substitution_menu = ("Choisissez une substitution:\n")
        self.substitute_chosen = str()
        self.id_substitute_chosen = int()

    def ask_user(self, message): 
        self.user_input = input(message)

    def build_selection(self, menu_type):

        if menu_type == "category_menu": 
   
            for item, in self.names_retrieved: self.category_choices += [item]
            self.category_choices = list(enumerate(self.category_choices, start = 1))

            for number, choice in self.category_choices:
                self.category_menu += "{}: {} \n".format(number, choice)

            self.category_menu += "Votre choix ?\n"
        
        if menu_type == "product_menu": 
            
            for item, in self.names_retrieved: self.product_choices  += [item]
            self.product_choices  = list(enumerate(self.product_choices , start = 1))

            for number, choice in self.product_choices :
                self.product_menu += "{}: {} \n".format(number, choice)
            
            self.product_menu += "Alors alors ??\n"

        if menu_type == "substitution_menu": 
            self.subtitution_choices = list(enumerate(self.names_retrieved, start = 1))

            for number, ((product, product_id), (substitute, substitute_id)) in self.subtitution_choices:
                self.substitution_menu += "{}: {} remplacé par {} \n".format(number, product, substitute)
            self.substitution_menu += "Votre choix ?\n"

    def display_substitute (self): 
      
        # Cette fonction determine en fait le produit le plus sain à partir de la categorie du produit et donc sans se soucier plus que ça du produit choisi...   
        # Pourquoi ne pas quand même afficher un message si le produit choisi n'est pas plus sain que l'alternative proposée ? 
        # Et proposer un autre message si le produit choisi est exactement celui qui est considéré comme l'alternative la meilleure. 

        self.substitute_data = {
            "name": self.names_retrieved[0][0],
            "description": self.names_retrieved[0][1],
            "url": self.names_retrieved[0][2],
            "retailer": self.names_retrieved[0][4],
            "nutriscore": self.names_retrieved[0][5],
            "choice": self.product_chosen }

        self.substitute_name = self.substitute_data["name"]

        self.substitute_prompt = ("Voici un subtitut plus sain au produit \"{choice}\" que vous avez choisi de remplacer: \n"
            "Nom: {name}\n"
            "Nutriscore: {nutriscore}\n"
            "Composition: {description}\n"
            "Vous pouvez acheter le produit ici: {retailer}\n"
            "Plus d'infos sur OpenFoodFacts à cette adresse: {url}\n"
            ).format(choice = self.substitute_data['choice'], 
            url = self.substitute_data['url'], 
            name = self.substitute_data['name'], 
            nutriscore = self.substitute_data["nutriscore"], 
            description = self.substitute_data["description"], 
            retailer = self.substitute_data["retailer"])

        print(self.substitute_prompt)

    def set_chosen(self, choice_type): 
        
        if choice_type == "category_chosen": 
            
            self.category_chosen = self.category_choices[self.user_input-1][1]
        
        if choice_type == "product_chosen": 

            self.product_chosen = self.product_choices[self.user_input-1][1]
     
        if choice_type == "substitute_chosen": 
            
            self.product_chosen = self.subtitution_choices[self.user_input-1][1][0][0]

            self.substitute_chosen = self.subtitution_choices[self.user_input-1][1][1][0]

            self.id_substitute_chosen = self.subtitution_choices[self.user_input-1][1][1][1]

    def test_input(self, re_message, min_choice, max_choice):

        type_error = ("Le caractère que vous avez entré n'est pas un chiffre ou un nombre.\n"
        "Veuillez entrer un nombre s'il vous plait")
        range_error = "Choississez entre {} et {} pour bénéficier du programme".format(min_choice, max_choice)

        while type(self.user_input) != int and self.user_input not in range(min_choice, max_choice+1):
            
            try: 
                self.user_input = int(self.user_input)
                assert self.user_input in range(min_choice, max_choice+1)

            except ValueError:
                print (type_error)
                time.sleep(self.freeze_time)
                self.user_input = input(re_message) 
            
            except AssertionError:
                print (range_error)
                self.user_input = input(re_message) 

class Database: 
    
    def __init__(self, user, password, host, database, use_unicode, verbosity): 
        
        self.connection = mysql.connector.connect(
            user = user,
            password = password,
            host = host, 
            database = database,
            use_unicode = use_unicode) 
          
        self.cursor = self.connection.cursor()
        self.verbose = verbosity

    def retrieve_data(self, type_data, Ui_object):

        if type_data == "category_data" or type_data == "product_data" or type_data == "substitute_data": 
            if type_data == "category_data":
                self.cursor.execute("SELECT name FROM 5db.Category")

            elif type_data == "product_data":
                self.cursor.execute("SELECT name FROM 5db.Product WHERE category = %s", [Ui_object.category_chosen]) 

            elif type_data == "substitute_data": 
                
                if len(Ui_object.category_chosen) !=0: 
                    self.cursor.execute("SELECT name, description, url, category, retailer, nutriscore FROM 5db.Product WHERE category = %s ORDER BY nutriscore LIMIT 1", [Ui_object.category_chosen])
                     
                elif Ui_object.id_substitute_chosen != 0: 
                    self.cursor.execute("SELECT name, description, url, category, retailer, nutriscore FROM 5db.Product WHERE id = %s", [Ui_object.id_substitute_chosen])

            Ui_object.names_retrieved = self.cursor.fetchall()

        elif type_data == "substitution_data":
            
            self.cursor.execute("SELECT * FROM 5db.Research")
            id_data = self.cursor.fetchall()

            for product_id, substitute_id in id_data: 

                self.cursor.execute("SELECT name FROM 5db.Product WHERE id = %s", [product_id])
                product_name = self.cursor.fetchall()[0][0]

                self.cursor.execute("SELECT name FROM 5db.Product WHERE id = %s", [substitute_id])
                substitute_name = self.cursor.fetchall()[0][0]

                Ui_object.names_retrieved += [((product_name, product_id), (substitute_name, substitute_id))]

    def retrieve_id(self, Ui_object):

        for name in [Ui_object.product_chosen, Ui_object.substitute_name]: 
            self.cursor.execute("SELECT id FROM 5db.Product WHERE name = %s", [name]) 
            Ui_object.id_list += [self.cursor.fetchall()[0][0]]

    def create_database(self, sql_file, sep): 
        with open(sql_file) as f: 
            for statement in f.read().split(sep): 
                self.cursor.execute(statement) 
    
    def add_to_table(self, table_name, values): 
        
        extra_statement = {
        "5db.Category": " (name) VALUES (%s)", 
        "5db.Nutriscore": " (grade) VALUES (%s)",
        "5db.Product": " (name, description, quantity, url, category, retailer, nutriscore) VALUES (%(product_name)s, %(ingredients_text)s, %(quantity)s, %(url)s, %(categories)s, %(stores)s, %(nutrition_grade_fr)s)",
        "5db.Research": " (product_id, substitute_id) VALUES (%s, %s)"} 
        
        addtotable_statement = ("INSERT INTO " + table_name + extra_statement[table_name]) 

        try: 
            self.cursor.execute(addtotable_statement, values)
            self.connection.commit()

        except mysql.connector.errors.IntegrityError:
            if self.verbose == True:
                print("Item déjà enregistré dans {}, produit suivant!".format(table_name))

    def close_cursor(self): 
        return self.cursor.close()

class Structural_data:
    
    def __init__(self, data_file): 
        self.data_file = data_file
    
    @property
    def listversion (self): 
        data_list = []
        with open(self.data_file) as f: 
            for data in f.read().splitlines():
                data_list += [data]
        return data_list
    
    def prepared_for_insertion(self, value):
        data_to_insert = []
        data_to_insert += [value] 
        return data_to_insert

class Product_data:

    def __init__ (self, search_terms, page_size, page_number, verbosity): 
        self.search_pr = {"action": "process", "search_terms": search_terms, "sort_by": "unique_scans_n", "page_size": page_size, "page": page_number, "json": "true"}
        self.data = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = self.search_pr)
        self.keys_to_check = ["product_name", "ingredients_text", "quantity", "url", "categories", "stores", "nutrition_grade_fr"]
        self.verbose = verbosity

    @property    
    def listversion (self):
        return self.data.json()['products']

    def prepared_for_insertion(self, category, product): 
        data_to_insert = dict()
        for key in self.keys_to_check: 
            if key == "categories":
                data_to_insert[key] = category 
            else:    
                data_to_insert[key] = product[key] 
        return data_to_insert

    def key_tester (self, product): 
        keys_missing = dict() 
        key_problem = False
        for value_tested in self.keys_to_check:
            try:
                if len(product[value_tested]) == 0:
                    keys_missing[value_tested] = "this key returns no value for product " + product["product_name"]
                    
                    if self.verbose == True:
                        print(keys_missing) 

            except KeyError: 
                try:
                    key_problem = True
                    keys_missing[value_tested] = "WARNING: this key does not exist in product " + product["product_name"] 
                    if self.verbose == True:
                        print(keys_missing) 
                except KeyError: 
                    key_problem = True
                    keys_missing[value_tested] = "WARNING: this key does not exist in this product. Unable to give product's name because its key does not exist."
                    if self.verbose == True:
                        print(keys_missing) 

        return True if "nutrition_grade_fr" in keys_missing or "product_name" in keys_missing or key_problem == True else False