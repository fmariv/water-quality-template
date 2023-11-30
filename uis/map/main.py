"""
Streamlit app to display vegetation analytics
"""
import os

import geopandas as gpd
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from spai.project import ProjectConfig

project = ProjectConfig()

base_url = "http://localhost"  # TODO control this with env vars
analytics_url = f'{base_url}:{project.api_port("analytics")}'
xyz_url = f'{base_url}:{project.api_port("xyz")}'


@st.cache_data(ttl=10)
def get_data():
    """
    Get vegetation analytics data

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with vegetation analytics data
    """
    api_url = analytics_url
    analytics = requests.get(api_url, timeout=10).json()
    analytics_df = pd.DataFrame(analytics)
    analytics_df.sort_index(inplace=True)
    return analytics_df


def get_aoi_centroid():
    """
    Get AOI centroid

    Returns
    -------
    centroid : tuple
        AOI centroid
    """
    aoi = project.aoi
    gdf = gpd.GeoDataFrame.from_features(aoi)
    centroid = gdf.geometry.centroid[0].x, gdf.geometry.centroid[0].y

    return centroid


st.set_page_config(page_title="Forest monitoring Pulse", page_icon="🌳")

df = get_data()
centroid = get_aoi_centroid()

# AWS Open Data Terrain Tiles
TERRAIN_IMAGE = (
    "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
)

# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}


def choose_variables():
    with st.sidebar:
        st.sidebar.markdown("### Select date and indicator")
        date = st.selectbox("Date", df.index)
        variable = st.selectbox("Indicator", ["Vegetation", "Quality"])
        variable = variable.lower()
    return date, variable


date, variable = choose_variables()

if variable == "quality":
    stretch = "0,3"
else:
    stretch = "0,1"


selected_layer = pdk.Layer(
    "TerrainLayer",
    texture=f"{xyz_url}/{variable}_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn&stretch={stretch}",
    elevation_decoder=ELEVATION_DECODER,
    elevation_data=TERRAIN_IMAGE,
)


view_state = pdk.ViewState(
    latitude=centroid[1], longitude=centroid[0], zoom=9, pitch=60
)

if selected_layer:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=selected_layer,
        )
    )
else:
    st.error("Please choose at least one date and indicator.")

st.title("Vegetation Analytics")

colors = ["#e41a1c", "#BFEAA2", "#E4EA20", "#245900"]

df_chart = df.drop(columns=["Total"])  # Remove Total column to not plot it
st.line_chart(df_chart, color=colors)  # TODO use altair
if st.checkbox("Show data"):
    st.write(df)
