# tfl-bikepoints
A Flask web application that allows you to view live information about cycle hire in London, using the TfL API.

If you want to use this application with a TfL application key (and you should, because it heavily rate-limits unregistered users), you should specify APP_ID and APP_KEY as environment variables. This application uses PostgreSQL to store information about bike hire points, so set DATABASE_URL. This is done automatically if you are using Heroku though!

This application can be started with the command:
        python main.py
