
import logging
import db_helper
import json
# import geojson
# from geoalchemy.shape import from_shape
from flask import request, Response, jsonify
from models import Poi, PoiType, PoiProperty, PoiPropertyRelation
from sqlalchemy import func
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if (
                    not x.startswith('_') and x != 'metadata')]:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values
                    fields[field] = data
                    json.dumps(data)
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

RANGE_CMD = 'poi_in_polygon'
NAME_CMD = 'poi_by_name'
TYPE_CMD = 'poi_by_type'
PROP_CMD = 'poi_by_property'

'''
  json cmd for poi in polygon:
  {
      "poi_in_polygon": {
        "type": "Feature",
        "properties": {
            "name": "bla",
            "area": 2947
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
                [
                  [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                  [100.0, 1.0], [100.0, 0.0]
                ]
            ],
            "crs": {
                "type": "name",
                "properties": {
                    "name": "EPSG:4326"
                }
            }
        },
      },
      "poi_by_name": "name",
      "poi_by_type": ["type_name"],
      "poi_by_property": ["prop1", "prop2", ... ]
  }
'''


def handle_poi_range(q, param):
    poly = json.dumps(param['geometry'])
    poly = func.ST_GeomFromGeoJSON(poly)
    # poly = geojson.loads(param)
    return q.filter(func.ST_WITHIN(Poi.geo_location, poly))


def hande_poi_name(q, param):
    return q.filter(Poi.name == param)


def handle_poi_type(q, param):
    return q.filter(PoiType.name.in_(param))


def handle_poi_by_property(q, data):
    if data:
        q = q.join(PoiPropertyRelation, PoiPropertyRelation.poi_id == Poi.id)
        q = q.join(PoiProperty, PoiProperty.id == PoiPropertyRelation.prop_id)
        q = q.filter(PoiProperty.name.in_(data))
    return q


CMD_MAP = {
    RANGE_CMD: handle_poi_range,
    NAME_CMD: hande_poi_name,
    TYPE_CMD: handle_poi_type,
    PROP_CMD: handle_poi_by_property
}


def handle_poi_request(url, req: request):
    data = req.get_json()
    keys = data.keys()
    if keys and len(keys) > 0:
        session = db_helper.session
        q = session.query(Poi).join(PoiType, Poi.poi_type_id == PoiType.id)
        for k in keys:
            if k not in CMD_MAP:
                return f'Unsupported cmd: {data}'
            q = CMD_MAP[k](q, data[k])
        return json_response(q)
    return f'Unsupported cmd: {data}'


def debugprint(statement, dialect=None, reindent=True):
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        if dialect is None:
            dialect = statement.session.get_bind().dialect
        statement = statement.statement
    compiled = statement.compile(dialect=dialect,
                                 compile_kwargs={'literal_binds': True})
    return str(compiled)


def json_response(query):
    # qry = debugprint(query)
    rows = query.limit(100).all()
    if rows:
        raw = [json.dumps(row, cls=AlchemyEncoder) for row in rows]
    else:
        raw = '{"response": "No results"}'
    resp = Response(raw,  mimetype='application/json')
    return resp
