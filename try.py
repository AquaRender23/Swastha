import requests

def find_hospitals_osm(lat, lon, radius=5000):
    # Overpass QL query to find hospital nodes and ways within radius (meters)
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={'data': query})
    
    if response.status_code != 200:
        print("Error from Overpass API:", response.status_code)
        return []
    data = response.json()
    hospitals = []
    for element in data.get('elements', []):
        name = element['tags'].get('name', 'Unnamed hospital')
        # For ways/relations 'center' has lat/lon; for nodes use lat/lon directly
        if 'center' in element:
            lat = element['center']['lat']
            lon = element['center']['lon']
        else:
            lat = element.get('lat')
            lon = element.get('lon')
        hospitals.append({
            'name': name,
            'latitude': lat,
            'longitude': lon
        })
    return hospitals

if __name__ == "__main__":
    jp_nagar_lat = 12.912647
    jp_nagar_lon = 77.588913
    radius_meters = 5000

results = find_hospitals_osm(jp_nagar_lat, jp_nagar_lon, radius_meters)
for hospital in results:
    print(hospital)

    