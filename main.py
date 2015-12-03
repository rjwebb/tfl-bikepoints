from flask import Flask, render_template
from collections import defaultdict

from tfl import TfL

import tfl_config

app = Flask(__name__)
app.debug = True


tfl_api = TfL( auth=tfl_config.auth )


@app.route("/")
def index(error=""):
    bikepoints = tfl_api.bikepoints()
    return render_template('index.html', bikepoints=bikepoints, error=error)


@app.route("/search/")
def blank_search_bikepoints():
    # error - no query given!
    error = "No query string given!"
    return index(error=error)


@app.route("/search/<query>")
def search_bikepoints(query):
    bikepoints = tfl_api.bikepoint_query(query)

    return render_template('query_results.html',
                           bikepoints=bikepoints,
                           query=query)


@app.route("/bikepoint/<bikepoint_id>")
def single_bikepoint(bikepoint_id):
    bikepoint = tfl_api.bikepoint(bikepoint_id)

    for p in bikepoint['additionalProperties']:
        bikepoint[p['key']] = p['value']

    return render_template('bikepoint.html', bikepoint=bikepoint)


if __name__ == "__main__":
    app.run()
