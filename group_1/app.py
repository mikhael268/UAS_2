from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Cinezone'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('halaman_depan.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signUp.html')

@app.route('/start-verification', methods=['POST'])
def start_verification():
    session['username'] = request.form['username']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    return redirect(url_for('verify_email_post'))

@app.route('/verify-email')
def verify_email_post():
    return render_template('verify_email.html', email=session.get('email'))

@app.route('/finish-verification', methods=['POST'])
def finish_verification():
    username = session.get('username')
    email = session.get('email')
    password = session.get('password')
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_pw))
    mysql.connection.commit()
    cursor.close()

    session.clear()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "Halaman login"

if __name__ == "__main__":
    app.run(debug=True)
