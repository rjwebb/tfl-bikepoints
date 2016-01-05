#stdlib
import datetime
import json
import os

#flask
from flask import render_template, request, abort, jsonify

#tfl api
from tfl import TfL

#this app
from tfl_bikepoints import app, db
from tfl_bikepoints.models import BikePoint, Meta


def update_bike_data_if_old(time_limit=app.config['BIKE_DATA_TIMEOUT']):
    last_edited = Meta.get_last_edited()
    now = datetime.datetime.now()

    # if the database is due an update
    if not last_edited or now - last_edited > time_limit:
        update_bike_data()

        # update the last edited timestamp
        Meta.update_last_edited()


def update_bike_data():
    print "requesting more data from TfL"

    # Get the bike hire data from TfL's API
    app_id = os.environ.get('APP_ID',"")
    app_key = os.environ.get('APP_KEY',"")
    bikepoint_data = TfL( auth=(app_id, app_key) ).bikepoints()

    # delete all the old bikepoint data points
    db.session.query(BikePoint).delete()

    # add the updated bikepoints to the db
    for bp in bikepoint_data:
        additional_properties = dict([ (x['key'],x['value']) for x in bp['additionalProperties']])

        # Create a BikePoint object
        bp_obj = BikePoint(bp_id=bp['id'],
                           name=bp['commonName'],
                           lat=bp['lat'],
                           lon=bp['lon'],
                           nbDocks=additional_properties['NbDocks'],
                           nbBikes=additional_properties['NbBikes'],
                           nbEmptyDocks=additional_properties['NbEmptyDocks'])

        # Add it to the database transaction
        db.session.add(bp_obj)

    # Commit the additions of the BikePoints to the database
    db.session.commit()


# Controller for listing all of the BikePoints
@app.route("/")
def index(error=""):
    update_bike_data_if_old()

    bikepoints = db.session.query(BikePoint).all()

    return render_template('bikepoints_map.html', bikepoints=bikepoints,
                           error=error)


@app.route("/about")
def about_page():
    return render_template('about.html')


# Controller for a search where no query string is given.
@app.route("/search/")
def search_bikepoints():
    query = request.args.get('query')

    # make sure it wasn't just a blank query
    if query:
        update_bike_data_if_old()

        ilike_q = "%{}%".format(query)
        bikepoints = BikePoint.query.filter(BikePoint.name.ilike(ilike_q)).all()
        return render_template('bikepoints_map.html',
                               bikepoints=bikepoints,
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
        return render_template('bikepoint_detail.html', bikepoint=bikepoint)
    else:
        abort(404)



"""
Controllers for returning information in JSON format
"""

@app.route("/bikepoint_api/<bikepoint_id>")
def single_bikepoint_json(bikepoint_id):
    update_bike_data_if_old()

    bikepoint = db.session.query(BikePoint).get(bikepoint_id)

    if bikepoint:
        return jsonify(bikepoint.serialize)
    else:
        abort(404)

@app.route("/bikepoint_api")
def all_bikepoints_json():
    update_bike_data_if_old()

    bikepoints = db.session.query(BikePoint).all()

    return jsonify(json_list=[bp.serialize for bp in bikepoints])

# Controller for a search where no query string is given.
@app.route("/search_api/")
def search_bikepoints_json():
    query = request.args.get('query')

    # make sure it wasn't just a blank query
    if query:
        update_bike_data_if_old()

        ilike_q = "%{}%".format(query)
        bikepoints = BikePoint.query.filter(BikePoint.name.ilike(ilike_q)).all()
        return jsonify(json_list=[bp.serialize for bp in bikepoints])

    else:
        error = "No query string given"
        return jsonify(error=error), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
