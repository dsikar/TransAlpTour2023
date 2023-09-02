import xml.etree.ElementTree as ET
import requests
import os

with open('API_KEY', 'r') as f:
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
    gpx_files = [
        "/home/daniel/Downloads/Day01GenevaToRiddes160km.gpx",
        "/home/daniel/Downloads/Day02SionToAndermatt161km.gpx",
        "/home/daniel/Downloads/Day03AndermattToTriesen135km.gpx",
        "/home/daniel/Downloads/Day04TriesenToElmen121km.gpx",
        "/home/daniel/Downloads/Day05ElmenToHausem137km.gpx",
        "/home/daniel/Downloads/Day06HausernToZell-am-See-Sud124km.gpx",
        "/home/daniel/Downloads/Day07Zell-am-See-SudToSpitall-an-der-Drau156km.gpx",
        "/home/daniel/Downloads/Day08Spitall-an-der-DrauToLjubljana175km.gpx",
        "/home/daniel/Downloads/Day09LjubljanaToCrikvenica159km.gpx",
        "/home/daniel/Downloads/Day10CrikvenicaToPag119km.gpx",
        "/home/daniel/Downloads/Day11PagToZadar51km.gpx"
    ]    
    for gpx_file in gpx_files:
        coords = extract_lat_lng_from_gpx(gpx_file)
        elevations = [get_elevation(lat, lng) for lat, lng in coords]
        
        # Write data to a new file
        output_file = os.path.splitext(gpx_file)[0] + '_with_elevation.txt'
        with open(output_file, 'w') as f:
            for (lat, lng), elevation in zip(coords, elevations):
                f.write(f"Latitude: {lat}, Longitude: {lng}, Elevation: {elevation} meters\n")

if __name__ == '__main__':
    main()

