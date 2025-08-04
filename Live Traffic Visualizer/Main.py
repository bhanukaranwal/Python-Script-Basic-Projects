import folium
import random
import webbrowser
import os

def live_traffic_visualizer():
    print("\nWelcome to the Live Traffic Visualizer (Demo)!")
    # Some example city coordinates for demo purposes
    city_coords = {
        'new york': (40.7128, -74.0060),
        'san francisco': (37.7749, -122.4194),
        'london': (51.5074, -0.1278),
        'tokyo': (35.6762, 139.6503)
    }
    print("Cities available:", ', '.join(city_coords.keys()))
    city = input("Enter a city from above: ").lower()
    if city not in city_coords:
        print("City not available in demo. Please pick from the list.")
        return

    lat, lon = city_coords[city]
    print(f"Generating map for {city.title()} ...")

    # Create base map centered on selected city
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Simulated traffic incident markers
    for i in range(10):
        offset_lat = random.uniform(-0.05, 0.05)
        offset_lon = random.uniform(-0.05, 0.05)
        folium.Marker(
            [lat + offset_lat, lon + offset_lon],
            popup=f"Traffic incident {i+1}"
        ).add_to(m)

    file_path = f"traffic_map_{city.replace(' ', '_')}.html"
    m.save(file_path)
    print(f"Map saved as {file_path}. Opening in browser...")
    webbrowser.open('file://' + os.path.realpath(file_path))

if __name__ == '__main__':
    live_traffic_visualizer()
