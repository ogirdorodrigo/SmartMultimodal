from flask import Flask
import googlemaps
from datetime import datetime
import polyline


app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyCypPj6yAIQ2g2Iu9X0qpGEMSw6Vzw-x0Y')

@app.route('/')
def hello_world():
    return 'Hello, World!'

def get_polyline_from_direction(direction):
    encoded = direction["overview_polyline"]["points"]
    return polyline.decode(encoded)

if __name__ == "__main__":
    now = datetime.now()
    directions_result = gmaps.directions("Tempelhoferfeld",
                                     "Alexanderplatz",
                                     mode="transit",
                                     departure_time=now)
    #print(directions_result)
    points = get_polyline_from_direction(directions_result[0])
    #app.run(debug=True)
    