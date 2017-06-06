from flask import Flask
from flask import render_template
from wtforms import Form, TextField, validators, StringField, SubmitField
from flask import session, flash, request, redirect, abort
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
app.config.from_object(__name__)

class UserForm(Form):
    username = StringField('Username', validators=[validators.required()])
    email = StringField('Email')
    password = TextField('Password', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf()) ])
        self.process(blankData)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

app.secret_key = os.urandom(12)
app.run(debug=True, port=5000)
