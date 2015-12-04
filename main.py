from flask import Flask, render_template, request
from collections import defaultdict

from tfl import TfL

import tfl_config

# Initialise the Flask web application
app = Flask(__name__)
app.debug = True

# Initialise the TFL API object - this encapsulates the methods for
# retrieving data, and 'holds' the authentication information.
tfl_api = TfL( auth=tfl_config.auth )


# Controller for listing all of the BikePoints
@app.route("/")
def index(error=""):
    bikepoints = tfl_api.bikepoints()
    return render_template('index.html', bikepoints=bikepoints, error=error)

@app.route("/about")
def about_page():
    return render_template('about.html')

# Controller for a search where no query string is given.
@app.route("/search/")
def search_bikepoints():
    query = request.args.get('query')
    if query:
        bikepoints = tfl_api.bikepoint_query(query)
        return render_template('query_results.html',
                               bikepoints=bikepoints,
                               query=query)
    else:
        # error - no query given!
        error = "No query string given!"
        return index(error=error)

# Controller for a single BikePoint view
@app.route("/bikepoint/<bikepoint_id>")
def single_bikepoint(bikepoint_id):
    bikepoint = tfl_api.bikepoint(bikepoint_id)

    for p in bikepoint['additionalProperties']:
        bikepoint[p['key']] = p['value']

    return render_template('bikepoint.html', bikepoint=bikepoint)

# Boilerplate ;)
if __name__ == "__main__":
    app.run()
