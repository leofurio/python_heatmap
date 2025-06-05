# python_heatmap

Python Gmaps HEATMAP (Covid-19)

## Usage

This repository contains a simple script to generate a COVID-19 heatmap using
[Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) case
numbers.

The script downloads the latest confirmed case data and builds an interactive
heatmap saved as `covid_heatmap.html`.

```bash
pip install pandas folium
python covid_heatmap.py
```

Open the resulting `covid_heatmap.html` file in your browser to visualize the
cases.

### Jupyter Notebook

You can also run the notebook version in Jupyter:

```bash
pip install pandas folium jupyter
jupyter notebook covid_heatmap.ipynb
```

Executing all cells will display the map inline and save it to
`covid_heatmap.html`.
