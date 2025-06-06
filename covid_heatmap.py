"""Generate an interactive COVID-19 bubble map using Folium."""

from __future__ import annotations

import argparse
from math import sqrt
import json

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
    table_data: dict[str, list[dict[str, float | int]]] = {iso: [] for iso in iso_dates}

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
            table_data[iso].append({"Lat": float(lat), "Long": float(lon), "Cases": int(count)})

    b = folium.Map(location=[0, 0], zoom_start=2, width="80%", height="60%")
    TimestampedGeoJson(
        {"type": "FeatureCollection", "features": features},
        period="P1D",
        add_last_point=False,
        auto_play=False,
    ).add_to(b)

    table_json = json.dumps(table_data)
    options = "".join(f'<option value="{d}">{d}</option>' for d in iso_dates)
    table_html = f"""
    <div id=\"table-container\">
      <label for=\"date-select\">Date:</label>
      <select id=\"date-select\">{options}</select>
      <table id=\"data-table\">
        <thead><tr><th>Latitude</th><th>Longitude</th><th>Cases</th></tr></thead>
        <tbody id=\"data-tbody\"></tbody>
      </table>
    </div>
    <style>
    #table-container {{width:80%;margin:20px auto;}}
    #data-table {{width:100%;border-collapse:collapse;}}
    #data-table th,#data-table td {{border:1px solid #ccc;padding:4px;text-align:right;}}
    #data-table th {{background-color:#f0f0f0;}}
    </style>
    <script>
    var tableData = {table_json};
    var select = document.getElementById('date-select');
    function render(date) {{
      var body = document.getElementById('data-tbody');
      body.innerHTML = '';
      (tableData[date] || []).forEach(function(row) {{
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>'+row.Lat+'</td><td>'+row.Long+'</td><td>'+row.Cases+'</td>';
        body.appendChild(tr);
      }});
    }}
    select.addEventListener('change', function() {{render(this.value);}});
    render(select.value);
    </script>
    """
    b.get_root().html.add_child(folium.Element(table_html))

    b.save("covid_dashboard.html")
    print(
        f"Dashboard saved to covid_dashboard.html for dates {date_cols[0]} to {date_cols[-1]}."
    )


if __name__ == "__main__":
    main()
