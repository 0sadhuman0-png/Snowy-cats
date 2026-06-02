from flask import Flask, render_template, request, jsonify
from whitenoise import WhiteNoise
import sqlite3
import os

app = Flask(__name__)

# Настройка WhiteNoise (чтобы видел картинки в папке static)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

# Функция для создания базы данных и таблицы
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE likes_table (image_id TEXT PRIMARY KEY, likes INTEGER)''')
        conn.commit()
        conn.close()

init_db()

# Функция для получения лайков одного конкретного пина
def get_likes_from_db(image_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT likes FROM likes_table WHERE image_id = ?", (image_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0


@app.route('/')
def home():
    # Список динамических пинов для первой вкладки (Snow Cat)
    # Замени или дополни этот список своими реальными картинками
    my_pins = [
        {"id": "1", "title": "Snow Cat (Black Edition)", "image": "Snow_cat_blackl.jpg"},
        {"id": "2", "title": "Snow Cat (White Edition)", "image": "Snow_cat_white.jpg"},
    ]
    
    # Добавляем актуальные лайки из базы данных в каждый пин перед отправкой на страницу
    for pin in my_pins:
        pin["likes"] = get_likes_from_db(pin["id"])
        
    return render_template('index.html', pins=my_pins)


# 1. НОВЫЙ РОУТ: Отдает ВСЕ лайки из базы в формате JSON.
# Это нужно, чтобы вкладки 2 и 3 автоматически подгружали лайки при заходе на сайт!
@app.route('/api/get_likes', methods=['GET'])
def get_all_likes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT image_id, likes FROM likes_table")
    rows = cursor.fetchall()
    conn.close()
    
    # Превращаем результат в красивый словарь: {"1": 5, "101": 12, "201": 1}
    likes_dict = {row[0]: row[1] for row in rows}
    return jsonify(likes_dict)


# 2. ИСПРАВЛЕННЫЙ РОУТ: Обрабатывает нажатие на сердечко (лайк / анлайк)
@app.route('/api/like', methods=['POST'])
def handle_like():
    data = request.get_json()
    image_id = data.get('id')
    action = data.get('action') # Получаем 'like' или 'unlike'
    
    if not image_id:
        return jsonify({'error': 'No ID provided'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Ищем, есть ли уже этот ID в базе данных
    cursor.execute("SELECT likes FROM likes_table WHERE image_id = ?", (image_id,))
    row = cursor.fetchone()
    
    if not row:
        # Если записи еще нет в базе, создаем ее
        initial_likes = 1 if action == 'like' else 0
        cursor.execute("INSERT INTO likes_table (image_id, likes) VALUES (?, ?)", (image_id, initial_likes))
        new_count = initial_likes
    else:
        # Если запись есть, увеличиваем или уменьшаем счетчик
        current_likes = row[0]
        if action == 'like':
            new_count = current_likes + 1
        else:
            new_count = max(0, current_likes - 1) # Чтобы лайки не ушли в минус
            
        cursor.execute("UPDATE likes_table SET likes = ? WHERE image_id = ?", (new_count, image_id))
    
    conn.commit()
    conn.close()
    
    # Возвращаем обновленное количество лайков обратно во фронтенд
    return jsonify({'likes': new_count})


if __name__ == '__main__':
    app.run(debug=True)