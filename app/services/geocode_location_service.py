from functools import lru_cache

from app.config.googlemaps_config.googlemaps_client import create_gmaps_client


@lru_cache(maxsize=None)
def get_coordinates(location_text, gmaps_client=None):
    if not gmaps_client:
        gmaps_client = create_gmaps_client()

    try:
        result = gmaps_client.geocode(location_text)
        if result:
            location = result[0]['geometry']['location']
            return {
                'lat': location['lat'],
                'lon': location['lng'],
                'address': result[0]['formatted_address'],
                'type': result[0]['types'][0]
            }
        return None

    except Exception as e:
        print(f"Error geocoding {location_text}: {e}")
        return None


# דוגמה לשימוש
def main():

    locations = ["New York", "France", "Pacific Ocean"]
    for loc in locations:
        result = get_coordinates(loc)
        print(result)
        if result:
            print(f"\nLocation: {loc}")
            print(f"Coordinates: {result['lat']}, {result['lon']}")
            print(f"Address: {result['address']}")


if __name__ == '__main__':
    main()
