from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

# Initialise the Flask web application
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Initialise the database
db = SQLAlchemy(app)

import tfl_bikepoints.controllers
import tfl_bikepoints.filters
