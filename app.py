from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Создание базы данных и таблиц
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Таблица для отзывов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tour TEXT,
            rating INTEGER NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    # Таблица для сообщений из контактов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            message TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# ===== Функции для отзывов =====
def get_reviews():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, tour, rating, text, date FROM reviews ORDER BY id DESC')
    reviews = cursor.fetchall()
    conn.close()
    
    reviews_list = []
    for review in reviews:
        reviews_list.append({
            'name': review[0],
            'tour': review[1],
            'rating': review[2],
            'text': review[3],
            'date': review[4]
        })
    return reviews_list

def save_review(name, tour, rating, text):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%d %B %Y')
    cursor.execute('''
        INSERT INTO reviews (name, tour, rating, text, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, tour, rating, text, date))
    conn.commit()
    conn.close()

# ===== Функции для контактов =====
def save_contact(name, email, phone, message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%d %B %Y %H:%M')
    cursor.execute('''
        INSERT INTO contacts (name, email, phone, message, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, message, date))
    conn.commit()
    conn.close()

def get_contacts():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, phone, message, date FROM contacts ORDER BY id DESC')
    contacts = cursor.fetchall()
    conn.close()
    
    contacts_list = []
    for contact in contacts:
        contacts_list.append({
            'name': contact[0],
            'email': contact[1],
            'phone': contact[2],
            'message': contact[3],
            'date': contact[4]
        })
    return contacts_list

# ===== API для отзывов =====
@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    reviews = get_reviews()
    return jsonify(reviews)

@app.route('/api/reviews', methods=['POST'])
def api_add_review():
    data = request.get_json()
    name = data.get('name')
    tour = data.get('tour', '')
    rating = data.get('rating')
    text = data.get('text')
    
    if not name or not text or not rating:
        return jsonify({'error': 'Заполните все поля'}), 400
    
    save_review(name, tour, rating, text)
    return jsonify({'success': True})

# ===== API для контактов =====
@app.route('/api/contact', methods=['POST'])
def api_send_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone', '')
    message = data.get('message')
    
    if not name or not email or not message:
        return jsonify({'error': 'Заполните обязательные поля (имя, email, сообщение)'}), 400
    
    save_contact(name, email, phone, message)
    return jsonify({'success': True, 'message': 'Сообщение отправлено! Мы свяжемся с вами.'})

# ===== Страницы =====
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/destinations')
def destinations():
    return render_template('destinations.html')

@app.route('/tours')
def tours():
    return render_template('tours.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)