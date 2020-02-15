import requests
import json
from os.path import join as pjoin

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
    f = open(pjoin('..', 'data', 'tier_scooters.json'), 'a')
    while next_page:
        try:
            new_batch, url = get_scooters_batch(url)
        except:
            next_page = False
        dataset += new_batch
        i += 1
        print(i, len(dataset))
        json.dump(new_batch, f)

    f.close()

    return dataset


if __name__ == "__main__":
    download_tier_dataset()
