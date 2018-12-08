from flask import render_template, url_for, flash, redirect, request, jsonify
from musyk import app, db, bcrypt
from musyk.forms import RegistrationForm, LoginForm
from musyk.models import User, Track
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
    return render_template('toptracks.html', countries=allcountries, toptracks=toptracks[0]['tracks']['track'], error=error, title='Top Tracks')


# @app.route("/playlists")
# @login_required
# def playlists():
#     if current_user and current_user.is_authenticated:
#         tracks = Track.query.filter_by(user_id=current_user.id)
#         return render_template('playlists.html', countries=allcountries, title='My Playlists', tracks=tracks)
#     return redirect(url_for('home'))


@app.route('/country', methods=['POST'])
def country():
    userId = request.form['user_id']
    country = request.form['country']
    user = User.query.filter_by(id=userId).first()
    print(userId + country)
    if user:
        user.country = country
        db.session.commit()
    return jsonify({'success' : 'Yay, your region is now changed'})

@app.route('/playlists', methods=['POST', 'GET'])
def playlists():
    if current_user and current_user.is_authenticated:
        if request.method == 'POST':
            trackId = request.form['trackId']
            existing_track = Track.query.filter_by(id=trackId).first()
            if existing_track:
                db.session.delete(existing_track)
                db.session.commit()
                updatedTracks = Track.query.filter_by(user_id=current_user.id)
                return render_template('updatedPlaylist.html', tracks=updatedTracks)
            else:
                jsonify({'error' : 'Oops! Issue getting rid of this track from your playlist'})
        else:
            tracks = Track.query.filter_by(user_id=current_user.id).all()
            return render_template('playlists.html', countries=allcountries, title='My Playlists', tracks=tracks)
    return jsonify({'error' : 'Oops! Error getting your playlists'})

@app.route("/add_to_playlist", methods=['POST'])
def addtoplaylist():
    user_id = request.form['user_id']
    track_name = request.form['name']
    track_artist = request.form['artist']
    print("user...#####")
    print(user_id)
    if user_id == None or user_id == "":
        return jsonify({'error' : 'Please Sign In to add tracks to your playlists'})
    existing_track = Track.query.filter_by(name=track_name, artist=track_artist, user_id=user_id).first()
    if existing_track:
        return jsonify({'error' : 'Track already in your playlist'})
    else:
        track = Track(name=track_name, artist=track_artist, user_id=user_id)
        db.session.add(track)
        db.session.commit()
    return jsonify({'success' : 'Track added to your playlist'})

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
    return render_template('account.html', title='Account', countries=allcountries)
