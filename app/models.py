from app import db
from app import app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class AbstractBaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(54), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name


class Bucketlist(AbstractBaseModel):
    __tablename__ = 'bucketlists'
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', cascade="all,delete", backref='bucketlist',
                            lazy='select')

    def __init__(self, name, created_by):
        self.created_by = created_by
        super(Bucketlist, self).__init__(name)

    def __repr__(self):
        return '<Bucketlist %r>' % self.name


class Item(AbstractBaseModel):
    __tablename__ = 'bucketitems'
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, bucketlist_id, description=''):
        self.bucketlist_id = bucketlist_id
        self.description = description
        super(Item, self).__init__(name)

    def __repr__(self):
        return '<Item %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship(
        'Bucketlist', cascade="all,delete", backref='bucketlist', lazy='dynamic')

    @staticmethod
    def hash_password(password):
        password_hash = pwd_context.encrypt(password)
        return password_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self, expiration=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

db.create_all()
