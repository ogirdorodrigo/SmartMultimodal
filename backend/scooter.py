import requests
import json

def get_available_scooters():
    # Open weather api key
    url = "https://platform.tier-services.io/mds/BERLIN/trips"

    payload = {}
    headers = {
        'x-api-key': 'gXKxBRaZsYaXUyMyyvpKxADg',
        'Accept': 'application/vnd.mds.provider+json;version=0.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text.encode('utf8')

if __name__ == "__main__":
    print(get_available_scooters())
