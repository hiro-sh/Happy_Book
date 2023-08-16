from flask import Flask, render_template, g, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'  # この部分は実際のデータベースファイルのパスに置き換えてください

app.config['SECRET_KEY'] = 'your_secret_key_here'

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        
        if user and user[0] == password:
            session['logged_in'] = True
            session['username'] = username
            cur.execute("SELECT id FROM users WHERE username=?", (username,))
            user_id = cur.fetchone()
            session['user_id'] = user_id[0]
            return redirect('/list')

    return render_template('login.html')

#　ログアウト
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/login')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/list')
def list():
    user_id = session['user_id']
    cur = get_db().cursor()
    cur.execute("SELECT id, image_path FROM books WHERE user_id=?", (user_id,))
    books = cur.fetchall()
    print(books)
    return render_template('list.html', books=books)


@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    return render_template('scanner.html')

@app.route('/handle_barcode', methods=['POST'])
def handle_barcode():
    data = request.get_json()
    barcode = data.get('barcode', None)

    if barcode and barcode.startswith('97') and len(barcode) == 13:
        return jsonify({"redirect": url_for('barcode_add', barcode=barcode)})

    # 条件に一致しない場合、特にエラーメッセージなどを返さずに空のレスポンスを返す
    return jsonify({})

@app.route('/barcode_add/<barcode>')
def barcode_add(barcode):
    return render_template('barcode_add.html', barcode=barcode)

# この本を本だなに入れるが押された時
@app.route('/add_book', methods=['POST'])
def add_book():
    barcode = request.form.get('barcode')
    user_id = session['user_id']

    db = get_db()
    cur = db.cursor()

    cur.execute("INSERT INTO books (image_path, user_id) VALUES (?, ?)", (barcode, user_id))

    db.commit()
    return redirect('/list')


# やめるが押されたらリストに戻る
@app.route('/cancel_add', methods=['POST'])
def cancel_add():
    return redirect('/list')

@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form.get('book_id')
    
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    db.commit()

    return redirect('/list')

@app.route("/mypage")
def mypage_get():
    return render_template("mypage.html")

@app.route("/te_login")
def te_login_get():
    return render_template("te_login.html")

@app.route("/st_list")
def st_list_get():
    return render_template("st_list.html")

@app.route("/booklist")
def booklist_get():
    return render_template("booklist.html")



if __name__ == '__main__':
    app.run(debug=True)
