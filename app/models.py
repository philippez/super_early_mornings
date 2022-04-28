from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy.orm import Session, relationship



followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    assets = db.relationship('Asset', backref='originator', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='transactor', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    asset_name = db.Column(db.String(64), index=True, unique=True)
    asset_currency = db.Column(db.String(10))
    asset_desc = db.Column(db.String(200))
    asset_region = db.Column(db.String(64))
    asset_type = db.Column(db.String(64))
    super_theme = db.Column(db.String(64))
    micro_theme = db.Column(db.String(64))
    bloomberg_ticker = db.Column(db.String(64))
    sec_ref = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction', backref='transactions_asset', lazy='dynamic')
    asset_prices = db.relationship('Asset_Prices', backref='priced_asset', lazy='dynamic')

    def __repr__(self):
        return '<Asset {}>'.format(self.asset_name)

class Super_Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    super_theme_name = db.Column(db.String(64), index=True, unique=True)
    super_theme_desc = db.Column(db.String(200))

    def __repr__(self):
        return '<Super_Theme {}>'.format(self.super_theme_name)

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opinion_name = db.Column(db.String(64))
    opinion_factor = db.Column(db.Integer)
    opinion_desc = db.Column(db.String (200))

    def __repr__(self):
        return '<Opinion {}>'.format(self.opinion_name)

class Tx_Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tx_type_name = db.Column(db.String(64))
    tx_type_desc = db.Column(db.String(200))

    def __repr__(self):
        return '<Tx_Type {}>'.format(self.tx_type_name)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(64))
    platform_desc = db.Column(db.String(64))
    transactions = db.relationship('Transaction', backref='transactions_platform', lazy='dynamic')

    def __repr__(self):
        return '<Platform {}>'.format(self.platform_name)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    type = db.Column(db.String(64))
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Asset_Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    price = db.Column(db.Integer)

