from database import db

class Students(db.Model):
    __tablename__ = 'Students'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    identityNumber = db.Column(db.String(9), nullable=False, unique=True)
    classN = db.Column('class', db.String(10), nullable=False)

class Teachers(db.Model):
    __tablename__ = 'Teachers'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    identityNumber = db.Column(db.String(9), nullable=False, unique=True)
    classN = db.Column('class', db.String(10), nullable=False)

class Locations(db.Model):
    __tablename__ = 'Locations'

    id = db.Column(db.Integer, primary_key=True)
    studentIdentity = db.Column(db.String(9), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    timeS = db.Column(db.DateTime, nullable=False)