import flask
from flask import Flask
import flask_login



class User(flask_login.UserMixin):
    pass




# Our mock database.
users = {'georgeha@gmail.com': {'password': 'hello'}}