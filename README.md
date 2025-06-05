# python_heatmap

Python Gmaps Bubble Map (Covid-19)

## Usage

This repository contains a simple script to generate a COVID-19 bubble map using
[Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) case
numbers.

The script downloads the confirmed case data and builds an interactive
bubble map saved as `covid_bubble_map.html`. A date slider lets you explore the
spread of cases from the earliest available date to the most recent one.

```bash
pip install pandas folium
python covid_heatmap.py
```

Open the resulting `covid_bubble_map.html` file in your browser to visualize the
cases.

### Jupyter Notebook

You can also run the notebook version in Jupyter:

```bash
pip install pandas folium jupyter
jupyter notebook covid_heatmap.ipynb
```

Executing all cells will display the map inline and save it to
`covid_bubble_map.html`.
