import json

infile = open("eq_data_30_day_m1.json", "r")
outfile = open("readable_eq_data2.json", "w")

eq_data = json.load(infile)

json.dump(eq_data, outfile, indent=4)

# Type of object
print("The type of eq_data is: ", type(eq_data))

# Number of Earthquakes
list_of_eqs = eq_data["features"]
print(f"The number of earthquakes are {len(list_of_eqs)}")

mags, lons, lats, hover_text = [], [], [], []

for eq in list_of_eqs:
    mag = eq["properties"]["mag"]
    if mag > 5:
        lon = eq["geometry"]["coordinates"][0]
        lat = eq["geometry"]["coordinates"][1]
        title = eq["properties"]["title"]

        mags.append(mag)
        lons.append(lon)
        lats.append(lat)
        hover_text.append(title)

# print the first 10 elements
print(f"The first 10 Magnitudes are: {mags[:10]}")
print(f"The first 10 Longitudes are: {lons[:10]}")
print(f"The first 10 Latitudes are: {lats[:10]}")


# Plot the elemments
from plotly.graph_objects import Scattergeo, Layout
from plotly import offline

# my_data = Scattergeo(lon=lons, lat=lats)

my_data = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_text,
        "marker": {
            "size": [5 * mag for mag in mags],
            "color": mags,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Magnitude"},
        },
    }
]

my_layout = Layout(title="Global Earthquakes")

fig = {"data": my_data, "layout": my_layout}

offline.plot(fig, filename="global_earthquakes2.html")
