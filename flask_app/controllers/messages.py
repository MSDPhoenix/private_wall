from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wall/')
def wall():
    if 'user_id' not in session:
        return redirect('/')
    data = { 
        'user_id' : session['user_id'] 
        }
    user = User(data)
    return render_template('wall.html',user=user)
