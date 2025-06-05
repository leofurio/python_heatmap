"""Generate an interactive COVID-19 bubble map using Folium."""

from __future__ import annotations

import argparse
from math import sqrt

import folium
import pandas as pd
from folium.plugins import TimestampedGeoJson

URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_confirmed_global.csv"
)


def parse_args() -> argparse.Namespace:
    """Return command line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--last-days",
        type=int,
        default=30,
        help="Number of recent days to include in the map",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=100.0,
        help="Bubble size scale factor. Higher values yield smaller bubbles.",
    )
    parser.add_argument(
        "--min-cases",
        type=int,
        default=1,
        help="Minimum number of cases required to display a bubble",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(URL)

    date_cols = data.columns[4:]
    if args.last_days > 0:
        date_cols = date_cols[-args.last_days :]

    grouped = data.groupby(["Lat", "Long"])[date_cols].sum().reset_index()
    iso_dates = pd.to_datetime(date_cols).strftime("%Y-%m-%d")

    features = []
    for _, row in grouped.iterrows():
        lat = row["Lat"]
        lon = row["Long"]
        for date, iso in zip(date_cols, iso_dates):
            count = row[date]
            if count < args.min_cases:
                continue
            radius = max(2, sqrt(count) / args.scale)
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

    b = folium.Map(location=[0, 0], zoom_start=2, width="80%", height="60%")
    TimestampedGeoJson(
        {"type": "FeatureCollection", "features": features},
        period="P1D",
        add_last_point=False,
        auto_play=False,
    ).add_to(b)
    b.save("covid_bubble_map.html")
    print(
        f"Bubble map saved to covid_bubble_map.html for dates {date_cols[0]} to {date_cols[-1]}."
    )


if __name__ == "__main__":
    main()
