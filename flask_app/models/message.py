from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user
import datetime
import humanize
db = 'private_wall'

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.receiver = None
        self.how_long_ago = None

    @classmethod
    def get_messages_received(cls,data):
        query = '''
                SELECT * FROM messages WHERE receiver_id = %(user_id)s;
                '''
        result = connectToMySQL(db).query_db(query,data)
        messages = []
        for row in result:
            message = cls(row)
            message_data = {
                'user_id' : message.sender_id
            }
            message.sender = user.User.get_by_id(message_data)
            message.how_long_ago = humanize.naturaltime(message.created_at)
            messages.append(message) 
        return messages

    @classmethod
    def get_messages_sent(cls,data):
        query = '''
                SELECT * FROM messages WHERE sender_id = %(user_id)s;
                '''
        result = connectToMySQL(db).query_db(query,data)
        messages = []
        for row in result:
            message = cls(row)
            message.how_long_ago = humanize.naturaltime(message.created_at)
            messages.append(message) 
        return messages

    @classmethod
    def save(cls,data):
        query = '''
                INSERT INTO messages (content,sender_id,receiver_id)
                VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);
                '''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = '''
                DELETE FROM messages WHERE id = %(message_id)s;
                '''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = '''
                SELECT * FROM messages WHERE id = %(message_id)s;
                '''
        result = connectToMySQL(db).query_db(query,data)
        message = cls(result[0])
        return message


