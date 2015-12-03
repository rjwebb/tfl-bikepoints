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
        if self.use_auth:
            req_params = copy.copy(params)
            req_params['app_id'] = self.app_id
            req_params['app_key'] = self.app_key
        else:
            req_params = params

        return requests.get(url, params=req_params)

    def __get_json(self, url, params={}):
        return self.__get_url(url, params=params).json()

    def bikepoints(self):
        u = self.root_url + "/BikePoint"
        return self.__get_json(u)

    def bikepoint(self, bikepoint_id):
        u = self.root_url + "/BikePoint/%s" % bikepoint_id
        return self.__get_json(u)

    def bikepoint_bounding(self, swLat, swLon, neLat, neLon):
        u = self.root_url + "/BikePoint"
        params = {'swLat': swLat, 'swLon': swLon,
                  'neLat': neLat, 'neLon': neLon}
        return self.__get_json(u, params)

    def bikepoint_query(self, query):
        u = self.root_url + "/BikePoint/Search"
        params = {'query': query}
        return self.__get_json(u, params)
