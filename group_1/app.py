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
    
@app.route('/login', methods=['GET', 'POST'] )
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from tbl_user where username = '{username}'")
        user = cur.fetchone()
        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO tbl_user (username, password) VALUES ('{username}', '{password}')")
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


