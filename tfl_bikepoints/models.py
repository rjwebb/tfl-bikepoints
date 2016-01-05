import datetime
from tfl_bikepoints import db

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_edited = db.Column(db.DateTime())

    def __init__(self, last_edited):
        self.last_edited = last_edited

    def __repr__(self):
        return '<last_edited: {}>'.format(self.last_edited)


    @staticmethod
    def get_last_edited():
        m = db.session.query(Meta).first()

        if m:
            return m.last_edited
        else:
            return None


    @staticmethod
    def update_last_edited():
        now = datetime.datetime.now()

        m = Meta(last_edited=now)

        # delete all the previous entries
        db.session.query(Meta).delete()

        # add the new entry
        db.session.add(m)
        db.session.commit()

        return now


class BikePoint(db.Model):
    __tablename__ = 'bikepoints'

    bp_id = db.Column(db.String(), primary_key=True)

    name = db.Column(db.String())

    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    nbDocks = db.Column(db.Integer())
    nbBikes = db.Column(db.Integer())
    nbEmptyDocks = db.Column(db.Integer())

    def __init__(self, bp_id, name, lat, lon, nbDocks, nbBikes, nbEmptyDocks):
        self.bp_id = bp_id

        self.name = name

        self.lat = lat
        self.lon = lon

        self.nbDocks = nbDocks
        self.nbBikes = nbBikes
        self.nbEmptyDocks = nbEmptyDocks


    @property
    def serialize(self):
        """Return object data in an easily serializeable format"""
        return {
            'id' : self.bp_id,
            'name' : self.name,
            'lat' : self.lat,
            'lon' : self.lon,
            'nbDocks' : self.nbDocks,
            'nbBikes' : self.nbBikes,
            'nbEmptyDocks' : self.nbEmptyDocks
        }

    def __repr__(self):
        return '<bp_id {}>'.format(self.bp_id)

