from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
import socket
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wall/')
def wall():
    if not 'user_id' in session:
        return redirect('/')
    data = { 
        'user_id' : session['user_id'] 
        }
    user = User.get_by_id(data)
    other_users = User.get_other_users(data)
    messages_received = Message.get_messages_received(data) 
    return render_template('wall.html',user=user,other_users=other_users,messages_received=messages_received)

@app.route('/send_message/',methods=['POST'])
def send_message():
    if not 'user_id' in session:
        return redirect('/')
    if len(request.form['content']) < 1:
        flash('Message cannot be blank','message')
        return redirect('/wall/')
    if len(request.form['content']) < 5:
        flash('Message must be at least 5 characters long','message')
        return redirect('/wall/')
    Message.save(request.form)
    return redirect('/wall/')

@app.route('/destroy/<int:message_id>/')
def destroy(message_id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'message_id' : message_id
    }
    message = Message.get_by_id(data)
    if message.receiver_id != session['user_id']:
        return redirect(f'/danger/{message_id}')
    Message.destroy(data)
    return redirect('/wall/')


@app.route('/danger/<int:message_id>/')
def danger(message_id):
    if 'been_warned' not in session:
        session['been_warned']=True
        print('been_warned')
    else:
        print("Z")
        print("logging out")
        session.clear()
        flash('You have been logged out','login')
        return redirect('/')
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return render_template('danger.html', message_id=message_id,ip_address=ip_address)
