import pdb
import unittest

from tfl_bikepoints import app, db
from tfl_bikepoints.models import Meta
#import tfl_bikepoints.controllers as controllers
# Uses code from: kronosapiens.github.io/blog/2014/07/29/setting-up-unit-tests-with-flask.html


class TestMeta(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tfl_bikepoints.config.TestingConfig')
        db.session.close()
        db.drop_all()
        db.create_all()

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


if __name__ == '__main__':
    unittest.main()
