import json

infile = open("eq_data_1_day_m1.json", "r")
outfile = open("readable_eq_data1.json", "w")

eq_data = json.load(infile)

json.dump(eq_data, outfile, indent=4)

# Type of object
print("The type of eq_data is: ", type(eq_data))

# Number of Earthquakes
list_of_eqs = eq_data["features"]
print(f"The number of earthquakes are {len(list_of_eqs)}")

mags, lons, lats = [], [], []

for eq in list_of_eqs:
    mag = eq["properties"]["mag"]
    mags.append(mag)

    lon = eq["geometry"]["coordinates"][0]
    lons.append(lon)

    lat = eq["geometry"]["coordinates"][1]
    lats.append(lat)

# print the first 10 elements
print(f"The first 10 Magnitudes are: {mags[:10]}")
print(f"The first 10 Longitudes are: {lons[:10]}")
print(f"The first 10 Latitudes are: {lats[:10]}")


# Plot the elemments
from plotly.graph_objects import Scattergeo, Layout
from plotly import offline

my_data = Scattergeo(lon=lons, lat=lats)
my_layout = Layout(title="Global Earthquakes")

fig = {"data": my_data, "layout": my_layout}

offline.plot(fig, filename="global_earthquakes1.html")
