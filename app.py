from flask import Flask, request, jsonify
from db_config import connect_db
from datetime import date

app = Flask(__name__)

# USER ROUTES

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added', 'user_id': user_id})

@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# MOOD ROUTES 

@app.route('/moods', methods=['POST'])
def add_mood():
    data = request.get_json()
    mood = data['mood']
    trigger_note = data['trigger_note']
    mood_date = data.get('date', str(date.today()))
    user_id = data['user_id']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (mood, trigger_note, date, user_id) VALUES (%s, %s, %s, %s)", 
                   (mood, trigger_note, mood_date, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Mood logged successfully'})

@app.route('/moods/<int:user_id>', methods=['GET'])
def get_moods(user_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM moods WHERE user_id = %s ORDER BY date DESC", (user_id,))
    moods = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(moods)

@app.route('/moods/<int:id>', methods=['PUT'])
def update_mood(id):
    data = request.get_json()
    mood = data['mood']
    trigger_note = data['trigger_note']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE moods SET mood=%s, trigger_note=%s WHERE id=%s", (mood, trigger_note, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Mood updated'})

@app.route('/moods/<int:id>', methods=['DELETE'])
def delete_mood(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM moods WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Mood deleted'})

#  STATS ROUTES 

@app.route('/moods/stats/summary/<int:user_id>', methods=['GET'])
def mood_summary(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mood, COUNT(*) FROM moods WHERE user_id=%s GROUP BY mood", (user_id,))
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({row[0]: row[1] for row in stats})

@app.route('/moods/recent/<int:user_id>', methods=['GET'])
def recent_moods(user_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM moods WHERE user_id = %s ORDER BY date DESC LIMIT 5", (user_id,))
    recent = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(recent)

if __name__ == '__main__':
    app.run(debug=True)
