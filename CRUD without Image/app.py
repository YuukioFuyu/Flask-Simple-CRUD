from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk membuat tabel di crudbase
def create_table():
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crud (
            id INTEGER PRIMARY KEY,
            nama TEXT NOT NULL,
            umur INTEGER,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk memasukkan crud ke dalam tabel
def insert_crud(nama, umur, email):
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO crud (nama, umur, email) VALUES (?, ?, ?)', (nama, umur, email))
    conn.commit()
    conn.close()

# Fungsi untuk mendapatkan semua crud dari tabel
def get_all_crud():
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM crud')
    crud = cursor.fetchall()
    conn.close()
    return crud

# Fungsi untuk mendapatkan crud berdasarkan ID
def get_crud_by_id(id):
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM crud WHERE id = ?', (id,))
    crud = cursor.fetchone()
    conn.close()
    return crud

# Fungsi untuk mengupdate crud berdasarkan ID
def update_crud(id, nama, umur, email):
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE crud SET nama = ?, umur = ?, email = ? WHERE id = ?', (nama, umur, email, id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus crud berdasarkan ID
def delete_crud(id):
    conn = sqlite3.connect('crud.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM crud WHERE id = ?', (id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    crud = get_all_crud()
    return render_template('index.html', crud=crud)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        umur = int(request.form['umur'])
        email = request.form['email']
        insert_crud(nama, umur, email)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    crud = get_crud_by_id(id)
    if request.method == 'POST':
        nama = request.form['nama']
        umur = int(request.form['umur'])
        email = request.form['email']
        update_crud(id, nama, umur, email)
        return redirect(url_for('index'))
    return render_template('edit.html', crud=crud)

@app.route('/delete/<int:id>')
def delete(id):
    delete_crud(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
