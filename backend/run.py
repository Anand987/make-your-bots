from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user'
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return "cool"
    

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username or password'

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name':request.form['username'], 'password': hashpass})
            session['username'] =  request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return "login successful"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)