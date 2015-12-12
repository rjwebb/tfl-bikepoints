from app import db


class BikePoint(db.Model):
    __tablename__ = 'bikepoints'

    id = db.Column(db.Integer, primary_key=True)
    bp_id = db.Column(db.String(), primary_key=True)

    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    nbDocks = db.Column(db.Integer())
    nbBikes = db.Column(db.Integer())
    nbEmptyDocks = db.Column(db.Integer())

    def __init__(self, bp_id, lat, lon, nbDocks, nbBikes, nbEmptyDocks):
        self.bp_id = bp_id

        self.lat = lat
        self.lon = lon

        self.nbDocks = nbDocks
        self.nbBikes = nbBikes
        self.nbEmptyDocks = nbEmptyDocks

    def __repr__(self):
        return '<bp_id {}>'.format(self.bp_id)

