from flask import Flask, render_template, g, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = '/Users/saato/OneDrive/デスクトップ/Happy_Book/database.db'  # この部分は実際のデータベースファイルのパスに置き換えてください

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
def list_books():
    cur = get_db().cursor()
    cur.execute("SELECT image_path FROM books")
    books = cur.fetchall()
    print(books)
    return render_template('list.html', books=books)



@app.route('/scanner')
def barcode_scanner():
    return render_template('scanner.html')

# @app.route('/handle_barcode', methods=['POST'])
# def handle_barcode():
#     data = request.get_json()
#     barcode = data.get('barcode', None)

#     if barcode:
#         # ここでバーコードに関連する処理やデータベースの操作を行うことができます。
#         print(f"Received barcode: {barcode}")

#         # レスポンスメッセージをカスタマイズすることができます。
#         return jsonify({"message": f"Received barcode: {barcode}"})
#     else:
#         return jsonify({"message": "No barcode received."})


if __name__ == '__main__':
    app.run(debug=True)



