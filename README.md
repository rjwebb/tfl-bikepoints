# tfl-bikepoints
A Flask web application that allows you to view live information about cycle hire in London, using the TfL API.

If you want to use this application with a TfL application key (and you should, because it heavily rate-limits unregistered users), you should specify the environment variables in *.env*

This application requires the *Flask* and *requests* libraries, both available via *pip*.

This application can be started with the command:
        python main.py
