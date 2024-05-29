import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from functools import wraps
app = Flask(__name__)
app.secret_key = 'random key'

# 요청을 보내기 전에 유저가 로그인 되어있는지 확인하는 데코레이터용 함수
def login_check(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("username"):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_func


# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html', username = session.get('username'))


# 회원가입 페이지 및 회원가입 api
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        # TODO : 회원가입 기능 구현하기
        # db/users.txt 파일에 가입 정보 저장
        req_form = request.form
        username = req_form['username']
        password = req_form['password']
        # 아이디 중복 확인
        with open('db/users.txt', 'r') as f:
            for line in f:
                if username == line.split()[0]:
                    return render_template('signup.html', error="This ID is already in use.")
        #db 입력
        with open('db/users.txt', 'a') as f:
            f.write("{} {}\n".format(username, password))
        return redirect(url_for('login'))


# 로그인 페이지 및 로그인 api
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        # TODO : 로그인 기능 구현하기
        # db/users.txt 파일에 가입 정보 저장
        req_form = request.form
        username = req_form['username']
        password = req_form['password']
        
        with open('db/users.txt', 'r') as f:
            for line in f:
                signed_username, singed_password = line.split()
                if signed_username != username:
                    continue

                if(password == singed_password):
                    session['username'] = username
                    return redirect(url_for('index'))
                
                return render_template('login.html', error="incorrect password.")
        return render_template('login.html', error="User cannot be found. Please check your ID.")

        

# 로그아웃 api
@app.route('/logout', methods = ['GET'])
@login_check
def logout():
    session.pop('username')
    return redirect(url_for('index'))


# 글쓰기 페이지 및 글쓰기 api
@app.route('/comment', methods =['GET', 'POST'])
@login_check
def handle_comment():
    if request.method == 'GET':
        # TODO : 글 작성 페이지 반환하기
        # db/comments.txt 파일에서 작성된 글 정보 가져오기
        with open('db/comments.txt', 'r') as f:
            comments = []
            for line in f:
                user, content = line.strip().split(' ', 1)
                comments.append({'user': user, 'content': content})
            return render_template('comments.html', comments = comments)

    
    elif request.method == 'POST':
        # TODO : 글 작성 기능 구현하기
        # db/comments.txt 파일에 작성된 글 정보 저장
        req_body = request.get_json()
        content = req_body['content']
        with open('db/comments.txt', 'a') as f:
            f.write(f"{session.get('username')} {content}\n")
        
        with open('db/comments.txt', 'r') as f:
            comments = []
            for line in f:
                user, content = line.strip().split(' ', 1)
                comments.append({'user': user, 'content': content})
        return render_template('comments.html', comments=comments)


app.debug = True

if __name__ == '__main__':
    app.run()