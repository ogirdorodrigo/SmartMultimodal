from flask import Flask
import googlemaps
from datetime import datetime
import polyline

with open('backend/google_key.txt', 'r') as f:
    google_key = f.read()

app = Flask(__name__)
gmaps = googlemaps.Client(key=google_key)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def get_polyline_from_direction(direction):
    encoded = direction["overview_polyline"]["points"]
    return polyline.decode(encoded)

if __name__ == "__main__":
    now = datetime.now()
    
    directions_result = gmaps.directions((52.52103409999999,13.4127321),
                                     "TU Berlin",
                                     mode="transit",
                                     departure_time=now)
    print(directions_result)
    points = get_polyline_from_direction(directions_result[0])
    #app.run(debug=True)
    