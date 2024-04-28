# sqlalchemy
# базы данных нужны для хранения информации 
# существует много видов баз данных, например MySQL, PostgreSQL, SQLite, Oracle, etc.

# План работы над сервисом регистрации
# 1. Создание структуры веб-сервиса
# 2. Создание html-шаблонов для веб-сервиса и стилей
# 3. Создание базы данных
# 4. Создание механизма авторизации

# ORM - Object Relational Mapper

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static') # веб-сервис
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
database = SQLAlchemy(app) # база данных

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True) # порядковый номер пользователя
    email = database.Column(database.String(50), unique=True) # электронный адрес пользователя
    password = database.Column(database.String(50), nullable=True) # пароль пользователя
    date = database.Column(database.DateTime, default=datetime.utcnow) # дата регистрации

    def __repr__(self):
        return f"users {self.id}"

class Profiles(database.Model):
    id = database.Column(database.Integer, primary_key=True) # порядковый номер пользователя
    name = database.Column(database.String(100), nullable=True) # имя пользователя
    old = database.Column(database.Integer) # возраст пользователя
    city = database.Column(database.String(100)) # город пользователя

    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def __repr__(self):
        return f"profiles {self.id}"

with app.app_context():
    database.create_all() # создание структуры базы данных пользователей и профилей

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        try:
            user = Users(email=request.form['email'], password=request.form['password'])
            database.session.add(user)
            database.session.flush()

            profile = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id=user.id)
            database.session.add(profile)
            database.session.commit()
        except:
            database.session.rollback()
            print('Ошибка бд')

    return render_template('index.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            return redirect('https://youtu.be/qnSVF7EEjSQ?si=x5hOpDslSR0EI2HZ')
        else: 
            return render_template('login.html', result='ну прям совсем плохо братан')

    return render_template('login.html', result='ты не вошел братан')

if __name__ == '__main__':
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/login', 'login', login)
    app.run(debug=True, port=8080)