from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = 'collab_editor.db'

# Initialize database with a single document
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, content TEXT)')
    c.execute("INSERT OR IGNORE INTO documents (id, content) VALUES (1, '')")
    conn.commit()
    conn.close()

@app.route('/get', methods=['GET'])
def get_document():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT content FROM documents WHERE id=1')
    content = c.fetchone()[0]
    conn.close()
    return jsonify({'content': content})

@app.route('/update', methods=['POST'])
def update_document():
    data = request.get_json()
    content = data.get('content', '')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE documents SET content=? WHERE id=1", (content,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
