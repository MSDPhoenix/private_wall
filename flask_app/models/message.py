from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user
db = 'private_wall'

class Message:
    def __init__(self,data):
        self.id = data['xxx']
        self.content = data['xxx']
        self.sender_id = data['xxx']
        self.receiver_id = data['xxx']
        self.created_at = data['xxx']
        self.updated_at = data['xxx']
        self.sender = None
        self.receiver = None

