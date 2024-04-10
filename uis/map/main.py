"""
Streamlit app to display vegetation analytics
"""

import os

import folium
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd
import requests
import streamlit as st
from spai.config import SPAIVars

from config import (
    ANALYTICS_URL,
    XYZ_URL,
    WATER_COLS,
    analytics_tables,
    MARKDOWN_DICT,
    COLORS_DICT,
)

vars = SPAIVars()


@st.cache_data(ttl=10)
def get_data(analytics_file: str):
    """
    Get water quality analytics data

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with water quality analytics data
    """
    api_url = ANALYTICS_URL
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
    aoi = vars["AOI"]
    gdf = gpd.GeoDataFrame.from_features(aoi)
    centroid = gdf.geometry.centroid[0].y, gdf.geometry.centroid[0].x

    return centroid


def choose_variables():
    """
    Choose date and indicator from the analytics tables and layers

    Returns
    -------
    date : str
        Date of the analytics
    variable : str
        Name of the analytics variable
    df : pandas.DataFrame
        Dataframe with the analytics data
    """
    base_df = get_data("table_water_extent")
    with st.sidebar:
        st.sidebar.markdown("### Select date and indicator")
        date = st.selectbox("Date", base_df.index)
        variable = st.selectbox(
            "Indicator", ["Water extent", "DOC", "Turbidity", "Chlorophyll"]
        )
        analytics_file = analytics_tables[variable]
        df = get_data(analytics_file)
        # Drop unused columns from Water extent table
        if variable == "Water extent":
            df = df[WATER_COLS]
    return date, variable, df


st.set_page_config(page_title="Water quality monitoring Pulse", page_icon="💧")

centroid = get_aoi_centroid()

date, variable, dataframe = choose_variables()

variables_url_dict = {
    "Water extent": f"{XYZ_URL}/water_mask_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=Blues&stretch=0,1",
    "DOC": f"{XYZ_URL}/DOC_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn_r&stretch=0,50",
    "Turbidity": f"{XYZ_URL}/ndti_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn&stretch=-1,1",
    "Chlorophyll": f"{XYZ_URL}/ndci_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn&stretch=-1,1",
}

# Create map with Folium
m = folium.Map(
    location=centroid,
    zoom_start=13,
    tiles="CartoDB Positron",
)
# Add the analytic layer to the map
raster = folium.raster_layers.TileLayer(
    tiles=variables_url_dict[variable],
    attr="Water Quality Pulse",
    name="Water",
    overlay=True,
    control=True,
    show=True,
)
raster.add_to(m)
folium_static(m)

st.title("Water quality Analytics")
st.markdown(MARKDOWN_DICT[variable])
st.line_chart(dataframe, color=COLORS_DICT[variable])
if st.checkbox("Show data"):
    st.write(dataframe)
