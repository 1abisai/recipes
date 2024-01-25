from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DB

from flask_app.models import user_model

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30_minutes = data['under_30_minutes']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    #this validates recipe entries
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be atleast 3 characters")
            is_valid = False


        if len(recipe['description']) < 3:
            flash("Descriptions must be atleast 3 characters")
            is_valid = False

        
        if len(recipe['instruction']) < 3:
            flash("Instructions must be atleast 3 characters")
            is_valid = False

        
        if len(recipe['date_cooked']) < 3:
            flash("Please enter date")
            is_valid = False
        
        return is_valid 
    
    #create a recipe method
    @classmethod
    def create_recipe(cls, data):
        
        query = """
            INSERT INTO recipes (user_id, name, description, instruction, under_30_minutes, date_cooked)
            VALUES (%(user_id)s, %(name)s, %(description)s, %(instruction)s, %(under_30_minutes)s, %(date_cooked)s)
        """
        
        results = connectToMySQL(DB).query_db(query, data)

        return results

    #read all recipes method
    @classmethod
    def read_all_recipes(cls):
        query = """
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id;
        """
        
        results = connectToMySQL(DB).query_db(query)

        all_recipes = []
        
        for row in results:
            recipe = cls(row)

            creator_data = {
             # **row reads and makes copy of every key value pair in dictionary
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }

            recipe.creator = user_model.User(creator_data)

            all_recipes.append(recipe)

        return all_recipes

    @classmethod
    def read_one_recipe(cls, data):
        query = """
            SELECT * FROM recipes WHERE id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query, data)

        return cls(results[0])

#update recipe
    @classmethod
    def update_recipe(cls, data):
        query = """
            UPDATE recipes 
            SET  name=%(name)s, description=%(description)s, 
            instruction=%(instruction)s, under_30_minutes=%(under_30_minutes)s, 
            date_cooked=%(date_cooked)s
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query, data)
        return results

#delete recipe
    @classmethod
    def delete_recipe(cls, data):
    
        query = """
            DELETE FROM recipes WHERE id = %(id)s
        """

        results = connectToMySQL(DB).query_db(query, data)

        if results == None:
            return "success"
        else:
            return "failure"

