# python_heatmap

Python Gmaps Bubble Map (Covid-19)

## Usage

This repository contains a simple script to generate a COVID-19 bubble map using
[Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) case
numbers.

The script downloads the confirmed case data and builds an interactive
bubble map saved as `covid_dashboard.html`. A date slider lets you explore the
spread of cases from the earliest available date to the most recent one. The
page also includes a dynamic table that updates to show case counts for the
selected date.

```bash
pip install pandas folium
python covid_heatmap.py --last-days 30 --scale 150
```
The optional flags let you limit the number of days displayed and control
bubble size. Increase `--scale` for smaller bubbles.

Open the resulting `covid_dashboard.html` file in your browser to visualize the
cases and browse the table.

### Jupyter Notebook

You can also run the notebook version in Jupyter:

```bash
pip install pandas folium jupyter
jupyter notebook covid_heatmap.ipynb
```

Executing all cells will display the map inline and save it to
`covid_dashboard.html`.
