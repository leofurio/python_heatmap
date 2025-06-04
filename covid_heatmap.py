import pandas as pd
import folium
from folium.plugins import HeatMap

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def main():
    data = pd.read_csv(URL)
    latest_date = data.columns[-1]
    # Keep only coordinates and latest case count
    df = data[['Lat', 'Long', latest_date]].copy()
    df = df.dropna(subset=['Lat', 'Long'])
    df = df[df[latest_date] > 0]
    heat_data = df.values.tolist()

    m = folium.Map(location=[0, 0], zoom_start=2)
    HeatMap(heat_data, radius=8).add_to(m)
    m.save('covid_heatmap.html')
    print(f"Heatmap saved to covid_heatmap.html for date {latest_date}.")

if __name__ == "__main__":
    main()
