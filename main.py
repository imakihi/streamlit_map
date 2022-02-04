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
                "ScatterplotLayer",
                data=data,
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                get_radius=10000,
                get_fill_color='[180, 0, 200, 140]',
                pickable=True
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
tokyo= [35.652832, 139.839478]
sapporo = [43.066666, 141.350006]
hakata = [33.604282, 130.397751]
zoom_level = 10
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

with row2_1:
    st.write("**マグニチュードの範囲 %i ~ %i**" % (mag_selected, 8))
    map(data, midpoint[0], midpoint[1], 8)

with row2_2:
    st.write("**東京**")
    map(data, tokyo[0],tokyo[1], zoom_level)

with row2_3:
    st.write("**札幌**")
    map(data, sapporo[0],sapporo[1], zoom_level)

with row2_4:
    st.write("**博多**")
    map(data, hakata[0],hakata[1], zoom_level)

# FILTERING DATA FOR THE HISTOGRAM
filtered = data[data['mag'] >= mag_selected]

hist = np.histogram(filtered['mag'], bins=8)[0]

chart_data = pd.DataFrame({"マグニチュード": range(1,9), "頻度": hist})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**マグニチュードの範囲 %i ~ %i**" % (mag_selected,8))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("マグニチュード:Q", scale=alt.Scale(nice=True)),
        y=alt.Y("頻度:Q"),
        tooltip=["マグニチュード","頻度"]
    ).configure_mark(
        opacity=0.2,
        color='red'
    ), use_container_width=True)