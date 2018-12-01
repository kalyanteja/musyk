from datetime import datetime
from musyk import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    tracks = db.relationship('Track', backref='listener', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    album = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Track('{self.title}', '{self.album}', '{self.artist}', '{self.date_posted}')"


def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()