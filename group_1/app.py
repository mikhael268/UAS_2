from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi database MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Cinezone'

mysql = MySQL(app)

# Halaman utama
@app.route('/')
def index():
    return render_template('halaman_depan.html')

# Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash password sebelum disimpan
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                       (username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signUp.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next_page = request.form.get('next')  # Ambil dari input hidden
        identifier = request.form['identifier']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (identifier, identifier))
        account = cursor.fetchone()

        if account and bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8')):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            if next_page:
                # Pastikan tidak dobel .html
                if not next_page.endswith('.html'):
                    next_page += '.html'
                return redirect(f"/{next_page}")
            else:
                return redirect(url_for('index'))
        else:
            return render_template('login.html', msg='Invalid credentials', next=next_page)

    # GET: Ambil ?next= dari URL
    return render_template('login.html', next=request.args.get('next'))

# Halaman detail film SeanMan
@app.route('/SeanMan.html')
def seanman():
    return render_template('SeanMan.html')

# Halaman reset password (OTP)
@app.route('/reset-password')
def reset_password():
    return render_template('index.html')

# Jalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
