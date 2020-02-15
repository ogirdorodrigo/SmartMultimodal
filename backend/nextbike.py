import requests
import json

def get_available_freebikes():
    # Available nextbikes that are not in stations
    urls = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_de/en/free_bike_status.json"

    response = requests.get(url=urls)

    return json.loads(response.text.encode('utf8'))

if __name__ == "__main__":
    print(get_available_scooters())
