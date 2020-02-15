from flask import Flask, request
import googlemaps
from datetime import datetime
import polyline
import json

with open('backend/google_key.txt', 'r') as f:
    google_key = f.read()

app = Flask(__name__)
gmaps = googlemaps.Client(key=google_key)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.rout('/direction')
def get_direction():
    start = request.args.get("start")
    end = request.args.get("end")
    mode = request.args.get("mode")

    directions_result = gmaps.directions(start,
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
    response = {
        "distance": directions_result["distance"]["value"],
        "duration": directions_result["duration"]["value"],
        "arrival_time": directions_result["arrival_time"]["value"],
        "steps": parse_steps(directions_result["steps"]),
        "overview_polyline": polyline.decode(directions_result["overview_polyline"]["points"])
    }
    return json.dumps(response)

def parse_steps(steps):
    return ""

if __name__ == "__main__":
    now = datetime.now()
    
    directions_result = gmaps.directions((52.52103409999999,13.4127321),
                                     "TU Berlin",
                                     mode="transit",
                                     departure_time=now)
    print(directions_result)
    points = get_polyline_from_direction(directions_result[0])
    #app.run(debug=True)
    