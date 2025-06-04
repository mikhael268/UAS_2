from flask import Flask
from models import db

app = Flask(__name__)

# Koneksi ke database MySQL (tanpa password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/uas_website'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Halo Flask + MySQL!"

if __name__ == '__main__':
    app.run(debug=True)
