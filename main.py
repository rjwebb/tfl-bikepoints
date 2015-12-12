from flask import Flask, render_template, request
from collections import defaultdict

from tfl import TfL

import json
import os

# Initialise the Flask web application
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

def get_auth_from_environ():
    app_id = os.environ.get('APP_ID',"")
    app_key = os.environ.get('APP_KEY',"")
    return app_id, app_key

def get_map_bounds(markers):
    """
    Given a list of markers (dicts) with a 'pos' attribute of
    the form (latitude, longitude), find the bounds of the map
    needed to show all of the markers.
    """
    latitudes = [bp['pos'][0] for bp in markers]
    longitudes = [bp['pos'][1] for bp in markers]

    return [ [max(latitudes), max(longitudes)],
             [min(latitudes), min(longitudes)] ]

def extract_marker_data(bikepoints):
    return [{ 'pos': [bp['lat'], bp['lon']],
              'commonName': bp['commonName'],
              'id': bp['id'],
              'url': '/bikepoint/%s' % bp['id']} for bp in bikepoints]

# Controller for listing all of the BikePoints
@app.route("/")
def index(error=""):
    bikepoints = TfL( auth=get_auth_from_environ() ).bikepoints()

    marker_data = extract_marker_data(bikepoints)
    map_bounds = get_map_bounds(marker_data)
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
        bikepoints = TfL( auth=get_auth_from_environ() ).bikepoint_query(query)
        marker_data = extract_marker_data(bikepoints)
        map_bounds = get_map_bounds(marker_data)
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
    bikepoint = TfL( auth=get_auth_from_environ() ).bikepoint(bikepoint_id)

    for p in bikepoint['additionalProperties']:
        bikepoint[p['key']] = p['value']

    return render_template('bikepoint.html', bikepoint=bikepoint)

# Boilerplate ;)
if __name__ == "__main__":
    app.run()
