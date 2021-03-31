import rejson
import time
import os

r = rejson.Client(host=os.environ['REDIS_HOST'],
                  password=os.environ['REDIS_PASS'],
                  port=os.environ['REDIS_PORT'], db=0)

while True:
    pipe = r.pipeline(transaction=False)
    path = "path:sonde:foo"
    pipe.jsonset(path, rejson.Path.rootPath(), {
        "type" : "Feature",
        "geometry" : {
            "type": "LineString",
            "coordinates": [],
        },
        "properties": {
            "coordinateProperties": []
        }
    }, nx=True)
    pipe.jsonarrappend(path, rejson.Path(".geometry.coordinates"), [47, 15, 920])
    per_sample_props = {
        "type":"Feature",
        "geometry":{
            "type":"Point",
            "coordinates":[26.2153,60.34085,417.0]
        },
        "properties":{
            "temp":3.6,
            "serial":"S0730589",
            "humidity":64.6,
            "vel_h":16.0,
            "uploader_callsign":"Lahti 24h raspberry",
            "time":1617220020,
            "uploader":{
                "callsign":"Lahti 24h raspberry"
            }
        }
    }
    pipe.jsonarrappend(path, rejson.Path(".properties.coordinateProperties"),per_sample_props)
    pipe.execute()
    time.sleep(0.01)
