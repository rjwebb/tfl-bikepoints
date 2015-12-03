import copy
import requests

class TfL(object):
    """
    A wrapper object for accessing the TfL API.
    Currently only works for bike rental points.
    """
    def __init__(self, auth=()):
        if auth:
            self.use_auth = True
            self.app_id, self.app_key = auth
        else:
            self.use_auth = False

        self.root_url = "https://api.tfl.gov.uk"

    def __get_url(self, url, params={}):
        """
        Internal method. Requests a url, with a given set of parameters.
        If we are using authentication, then include the app ID and key.
        """
        if self.use_auth:
            req_params = copy.copy(params)
            req_params['app_id'] = self.app_id
            req_params['app_key'] = self.app_key
        else:
            req_params = params

        return requests.get(url, params=req_params)

    def __get_json(self, url, params={}):
        """
        Same as __get_url, but returns the JSON content of the request.
        """
        return self.__get_url(url, params=params).json()

    def bikepoints(self):
        """
        Returns JSON of all of the BikePoints
        """
        u = self.root_url + "/BikePoint"
        return self.__get_json(u)

    def bikepoint(self, bikepoint_id):
        """
        Returns JSON for a single BikePoint with id=bikepoint_id
        """
        u = self.root_url + "/BikePoint/%s" % bikepoint_id
        return self.__get_json(u)

    def bikepoint_bounding(self, swLat, swLon, neLat, neLon):
        """
        Returns a JSON list of all of the BikePoints within a certain bounding box region.
        """
        u = self.root_url + "/BikePoint"
        params = {'swLat': swLat, 'swLon': swLon,
                  'neLat': neLat, 'neLon': neLon}
        return self.__get_json(u, params)

    def bikepoint_query(self, query):
        """
        Returns a JSON list of all of the BikePoints whose names contain the string query.
        """
        u = self.root_url + "/BikePoint/Search"
        params = {'query': query}
        return self.__get_json(u, params)
