import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
from math import sqrt

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def main():
    data = pd.read_csv(URL)

    # Columns from index 4 onwards contain the daily counts
    date_cols = data.columns[4:]

    grouped = data.groupby(['Lat', 'Long'])[date_cols].sum().reset_index()
    iso_dates = pd.to_datetime(date_cols).strftime("%Y-%m-%d")

    features = []
    scale = 100
    for _, row in grouped.iterrows():
        lat = row['Lat']
        lon = row['Long']
        for date, iso in zip(date_cols, iso_dates):
            count = row[date]
            if count <= 0:
                continue
            radius = max(2, sqrt(count) / scale)
            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "properties": {
                        "time": iso,
                        "icon": "circle",
                        "iconstyle": {
                            "fillColor": "red",
                            "color": "red",
                            "fillOpacity": 0.6,
                            "opacity": 0.6,
                            "radius": radius,
                        },
                        "popup": f"Cases: {int(count)}",
                    },
                }
            )

    m = folium.Map(location=[0, 0], zoom_start=2)
    TimestampedGeoJson(
        {"type": "FeatureCollection", "features": features},
        period="P1D",
        add_last_point=False,
        auto_play=False,
    ).add_to(m)
    m.save('covid_bubble_map.html')
    print(
        f"Bubble map saved to covid_bubble_map.html for dates {date_cols[0]} to {date_cols[-1]}."
    )

if __name__ == "__main__":
    main()
