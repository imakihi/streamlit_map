# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "time"

@st.experimental_memo
def load_data():
    data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')
    data = data[['time','latitude','longitude','depth','mag']]
    data = data.dropna()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data()

# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["longitude", "latitude"],
                radius=100,
                elevation_scale=4000,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("USGS地震データ")
    mag_selected = st.slider("マグニチュードを選んでください", 0, 8)

with row1_2:
    st.write(
    """
    ##
    スライドバーで、表示するマグニチュードの最低値を絞り込めます。
    """)



# FILTERING DATA BY HOUR SELECTED
data = data[data['mag'] >= mag_selected]

# show data as a table
st.dataframe(data.style.highlight_max(axis=0))

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
la_guardia= [40.7900, -73.8700]
jfk = [40.6650, -73.7821]
newark = [40.7090, -74.1805]
zoom_level = 12
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

with row2_1:
    st.write("**All New York City from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data, midpoint[0], midpoint[1], zoom_level)

with row2_2:
    st.write("**La Guardia Airport**")
    map(data, la_guardia[0],la_guardia[1], zoom_level)

with row2_3:
    st.write("**JFK Airport**")
    map(data, jfk[0],jfk[1], zoom_level)

with row2_4:
    st.write("**Newark Airport**")
    map(data, newark[0],newark[1], zoom_level)

# # FILTERING DATA FOR THE HISTOGRAM
# filtered = data[
#     (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
#     ]

# hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

# chart_data = pd.DataFrame({"minute": range(60), "mag": hist})

# # LAYING OUT THE HISTOGRAM SECTION

# st.write("")

# st.write("**Breakdown of earthquake per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

# st.altair_chart(alt.Chart(chart_data)
#     .mark_area(
#         interpolate='step-after',
#     ).encode(
#         x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
#         y=alt.Y("pickups:Q"),
#         tooltip=['depth', 'mag']
#     ).configure_mark(
#         opacity=0.2,
#         color='red'
#     ), use_container_width=True)