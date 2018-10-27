from forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from server import app
from flask_login import current_user, login_user
from models import User
from flask_login import logout_user
from flask_login import login_required
from server import db
from logic import *
from datetime import datetime
from forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, preferences='')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html')

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='Profile', user=user)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response = ''
    response, intent, suggestions = get_bot_response(message)
    print(suggestions)
    if intent=='goodbye' and suggestions:
        print(current_user.preferences)
        print(current_user.username)
        # pref = current_user.preferences
        # pref += suggestions + ','
        # db.session.query().filter(User.username == current_user.username).update({"preferences": pref})
        # db.session.commit()
        current_user.preferences += suggestions[0] + ', '
        db.session.commit()
    return jsonify({'message' : response, 'intent': intent})
