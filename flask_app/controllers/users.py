from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register/',methods=['POST'])
def register():
    # how do I prevent users from entering localhost:5001/register/ in the search bar?
    if not User.validate(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        session['confirm_password'] = request.form['confirm_password']
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/wall/')
    
@app.route('/login/',methods=['POST'])
def login():
    # how do I prevent users from entering localhost:5001/login/ in the search bar?
    data = {
        'email' : request.form['email']
    }
    user = User.get_by_email(data)
    if not user or not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid email/password','login')
        session['email2'] = request.form['email']
        session['password2'] = request.form['password']
        return redirect('/')
    session.clear()
    session['user_id'] = user.id
    return redirect('/wall/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')
