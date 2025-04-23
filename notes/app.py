from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель заметки
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Note {self.title}>'

with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes, show_favorites=False) # Добавляем show_favorites

# Избранные заметки
@app.route('/favorite')
def favorites():
    notes = Note.query.filter_by(is_favorite=True).all()
    return render_template('index.html', notes=notes, show_favorites=True) # Добавляем show_favorites

# Просмотр заметки
@app.route('/note/<int:id>')
def note(id):
    note = Note.query.get_or_404(id)
    return render_template('note.html', note=note)

# Создание заметки
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_note = Note(title=title, content=content)

        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html')

# Редактирование заметки
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('note', id=note.id))

    return render_template('create.html', note=note)

# Удаление заметки
@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

# Добавление/удаление из избранного
@app.route('/favorite/<int:id>')
def favorite(id):
    note = Note.query.get_or_404(id)
    note.is_favorite = not note.is_favorite
    db.session.commit()
    return redirect(request.referrer or url_for('index')) # Возвращаемся на предыдущую страницу

# Поиск заметок
@app.route('/search')
def search():
    query = request.args.get('query')
    notes = Note.query.filter(Note.title.contains(query)).all()
    return render_template('index.html', notes=notes, show_favorites=False)

if __name__ == '__main__':
    app.run(debug=True)