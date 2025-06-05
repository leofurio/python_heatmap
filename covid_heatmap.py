import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def main():
    data = pd.read_csv(URL)

    # Columns from index 4 onwards contain the daily counts
    date_cols = data.columns[4:]

    heat_data = []
    for date in date_cols:
        df = data[['Lat', 'Long', date]].copy()
        df = df.dropna(subset=['Lat', 'Long'])
        df = df[df[date] > 0]
        heat_data.append(df.values.tolist())

    m = folium.Map(location=[0, 0], zoom_start=2)
    HeatMapWithTime(
        heat_data,
        index=date_cols.tolist(),
        radius=8,
        auto_play=False,
    ).add_to(m)
    m.save('covid_heatmap.html')
    print(
        f"Heatmap saved to covid_heatmap.html for dates {date_cols[0]} to {date_cols[-1]}."
    )

if __name__ == "__main__":
    main()
