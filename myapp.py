import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)


@app.route('/user/<username>')
def show_user(username):
	return username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id
    
@app.route('/post',  methods=['GET', 'POST'])
def handle_post():
     if request.method == 'GET':
          req_args = request.args
          keyword = req_args.get('keyword', default='none')
          return 'post list with keyword %s' % keyword
     
     elif request.method == 'POST':
          req_body = request.get_json()
          title = req_body['title']
          return 'post %s saved' % title
     x
@app.route('/hello_user')
def hello_user():
    username = request.args.get('username')
    print(username)
    return render_template('index.html', name = username)

app.secret_key = 'random key'

@app.route('/')
def index():
     if "username" in session: 
        return '%s is administrator' % session['username']
     else:
        return 'you are not administrator'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        req_form = request.form
        username = req_form['username']
        password = req_form['password']
        
        if(username=='cnu' and password=='r912'):
            session['username'] = username
        
        return redirect(url_for('index'))
    

app.debug = True

if __name__ == '__main__':
    app.run(debug=True)