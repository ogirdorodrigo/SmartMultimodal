import requests
import json
from sklearn.neighbors import DistanceMetric, BallTree
import numpy as np

def get_available_freebikes():
    # Available nextbikes that are not in stations
    urls = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_de/en/free_bike_status.json"

    response = requests.get(url=urls)
    bikes = json.loads(response.text.encode('utf8')).get('data').get('bikes')
    return bikes


def get_available_stationbikes():
    """Return two dictionaries:
    1. bikes: dictionary of station id (keys) with number of available bikes as value
    2. stations_coordinates: dictionary of coordinates (keys) with station id as value
    """
    # Available nextbikes that are not in stations
    urls = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_de/en/station_status.json"
    response = requests.get(url=urls)
    stations = json.loads(response.text.encode('utf8')).get('data').get('stations')
    bikes = {station.get('station_id'): station.get('num_bikes_available') for station in stations
             if station.get('num_bikes_available') > 0}

    # Get station positions
    urls = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_de/en/station_information.json"
    response = requests.get(url=urls)
    stations_info = json.loads(response.text.encode('utf8')).get('data').get('stations')
    stations_coordinates = {(station.get('lon'), station.get('lat')): station.get('station_id') for station
                            in stations_info}

    return bikes, stations_coordinates


def find_nearest_bikestations(lon: float, lat: float):
    """Return a dictionary with coordinate-tuples (keys) and number of available bikes per station within 0.5 of
    (lon, lat) coordinate (value) and list of distances
    """
    bikes, stations = get_available_stationbikes()
    stations_coordinates = list(stations.keys())
    dist = DistanceMetric.get_metric('haversine')
    tree = BallTree(np.array(stations_coordinates), metric=dist)

    # nearest_stations_ix = tree.query_ball_point((lon, lat), 0.5)
    dist, nearest_stations_ix = tree.query(np.array([(lon, lat)]), 5)
    nearest_stations = [stations_coordinates[i] for i in nearest_stations_ix[0]]
    nearest_bikes = {station: bikes.get(stations.get(station), 0) for station in nearest_stations}

    return nearest_bikes, dist


def find_nearest_freebikes(lon: float, lat: float):
    """Return list of coordinates to the nearest free bikes (not locked to a station), and distance"""
    freebikes = get_available_freebikes()
    bikes = [(bike.get('lon'), bike.get('lat')) for bike in freebikes if
             (bike.get('is_reserved') == 0 and bike.get('is_disabled') == 0)]
    dist = DistanceMetric.get_metric('haversine')
    tree = BallTree(np.array(bikes), metric=dist)
    # nearest_bikes_ix = tree.query_ball_point((lon, lat), 0.5)
    dist, nearest_bikes_ix = tree.query(np.array([(lon, lat)]), 5)

    return [bikes[i] for i in nearest_bikes_ix[0]], dist


if __name__ == "__main__":
    print(find_nearest_freebikes(13.384524, 52.453312))
    print(find_nearest_bikestations(13.384524, 52.453312))
