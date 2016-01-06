# tfl-bikepoints
A web application that allows you to view live information about cycle hire in London, using the TfL API. It was developed using Python, Flask (w/ Jinja2 for templating) and PostgreSQL on the back-end, and Bootstrap and Leafletjs on the front-end.

If you want to use this application with a TfL application key (and you should, because it heavily rate-limits unregistered users), you should specify APP_ID and APP_KEY as environment variables. This application uses PostgreSQL to store information about bike hire points, so set DATABASE_URL. This is done automatically if you are using Heroku though!

## Usage

To download this project, use:

```git clone https://github.com/rjwebb/tfl-bikepoints.git```

Change to the project directory:

```cd tfl-bikepoints```

I recommend you create a new virtual environment so that you can 'sandbox' the python packages that you installed to run this application. Change to the virtual environment.

Then install the related packages with:

```pip install -r requirements.txt```

Then set the environment variables to specify APP_ID, APP_KEY and DATABASE_URL (that points to the PostgreSQL database for the project).

This application can be started with the command:

```python manage.py runserver```

If you want to deploy this to Heroku then I have supplied a ```Procfile```.

If you want to run unit tests, use:

```python test.py```
