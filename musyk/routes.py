from flask import render_template, url_for, flash, redirect, request
from musyk import app, db, bcrypt
from musyk.forms import RegistrationForm, LoginForm
from musyk.models import User
from flask_login import login_user, current_user, logout_user, login_required
from musyk.lastfm import top_tracks
from musyk.countries import all_countries

allcountries = [{ 'name': 'Worldwide' }]
for country in all_countries():
    allcountries.append(country)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', countries=allcountries)


@app.route("/toptracks", methods=['GET', 'POST'])
def toptracks():
    toptracks = []
    error = None
    country = None
    if current_user and current_user.is_authenticated:
        country = current_user.country
        if country == "Worldwide":
            country = None
    resp = top_tracks(country)
    if resp:
        toptracks.append(resp)
    if len(toptracks) != 2:
        error = 'Bad Response from Last.FM API'
    return render_template('toptracks.html',countries=allcountries, toptracks=toptracks[0]['tracks']['track'], error=error, title='Top Tracks')


@app.route("/playlists")
def playlists():
    return render_template('playlists.html', countries=allcountries, title='My Playlists')


@app.route('/country/<countryName>')
def country(countryName):
    # todo, can't use split like this
    userName = countryName.split(',')[1]
    country = countryName.split(',')[0]
    user = User.query.filter_by(username=userName).first()
    if user:
        user.country = country
        db.session.commit()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# @app.route("/addtoplaylist", methods=['GET', 'POST'])
# def addtoplaylist():


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
