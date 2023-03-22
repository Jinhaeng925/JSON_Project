import json

# Plot the elemments
from plotly.graph_objects import Scattergeo, Layout
from plotly import offline

infile = open("schoolsgeo.json", "r")
sg_data = json.load(infile)

infile = open("univ.json", "r")
u_data = json.load(infile)

lons, lats, hover_text, tEnroll = [], [], [], []

# Big 12 Code
b12_code = 108

# Create a dictionary of Big 12 schools
big12_schools = {}
outfile = open("readable_big12_schools.json", "w")

# Input data from univ_data into the big 12 dictionary
for inst in u_data:
    if inst["NCAA"]["NAIA conference number football (IC2020)"] == b12_code:
        univInfo = {
            "address": "",
            "lat": "",
            "lon": "",
            "totalEnroll": inst["Total  enrollment (DRVEF2020)"],
            "malePop": int(
                round(
                    inst["Total  enrollment (DRVEF2020)"]
                    - inst["Total  enrollment (DRVEF2020)"]
                    * (
                        inst["Percent of total enrollment that are women (DRVEF2020)"]
                        / 100
                    ),
                    0,
                )
            ),
            "femalePop": int(
                round(
                    inst["Total  enrollment (DRVEF2020)"]
                    * (
                        inst["Percent of total enrollment that are women (DRVEF2020)"]
                        / 100
                    ),
                    0,
                )
            ),
        }
        big12_schools[inst["instnm"]] = univInfo

# Input data from sg_data into the big 12 dictionary
for s in big12_schools:
    for school in sg_data["features"]:
        if school["properties"]["NAME"] == s:
            addressInfo = (
                school["properties"]["STREET"]
                + " "
                + school["properties"]["CITY"]
                + " "
                + school["properties"]["STATE"]
                + " "
                + school["properties"]["ZIP"]
            )
            latInfo = school["properties"]["LAT"]
            lonInfo = school["properties"]["LON"]
            big12_schools[s]["address"] = addressInfo
            big12_schools[s]["lat"] = latInfo
            big12_schools[s]["lon"] = lonInfo


json.dump(big12_schools, outfile, indent=4)

for school, info in big12_schools.items():
    description = (
        "<b>"
        + school
        + "</b><br>"
        + info["address"]
        + "<br>"
        + "Total Enrollment: "
        + str(info["totalEnroll"])
        + "<br>"
        + "Male: "
        + str(info["malePop"])
        + "<br>"
        + "Female: "
        + str(info["femalePop"])
    )

    totEnroll = info["totalEnroll"]
    lon = info["lon"]
    lat = info["lat"]

    hover_text.append(description)
    tEnroll.append(totEnroll)
    lons.append(lon)
    lats.append(lat)

# Big 12 Data
b12_data = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_text,
        "marker": {
            "size": [float(te) / 1000 for te in tEnroll],
            "color": tEnroll,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Total Enrollment"},
        },
        "hoverinfo": "text",  # hide longitude and latitude values
    }
]

my_layout = Layout(
    title="Big 12 Schools",
    geo=dict(
        scope="usa",
        projection=dict(type="albers usa"),
        showland=True,
        landcolor="rgb(250, 250, 250)",
        subunitcolor="rgb(217, 217, 217)",
        countrycolor="rgb(217, 217, 217)",
        countrywidth=0.5,
        subunitwidth=0.5,
    ),
)

fig = {"data": b12_data, "layout": my_layout}

offline.plot(fig, filename="Big 12 Schools in the US.html")
