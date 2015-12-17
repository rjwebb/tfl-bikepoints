from tfl_bikepoints import app
import json

@app.template_filter('as_markers')
def as_markers_filter(bikepoints):
    """
    Given a list of BikePoint objects,
    return it as a JSON list in the Leafleft marker format
    """
    l = [{ 'pos': [bp.lat, bp.lon],
          'name': bp.name,
           'id': bp.bp_id,
           'url': '/bikepoint/%s' % bp.bp_id} for bp in bikepoints]

    return json.dumps(l)
