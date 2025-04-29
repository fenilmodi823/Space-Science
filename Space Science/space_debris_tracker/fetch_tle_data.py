# fetch_tle_data.py

import requests
import os

def fetch_tle_data():
    """
    Fetches TLE data for active satellites from CelesTrak and saves it in the main project folder.
    """
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    response = requests.get(url)
    
    if response.status_code == 200:
        tle_data = response.text

        # Get the parent folder (space_debris_tracker) no matter where you run from
        project_folder = os.path.dirname(os.path.abspath(__file__))
        tle_path = os.path.join(project_folder, "tle_data.txt")

        with open(tle_path, "w") as file:
            file.write(tle_data)
        
        print(f"[INFO] TLE data fetched and saved to {tle_path}")
    else:
        print(f"[ERROR] Failed to fetch TLE data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_tle_data()
