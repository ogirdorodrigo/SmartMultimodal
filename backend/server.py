from flask import Flask, request
import googlemaps
from datetime import datetime
import polyline
import json
from backend.weather import get_weather_description, is_rain

with open('backend/google_key.txt', 'r') as f:
    google_key = f.read()


app = Flask(__name__)
gmaps = googlemaps.Client(key=google_key)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/route')
def get_route():
    start = request.args.get("start")
    end = request.args.get("end")
    mode = request.args.get("mode")
    callback = request.args.get("callback")
    mode = "transit"
    now = datetime.now()

    rout_result = gmaps.directions(start,
                                    end,
                                    mode=mode,
                                    departure_time=now)[0]

    #TODO what to return?
    """
    distance
    duration
    arrival_time
    steps
        distance
        duration
        polyline
        travel_mode
    overview_polyline
    """
    #print(directions_result['legs'][0])

    response = {
        "distance": rout_result['legs'][0]["distance"]["value"],
        "duration": rout_result['legs'][0]["duration"]["value"],
        # "arrival_time": directions_result['legs'][0]["arrival_time"]["value"],
        "steps": parse_steps(rout_result['legs'][0]["steps"]),
        "overview_polyline": polyline.decode(rout_result["overview_polyline"]["points"])
    }
    return f'{callback}({json.dumps(response)})'

@app.route('/is_headwind_for_route')
def is_headwind_for_route():
    start = request.args.get("start")
    end = request.args.get("end")
    d,ws,wd = get_weather_description(start)
    rd = get_bearing_for_route(start, end)

    diff = rd-wd
    callback = request.args.get("callback")
    return f'{callback}({diff<45 and diff>-45})'

@app.route('/is_rain_at_route')
def is_rain_at_route():
    loc = request.args.get("loc")
    return is_rain(loc[0], loc[1])



def get_bearing_for_route(start, end):
    geodesic = pyproj.Geod(ellps='WGS84')
    fwd_azimuth,back_azimuth,distance = geodesic.inv(start[0], start[1], end[0], end[1])
    return fwd_azimuth

def parse_steps(steps):
    steps_list = []
    for step in steps:
        steps_list.append({
            "distance": step["distance"]["value"],
            "duration":step["distance"]["value"],
            "polyline": polyline.decode(step["polyline"]["points"]),
            "travel_mode": step["travel_mode"]
        })
    return steps_list

if __name__ == "__main__":
    app.run(debug=True)
    