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
    """
    If the bike point data is out of date by more than time_limit,
    then update it from the TfL API
    """
    last_edited = Meta.get_last_edited()
    now = datetime.datetime.now()

    # if the database is due an update
    if not last_edited or now - last_edited > time_limit:
        update_bike_data()

        # update the last edited timestamp
        Meta.update_last_edited()


def update_bike_data():
    """
    Update the bike point data from the TfL API
    """
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


"""
Controllers
"""


@app.route("/")
def index(error=""):
    """
    Controller for displaying all of the bike points
    """
    update_bike_data_if_old()

    bikepoints = db.session.query(BikePoint).all()

    return render_template('bikepoints_map.html', bikepoints=bikepoints,
                           error=error)


@app.route("/search/")
def search_bikepoints():
    """
    Controller for displaying the results of a search for bike points
    """
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


@app.route("/bikepoint/<bikepoint_id>")
def single_bikepoint(bikepoint_id):
    """
    Controller for displaying information about a single bike point
    """
    update_bike_data_if_old()

    bikepoint = db.session.query(BikePoint).get(bikepoint_id)

    if bikepoint:
        return render_template('bikepoint_detail.html', bikepoint=bikepoint)
    else:
        abort(404)


@app.route("/about")
def about_page():
    """
    Controller for displaying an About page
    """
    return render_template('about.html')


"""
Controllers for returning information in JSON format
"""

@app.route("/bikepoint_api")
def all_bikepoints_json():
    """
    Returns a JSON object of all bike points in the database
    """
    update_bike_data_if_old()

    bikepoints = db.session.query(BikePoint).all()

    return jsonify(json_list=[bp.serialize for bp in bikepoints])


@app.route("/search_api/")
def search_bikepoints_json():
    """
    Return a JSON object of all bike points whose names contain
    the string 'query'
    """
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


@app.route("/bikepoint_api/<bikepoint_id>")
def single_bikepoint_json(bikepoint_id):
    """
    Return the JSON data for a single bike point
    """
    update_bike_data_if_old()

    bikepoint = db.session.query(BikePoint).get(bikepoint_id)

    if bikepoint:
        return jsonify(bikepoint.serialize)
    else:
        abort(404)


"""
Error handler
"""
@app.errorhandler(404)
def page_not_found(e):
    """
    Displays a '404 File Not Found' page
    """
    return render_template('404.html'), 404
