"""
Script to download satellite images 
"""
from datetime import datetime, timedelta

import geopandas as gpd
from dotenv import load_dotenv
from spai.data.satellite import download_satellite_image, explore_satellite_images
from spai.models import ProjectConfig
from spai.storage import Storage

load_dotenv()

storage = Storage("data")
project = ProjectConfig()


if __name__ == "__main__":
    # explore available images
    print("Looking for images in the last month")
    aoi = gpd.GeoDataFrame.from_features(project.aoi["features"])
    dates = project.dates
    images = explore_satellite_images(aoi, dates, cloud_cover=10)

    if len(images) == 0:
        raise ValueError("No images found")

    # download images and save locally
    sensor = "S2L2A"  # or 'S2L1C'
    print("Found", len(images), f"image{'s' if len(images) > 1 else ''}")
    for image in images:
        existing_images = storage.list(f"{sensor}*.tif")
        dates = [image.split("_")[1].split(".")[0] for image in existing_images]
        date = image["date"].split("T")[0]
        # check if image is already downloaded
        if date in dates or image in existing_images:
            continue
        print("Downloading new image:", date)
        path = download_satellite_image(storage, aoi, date, sensor)
        print("Image saved at", path)
