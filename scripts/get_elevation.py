import xml.etree.ElementTree as ET
import requests
import os

base_path = "/home/daniel/git/TransAlpTour2023/scripts/"
api_key_path = os.path.join(base_path, 'API_KEY')

with open(api_key_path, 'r') as f:
    API_KEY = f.readline().strip()


# Replace with your actual API key
BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lng}&key={api_key}'

def extract_lat_lng_from_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    trackpoints = root.findall(".//default:trkpt", ns)
    coords = [(float(tp.get('lat')), float(tp.get('lon'))) for tp in trackpoints]
    return coords

def get_elevation(lat, lng):
    url = BASE_URL.format(lat=lat, lng=lng, api_key=API_KEY)
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['results'][0]['elevation']
    return None

def main():
    base_path = "/home/daniel/git/TransAlpTour2023/data/"
    gpx_files = [
        os.path.join(base_path, "Day01GenevaToRiddes160km.gpx"),
        os.path.join(base_path, "Day02SionToAndermatt161km.gpx"),
        os.path.join(base_path, "Day03AndermattToTriesen135km.gpx"),
        os.path.join(base_path, "Day04TriesenToElmen121km.gpx"),
        os.path.join(base_path, "Day05ElmenToHausem137km.gpx"),
        os.path.join(base_path, "Day06HausernToZell-am-See-Sud124km.gpx"),
        os.path.join(base_path, "Day07Zell-am-See-SudToSpitall-an-der-Drau156km.gpx"),
        os.path.join(base_path, "Day08Spitall-an-der-DrauToLjubljana175km.gpx"),
        os.path.join(base_path, "Day09LjubljanaToCrikvenica159km.gpx"),
        os.path.join(base_path, "Day10CrikvenicaToPag119km.gpx"),
        os.path.join(base_path, "Day11PagToZadar51km.gpx")
    ]
    for gpx_file in gpx_files:
        print(f"Processing file: {gpx_file}")
        coords = extract_lat_lng_from_gpx(gpx_file)
        print(f"Extracted {len(coords)} coordinates from {gpx_file}")

        elevations = []
        for lat, lng in coords:
            elevation = get_elevation(lat, lng)
            elevations.append(elevation)
            print(f"Retrieved elevation {elevation} meters for Latitude: {lat}, Longitude: {lng}")
        
        # Write data to a new file
        output_file = os.path.splitext(gpx_file)[0] + '_with_elevation.txt'
        with open(output_file, 'w') as f:
            for (lat, lng), elevation in zip(coords, elevations):
                f.write(f"Latitude: {lat}, Longitude: {lng}, Elevation: {elevation} meters\n")

if __name__ == '__main__':
    main()

