import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pymysql
app = Flask(__name__)
db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="9800",
    db="flask",
    charset="utf8"
)

cursor = db.cursor()

sql = '''
    select * from
'''

@app.route('/')
def home():
    try:
        with db.cursor() as cursor:
            sql = 'select * from users'
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
            return 'success'
    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)