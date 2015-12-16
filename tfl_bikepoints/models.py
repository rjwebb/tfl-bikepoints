from tfl_bikepoints import db

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_edited = db.Column(db.DateTime())

    def __init__(self, last_edited):
        self.last_edited = last_edited

    def __repr__(self):
        return '<last_edited: {}>'.format(self.last_edited)


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

    def to_marker_data(self):
        return { 'pos': [self.lat, self.lon],
                 'name': self.name,
                 'id': self.bp_id,
                 'url': '/bikepoint/%s' % self.bp_id}

    def __repr__(self):
        return '<bp_id {}>'.format(self.bp_id)

