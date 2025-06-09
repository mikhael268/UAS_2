from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = '123'  # Session secret key

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cinezone'

mysql = MySQL(app)

pending_resets = {}

# ================= ROUTES =================

@app.route('/')
def halaman_depan():
    return render_template('halaman_depan.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Invalid input data"}), 400

    hashed_password = generate_password_hash(password)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "User registered successfully!"})
    except Exception as e:
        print("Insert error:", e)
        return jsonify({"message": "Failed to register user."}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (identifier, identifier))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('halaman_depan'))  # 🔁 REDIRECT FIXED
        else:
            flash("Username or password is incorrect", "error")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('halaman_depan'))


@app.route('/film/<judul>')
def halaman_film(judul):
    if 'user_id' not in session:
        return redirect(url_for('index'))  
    return render_template(f"{judul}.html")


@app.route('/forget_password')
def forget_password():
    return render_template('forgot_password.html')

@app.route('/store_reset_otp', methods=['POST'])
def store_reset_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    if email and otp:
        pending_resets[email] = otp
        return jsonify({"message": "OTP stored."})
    return jsonify({"message": "Invalid request"}), 400

@app.route('/verify_reset_otp', methods=['POST'])
def verify_reset_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if email in pending_resets and pending_resets[email] == otp:
        return jsonify({"valid": True})
    return jsonify({"valid": False})

@app.route('/reset_password_final', methods=['POST'])
def reset_password_final():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({"success": False, "message": "Missing data"})

    try:
        hashed_password = generate_password_hash(new_password)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (hashed_password, email)
        )
        mysql.connection.commit()
        cursor.close()
        pending_resets.pop(email, None)
        return jsonify({"success": True})
    except Exception as e:
        print("Password reset error:", e)
        return jsonify({"success": False, "message": "DB error"})


@app.route('/reset_form')
def reset_form():
    return render_template('reset_form.html')


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# Format harga rupiah
def format_rupiah(value):
    return "Rp.{:,.2f}".format(value).replace(",", "#").replace(".", ",").replace("#", ".")

app.jinja_env.filters['format_rupiah'] = format_rupiah


# ================= Halaman Film =================

@app.route('/seanman')
def seanman():
    return render_template('seanman_film.html')

@app.route('/chittato')
def chittato():
    return render_template('chitatto_film.html')

@app.route('/dracula')
def dracula():
    return render_template('dracula_film.html')

@app.route('/dreams')
def dreams():
    return render_template('dreams_film.html')


# ================= Booking =================

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    film = request.form.get('film')
    jadwal = request.form.get('jadwal')
    jumlah = int(request.form.get('jumlah'))
    harga = int(request.form.get('harga'))
    total = harga * jumlah

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO bookings (nama_film, jam_tayang, jumlah_kursi, total_harga) VALUES (%s, %s, %s, %s)",
        (film, jadwal, jumlah, total)
    )
    mysql.connection.commit()
    cursor.close()

    beli_lagi_url = f"/{film.lower()}"
    return render_template('success.html', film=film, jadwal=jadwal, jumlah=jumlah, harga=harga, total=total, beli_lagi_url=beli_lagi_url)


# ================= Run Server =================

if __name__ == '__main__':
    app.run(debug=True)
