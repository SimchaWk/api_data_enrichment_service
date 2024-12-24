import os
import googlemaps
from dotenv import load_dotenv

load_dotenv(verbose=True)

google_maps_api_key = os.environ['GOOGLE_MAPS_API_KEY']


def create_gmaps_client(api_key: str = google_maps_api_key):
    return googlemaps.Client(key=api_key)


if __name__ == '__main__':
    print(create_gmaps_client())