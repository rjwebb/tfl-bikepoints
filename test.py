import string
import pdb
import random
import unittest

from tfl_bikepoints import app, db
from tfl_bikepoints.models import Meta, BikePoint
import tfl_bikepoints.controllers as controllers

# Uses code from:
# kronosapiens.github.io/blog/2014/07/29/setting-up-unit-tests-with-flask.html

def random_string(size=10, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def create_bike_point_json(i=0):
    commonName = random_string(size=20)

    lat = random.random() * 360 - 180
    lon = random.random() * 360 - 180

    NbDocks = random.randint(30,50)
    NbBikes = random.randint(0, NbDocks)
    NbEmptyDocks = random.randint(0, NbDocks - NbBikes )

    return {
        "id" : "BikePoint_"+str(i),
        "commonName" : commonName,
        "lat" : lat,
        "lon" : lon,
        "additionalProperties" : [
            {"key" :"NbDocks", "value" : NbDocks},
            {"key" : "NbBikes", "value" : NbBikes},
            {"key" : "NbEmptyDocks", "value" : NbEmptyDocks}
        ]
    }

def floats_same(f1, f2, epsilon=0.0000000001):
    """
    Returns true if f1 and f2 are the same, up to some epsilon
    """
    return abs(f1 - f2) < epsilon

class TestProject(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tfl_bikepoints.config.TestingConfig')
        db.session.close()
        db.drop_all()
        db.create_all()


class TestMeta(TestProject):
    def test_initial_last_edited_no_data(self):
        all_meta = db.session.query(Meta).all()
        assert len(all_meta) == 0
        assert Meta.get_last_edited() == None

    def test_set_last_edited(self):
        # test it once
        now = Meta.update_last_edited()

        all_meta = db.session.query(Meta).all()
        assert len(all_meta) == 1

        l = Meta.get_last_edited()
        assert l == now

        # test it twice
        now2 = Meta.update_last_edited()

        all_meta = db.session.query(Meta).all()
        assert len(all_meta) == 1

        l2 = Meta.get_last_edited()
        assert l2 == now2


class TestBikePoint(TestProject):
    def test_bike_points_initially_empty(self):
        all_bp = db.session.query(BikePoint).all()
        assert len(all_bp) == 0

    def test_bike_point_from_json(self):
        test_jsons = [create_bike_point_json(i=i) for i in range(20)]

        for bp_json in test_jsons:
            db.session.add(BikePoint.from_json(bp_json))
        db.session.commit()

        # assert that they were added to the DB correctly!
        for bp in db.session.query(BikePoint).all():
            bp_json = test_jsons[int(bp.bp_id.split("_")[1])]
            assert bp_json['id'] == bp.bp_id
            assert bp_json['commonName'] == bp.name
            assert floats_same(bp_json['lat'], bp.lat)
            assert floats_same(bp_json['lon'], bp.lon)


if __name__ == '__main__':
    unittest.main()
