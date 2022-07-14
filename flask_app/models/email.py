from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Email:
    schema = 'email_schema'
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def save(cls, data):
        query = "INSERT into emails (email) VALUES (%(email)s);"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM emails WHERE email = %(email)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results)< 1:
            return False
        row = results[0]
        emails = cls(row)
        return emails

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails "
        results = connectToMySQL(cls.schema).query_db(query)
        email = []
        for row in results:
            email.append( cls(row) )
        return email

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query,data)

    @staticmethod
    def is_valid(email):
        is_valid = True
        email_in_db = Email.get_email(email)
        if email_in_db:
            flash("Email is already been taken")
            is_valid =  False
        if len(email['email']) < 3:
            is_valid = False
            flash("email must be at least 3 characters.")
        if not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid