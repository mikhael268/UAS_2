from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysql import MySQL

app = Flask('__name__')
app.secret_key = '123'

#mysql config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bioskop_user'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('halaman_depan.html', username=session['username'])
    else:
        return render_template('halaman_depan.html')
