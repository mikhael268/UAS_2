from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os
from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')


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

if __name__ == '__main__':
    app.run(debug=True)


