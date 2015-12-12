from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import datetime
import json
import os

from collections import defaultdict
from tfl import TfL

# Initialise the Flask web application
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import BikePoint, Meta

BIKE_DATA_TIMEOUT = datetime.timedelta(seconds=60)


def get_auth_from_environ():
    app_id = os.environ.get('APP_ID',"")
    app_key = os.environ.get('APP_KEY',"")
    return app_id, app_key

def get_map_bounds(bikepoints):
    """
    Given a list of BikePoint objects, find the
    bounds of the area that encloses them all.
    """

    if len(bikepoints) == 0:
        return None
    else:
        latitudes = [bp.lat for bp in bikepoints]
        longitudes = [bp.lon for bp in bikepoints]

        return [ [max(latitudes), max(longitudes)],
                 [min(latitudes), min(longitudes)] ]

def extract_marker_data(bikepoints):
    return [{ 'pos': [bp.lat, bp.lon],
              'name': bp.name,
              'id': bp.bp_id,
              'url': '/bikepoint/%s' % bp.bp_id} for bp in bikepoints]

def get_last_edited():
    m = db.session.query(Meta).first()
    if m:
        return m.last_edited
    else:
        return None

def update_last_edited():
    now = datetime.datetime.now()

    m = Meta(last_edited=now)

    # delete all the previous entries
    db.session.query(Meta).delete()

    # add the new entry
    db.session.add(m)
    db.session.commit()

def update_bike_data_if_old(time_limit=BIKE_DATA_TIMEOUT):
    last_edited = get_last_edited()
    now = datetime.datetime.now()

    if now - last_edited > BIKE_DATA_TIMEOUT:
        update_bike_data()

def update_bike_data():
    bikepoint_data = TfL( auth=get_auth_from_environ() ).bikepoints()

    start_t = datetime.datetime.now()

    # delete all the old bikepoint data points
    db.session.query(BikePoint).delete()

    # add the updated bikepoints to the db
    for bp in bikepoint_data:
        additional_properties = dict([ (x['key'],x['value']) for x in bp['additionalProperties']])

        params = {
            'bp_id': bp['id'],
            'name': bp['commonName'],
            'lat': bp['lat'],
            'lon': bp['lon'],
            'nbDocks': additional_properties['NbDocks'],
            'nbBikes': additional_properties['NbBikes'],
            'nbEmptyDocks': additional_properties['NbEmptyDocks']
        }
        db.session.add(BikePoint(**params))

    db.session.commit()

    end_t = datetime.datetime.now()

    print "alt database update took", (end_t - start_t)

    update_last_edited()

# Controller for listing all of the BikePoints
@app.route("/")
def index(error=""):
    update_bike_data_if_old()
    bikepoints = list(db.session.query(BikePoint).all())

    marker_data = extract_marker_data(bikepoints)
    map_bounds = get_map_bounds(bikepoints)
    marker_data_json = json.dumps(marker_data)

    return render_template('index.html', bikepoints=bikepoints,
                           marker_data=marker_data_json,
                           map_bounds=map_bounds,
                           error=error)

@app.route("/about")
def about_page():
    return render_template('about.html')

# Controller for a search where no query string is given.
@app.route("/search/")
def search_bikepoints():
    query = request.args.get('query')
    if query:
        update_bike_data_if_old()

        ilike_q = "%{}%".format(query)
        bikepoints = BikePoint.query.filter(BikePoint.name.ilike(ilike_q)).all()

        marker_data = extract_marker_data(bikepoints)
        map_bounds = get_map_bounds(bikepoints)
        marker_data_json = json.dumps(marker_data)

        return render_template('query_results.html',
                               bikepoints=bikepoints,
                               marker_data=marker_data_json,
                               map_bounds=map_bounds,
                               query=query)

    else:
        # error - no query given
        # go back to the main index page (i.e. show all things)
        error = "No query string given!"
        return index(error=error)

# Controller for a single BikePoint view
@app.route("/bikepoint/<bikepoint_id>")
def single_bikepoint(bikepoint_id):
    update_bike_data_if_old()

    bikepoint = db.session.query(BikePoint).get(bikepoint_id)
    if bikepoint:
        return render_template('bikepoint.html', bikepoint=bikepoint)
    else:
        pass # todo: a 404 page

# Boilerplate ;)
if __name__ == "__main__":
    app.run()
