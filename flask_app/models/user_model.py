from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DB

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash("Name must be atleast 3 characters.", "registration")
            is_valid = False
        
        if len(user['last_name']) < 3:
            flash("Last name must be atleast 3 characters.", "registration")
            is_valid = False
        
        if len(user['email']) < 3:
            flash("Email must be atleast 3 characters.", "registration")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "registration")
            is_valid = False

        if (re.fullmatch(EMAIL_REGEX, user['email'])):
            this_user = {
                'email' : user['email']
            }
            results = User.check_db(this_user)
            if len(results) != 0:
                flash('Email is already in use.', "registration")
                is_valid = False

        if len(user['password']) < 3:
            flash("Password must be atleast 3 characters.", "registration")
            is_valid = False

        if(re.search('[0-9]', user['password']) == None):
            flash("Password requires at least one digit", "registration")
            is_valid = False

        if(re.search('[A-Z]', user['password']) == None):
            flash("Password requires at least one uppercase", "registration")
            is_valid = False
        
        if (user['password'] != user['confirm_password']):
            flash("Passwords do not match", "registration")
        
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True

        if len(user['email']) < 3:
            flash("Email must be atleast 3 characters.", "login")
            is_valid = False
        
        if len(user['password']) < 3:
            flash("Password must be atleast 3 characters.", "login")
            is_valid = False
        return is_valid

    @classmethod
    def check_db(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL(DB).query_db(query, data)

        return results

    @classmethod
    def get_user_with_id(cls, data):
        
        query = """SELECT * FROM users 
        
            WHERE id = %(user_id)s
        """
        
        result = connectToMySQL(DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def read_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return None

        return User(results[0])