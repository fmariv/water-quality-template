"""
Script to download satellite images 
"""

import os

from spai.data.satellite import download_satellite_imagery, explore_satellite_imagery
from spai.storage import Storage
from spai.config import SPAIVars

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    # explore available images
    print("Looking for images in the last month")
    # aoi = gpd.GeoDataFrame.from_features(project.aoi["features"])
    aoi = vars["AOI"]
    dates = vars["DATES"]
    images = explore_satellite_imagery(aoi, dates)

    if len(images) == 0:
        raise ValueError("No images found")

    # download images and save locally
    collection = "sentinel-2-l2a"
    print("Found", len(images), f"image{'s' if len(images) > 1 else ''}")
    for image in images:
        existing_images = storage.list(f"{collection}*.tif")
        dates = [image.split("_")[1].split(".")[0] for image in existing_images]
        date = image["datetime"].split("T")[0]
        # check if image is already downloaded
        if date in dates or image in existing_images:
            continue
        print("Downloading new image:", date)
        path = download_satellite_imagery(storage, aoi, date, collection)
        print("Image saved at", path)
