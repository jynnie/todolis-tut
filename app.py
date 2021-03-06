from flask import Flask
from flask import render_template
from wtforms import Form, TextField, validators, StringField, SubmitField
from flask import session, flash, request, redirect, abort
from sqlalchemy.orm import sessionmaker
import os
from tabledef import *

app = Flask(__name__)
app.config.from_object(__name__)

engine = create_engine('sqlite:///tutorial.db', echo=True)

class UserForm(Form):
    username = StringField('Username', validators=[validators.required()])
    email = StringField('Email')
    password = TextField('Password', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf()) ])
        self.process(blankData)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    todos = []

    if session.get('logged_in'):
        Session = sessionmaker(bind=engine)
        s = Session()

        current_user = s.query(User).get(session['user_id'])

        if request.method == 'POST':
            new_todo = request.form['todo']

            if new_todo != '': #if not empty
                todo = Todo(content=new_todo, user=current_user)
                s.add(todo)
                s.commit()

        user_todos = current_user.todos.all()

        for todo in user_todos:
            todos.append([todo.id, todo.content])

    return render_template('index.html',
                            list=todos)

@app.route('/delete')
def delete():
    if session.get('logged_in'):
        Session = sessionmaker(bind=engine)
        s = Session()

        todo_id = int(request.args.get('id'))
        todo = s.query(Todo).get(todo_id)
        s.delete(todo)
        s.commit()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm(request.form)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if form.validate():
            Session = sessionmaker(bind=engine)
            s = Session()
            user = User(username, email, password)
            s.add(user)
            s.commit()

            flash('Hello ' + username + '! Thanks for registering')
        else:
            flash('Error: All fields of the form are required')

    return render_template('signup.html',
                            form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if form.validate():
            Session = sessionmaker(bind=engine)
            s = Session()
            query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]))
            result = query.first()

            if result:
                session['logged_in'] = True
                session['user_id'] = result.id
                session['username'] = username
                flash('Welcome back, ' + session.get('username') + '!')
            else:
                flash('Sorry, invalid credentials. Try again')
        else:
            flash('Error: All fields of the form are required')

    return render_template('login.html',
                            form=form)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = 0
    session['username'] = 'Guest'
    return redirect('/')

app.secret_key = os.urandom(12)
app.run(debug=True, port=5000)
