from flask import Flask, flash, redirect, render_template, request, url_for, session
from config import Config
import os, pdfkit

class Portal:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = '!@#$123456&*()'
        self.con = Config()
        self.routes()
       
    def routes(self):
        @self.app.route('/testdb')
        def test_db():
            try:
                if self.con.mysql is not None:
                    return 'Database connection successful!'
            except Exception as e:
                return f"Database connection failed: {e}"
           
        # mobil
        @self.app.route('/data-mobil')
        def readMobil():
            cur = self.con.mysql.cursor()
            cur.execute('SELECT * FROM mobil')
            data = cur.fetchall()
            cur.close()
            return render_template('readMobil.html', data=data)
       
        @self.app.route('/insert-mobil/')
        def createMobil():
            return render_template('insertMobil.html')

        @self.app.route('/insert-mobil/process', methods=['POST'])
        def createMobilProcess():
            if request.method == 'POST':
                id_mobil = request.form['id_mobil']
                nama = request.form['nama']
                kategori = request.form['kategori']
                spesifikasi = request.form['spesifikasi']
                harga = request.form['harga']
                tahun = request.form['tahun']
                cur = self.con.mysql.cursor()
                try:
                    cur.execute('INSERT INTO mobil (id_mobil, nama, kategori, spesifikasi, harga, tahun) VALUES (%s, %s, %s, %s, %s, %s)',
                                (id_mobil, nama, kategori, spesifikasi, harga, tahun))
                    self.con.mysql.commit()
                    flash('Mobil created successfully!', 'success')
                except Exception as e:
                    flash('Mobil creation failed: ' + str(e), 'error')
                cur.close()
                return redirect(url_for('readMobil'))
               
        @self.app.route('/update-mobil/<string:id_mobil>')
        def updateMobil(id_mobil):
            cur = self.con.mysql.cursor()
            cur.execute('SELECT * FROM mobil WHERE id_mobil = %s', (id_mobil,))
            data = cur.fetchone()
            cur.close()
            return render_template('updateMobil.html', data=data)
       
        @self.app.route('/update-mobil/process', methods=['POST'])
        def updateMobilProcess():
            if request.method == 'POST':
                id_mobil = request.form['id_mobil']
                nama = request.form['nama']
                kategori = request.form['kategori']
                spesifikasi = request.form['spesifikasi']
                harga = request.form['harga']
                tahun = request.form['tahun']
                cur = self.con.mysql.cursor()
                try:
                    cur.execute('UPDATE mobil SET nama = %s, kategori = %s, spesifikasi = %s, harga = %s, tahun = %s WHERE id_mobil = %s',
                                (nama, kategori, spesifikasi, harga, tahun, id_mobil))
                    self.con.mysql.commit()
                    flash('Mobil updated successfully!', 'success')
                except Exception as e:
                    flash('Mobil update failed: ' + str(e), 'error')
                cur.close()
                return redirect(url_for('readMobil'))
           
        @self.app.route('/delete-mobil/<string:id_mobil>')
        def deleteMobil(id_mobil):
            cur = self.con.mysql.cursor()
            try:
                cur.execute('DELETE FROM mobil WHERE id_mobil = %s', (id_mobil,))
                self.con.mysql.commit()
                flash('Mobil deleted successfully!', category='success')
            except Exception as e:
                flash('Mobil delete failed: ' + str(e), category='error')
            cur.close()
            return redirect(url_for('readMobil'))
        # end mobil
                       
    def run(self):
        self.app.run(debug=True)
           
if __name__ == '__main__':
    portal = Portal()
    portal.run()
