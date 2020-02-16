import requests
import json
import os
from scipy.spatial import KDTree
from sklearn.neighbors import DistanceMetric, BallTree
import numpy as np

def get_scooters_batch(url):
    # Request parameters
    payload = {}
    headers = {
        'x-api-key': 'gXKxBRaZsYaXUyMyyvpKxADg',
        'Accept': 'application/vnd.mds.provider+json;version=0.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text.encode('utf8'))
    trips = data.get('data').get('trips')
    next_url = data.get('links').get('next')

    return trips, next_url


def download_tier_dataset():
    """Tier provides only a static dataset containing the following fields for each trip of the corresponding
    scooters (example):
    'provider_id': '264aad41-b47c-415d-8585-0208d436516e',
    'provider_name': 'Tier',
    'device_id': '907cd31e-8310-426b-ab01-020ad0ca7653',
    'vehicle_id': '221442',
    'vehicle_type': 'scooter',
    'propulsion_type': ['electric'],
    'trip_id': '048909eb-0008-5db5-bc19-edb134b50506',
    'trip_duration': 1980,
    'trip_distance': 9900,
    'route': {'type': 'FeatureCollection',
     'features': [{'type': 'Feature',
       'geometry': {'type': 'Point', 'coordinates': [13.388497, 52.518546]},
       'properties': {'timestamp': 1580588718000}},
      {'type': 'Feature',
       'geometry': {'type': 'Point', 'coordinates': [13.368137, 52.510468]},
       'properties': {'timestamp': 1580590690000}}]},
    'accuracy': 20,
    'start_time': 1580588718000,
    'end_time': 1580590690000},
    """
    dataset = []
    next_page = True
    i = 0
    # Entry point to Tier complete dataset
    url = "https://platform.tier-services.io/mds/BERLIN/trips"
    with open(os.path.join('..', 'data', 'tier_scooters.json'), 'w') as f:
        f.write('{"data": ')

    while next_page:
        try:
            new_batch, url = get_scooters_batch(url)
        except:
            break
        dataset += new_batch
        i += 1
        print(i, len(dataset))

    with open(os.path.join('..', 'data', 'tier_scooters.json'), 'a') as f:
        json.dump(dataset, f)
        f.write('}')

    return dataset


def reduce_dataset():
    with open(os.path.join('..', 'data', 'tier_scooters.json'), 'r') as f:
        data = json.load(f)
    fleet = dict()
    for scooter in data.get('data'):
        if fleet.get(scooter.get('vehicle_id')) is None:
            fleet[scooter.get('vehicle_id')] = scooter

    with open(os.path.join('..', 'data', 'tier_fleet.json'), 'w') as f:
        json.dump({'data': [fleet]}, f)

    fleet_location = {scooter: tuple(fleet[scooter].get('route').get('features')[0].get('geometry').get('coordinates')) for scooter in fleet}

    with open(os.path.join('..', 'data', 'tier_fleet_locations.json'), 'w') as f:
        json.dump({'data': [fleet_location]}, f)

    return fleet


def find_nearest_tier(lon: float, lat: float):
    """Return list of coordinates to the nearest scooters and list of distances"""
    with open(os.path.join('data', 'tier_fleet_locations.json'), 'r') as fd:
        fleet = json.load(fd).get('data')[0]

    scooters = [val for val in fleet.values()]
    dist = DistanceMetric.get_metric('haversine')
    tree = BallTree(np.array(scooters), metric=dist)
    dist, nearest_scooters_ix = tree.query(np.array([(lon, lat)]), 5)

    return [scooters[i] for i in nearest_scooters_ix[0]], dist


if __name__ == "__main__":
    print(find_nearest_tier(13.384524, 52.453312))