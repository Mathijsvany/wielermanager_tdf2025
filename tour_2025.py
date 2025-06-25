import requests
import pandas as pd

url_data_TOUR = "https://d1y1o5nodoer6n.cloudfront.net/data_TOUR_2025_full.json"

try:
    response = requests.get(url_data_TOUR)
    response.raise_for_status()
    data = response.json()

except requests.exceptions.RequestException as e:
    print(f"Fout bij het ophalen of parsen van de JSON: {e}")
    exit()

df = pd.DataFrame(data["players"])

print(df.head())