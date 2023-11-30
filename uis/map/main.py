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

analytics_tables = {
    "Water extent": "table_water_extent",
    "DOC": "table_doc_Ha",
    "Turbidity": "table_turbidity_Ha",
    "Chlorophyll": "table_chlorophyll_Ha",
}

analytics_tiffs = {
    "Water extent": "median_water_mask",
    "DOC": "DOC_masked",
    "Turbidity": "ndti_masked",
    "Chlorophyll": "ndci_masked",
}


@st.cache_data(ttl=10)
def get_data(analytics_file: str):
    """
    Get vegetation analytics data

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with vegetation analytics data
    """
    api_url = analytics_url
    analytics = requests.get(f"{api_url}/{analytics_file}", timeout=10).json()
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


st.set_page_config(page_title="Water quality monitoring Pulse", page_icon="💧")

centroid = get_aoi_centroid()

# AWS Open Data Terrain Tiles
TERRAIN_IMAGE = (
    "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
)

# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}

base_df = get_data("table_water_extent")


def choose_variables():
    with st.sidebar:
        st.sidebar.markdown("### Select date and indicator")
        date = st.selectbox("Date", base_df.index)
        variable = st.selectbox(
            "Indicator", ["Water extent", "DOC", "Turbidity", "Chlorophyll"]
        )
        analytics_file = analytics_tables[variable]
        image_name = analytics_tiffs[variable]
        df = get_data(analytics_file)
    return df, image_name, date, variable


df, image_name, date, variable = choose_variables()

if variable in ("Turbidity", "Chlorophyll"):
    stretch = "-1,1"
    palette = "plasma"
elif variable == "DOC":
    stretch = "0,100"
    palette = "RdYlGn"
else:
    stretch = "0,1"
    palette = "Blues"


selected_layer = pdk.Layer(
    "TerrainLayer",
    texture=f"{xyz_url}/{image_name}_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette={palette}&stretch={stretch}",
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

st.title("Water quality Analytics")

for col in df.columns:
    if "Total" in col:
        df.drop(col, axis=1, inplace=True)
st.line_chart(df)  # TODO use altair
if st.checkbox("Show data"):
    st.write(df)
