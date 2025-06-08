from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'cinezone-secret-key'  # Ganti untuk production

# Konfigurasi koneksi ke database MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Kosongkan jika tanpa password
app.config['MYSQL_DB'] = 'cinezone'

# Inisialisasi koneksi
mysql = MySQL(app)

# Halaman utama (halaman depan)
@app.route('/')
def halaman_depan():
    return render_template('halaman_depan.html')

# Halaman sign up (index.html)
@app.route('/index')
def index():
    return render_template('index.html')

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s OR email = %s",
            (identifier, identifier)
        )
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            print("✅ Login sukses untuk user:", user['username'])

            # Arahkan kembali ke halaman yang diminta sebelumnya jika ada
            next_page = request.form.get('next')
            return redirect(next_page or url_for('halaman_depan'))
        else:
            print("❌ Login gagal.")
            return "Login failed. Please check your credentials.", 401
    else:
        return render_template('login.html', next=request.args.get('next', '/'))

# Endpoint untuk menerima data user dari JavaScript (setelah OTP sukses)
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    print("🔵 Data dari frontend:", data)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        print("❌ Username/email/password kosong!")
        return jsonify({"message": "Invalid input data"}), 400

    hashed_password = generate_password_hash(password)
    print("🟢 Hashed password:", hashed_password)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        mysql.connection.commit()
        cursor.close()
        print("✅ User berhasil didaftarkan.")
        return jsonify({"message": "User registered successfully!"})
    except Exception as e:
        print("❌ ERROR saat insert ke DB:", e)
        return jsonify({"message": "Failed to register user."}), 500

# Halaman reset password
@app.route('/reset_password')
def reset_password():
    return "<h3>Coming Soon: Reset Password Page</h3>"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('halaman_depan'))

# ✅ Halaman film (proteksi: harus login)
@app.route('/film/<judul>')
def halaman_film(judul):
    if 'user_id' not in session:
        print("🔒 Belum login, redirect ke login.")
        return redirect(url_for('login', next=url_for('halaman_film', judul=judul)))

    # Misalnya halaman: SeanMan.html, dracula.html, dll.
    try:
        return render_template(f"{judul}.html")
    except:
        return "<h3>❌ Halaman film tidak ditemukan.</h3>", 404

if __name__ == '__main__':
    app.run(debug=True)
