"""
Script to download satellite images and run the water quality monitoring pipeline
"""

from spai.data.satellite import download_satellite_imagery, explore_satellite_imagery
from spai.analytics.water_quality import water_quality
from spai.storage import Storage
from spai.config import SPAIVars
from spai.logging import log
from spai.logging.log import Result
from tqdm import tqdm

storage = Storage()["data"]
vars = SPAIVars()


def _read_table(table_name):
    if table_name not in storage.list():
        return None
    df = storage.read(table_name)
    if hasattr(df.index, "strftime"):
        df.index = df.index.strftime("%Y-%m-%d")
    return df.loc[[d for d in dates_in_run if d in df.index]]

def _avg(df, col):
    if df is None or col not in df.columns:
        return None
    return round(float(df[col].mean()), 2)



if __name__ == "__main__":

    cloud_cover = 10

    log.log_inputs(
        {
            "aoi": vars["AOI"],
            "dates": vars["DATES"],
            "cloud_cover": cloud_cover,
            "collection": "sentinel-2-l2a"
    })
    
    
    try:
        # explore available images
        print("Looking for images in the last month")
        aoi = vars["AOI"]
        dates = vars["DATES"]
        images = explore_satellite_imagery(aoi, dates, cloud_cover=cloud_cover)

        if not images:
            raise ValueError(f"No images found for the given datetime: {dates}")

        # download images and save locally
        collection = "sentinel-2-l2a"
        print("Found", len(images), f"image{'s' if len(images) > 1 else ''}")
        for image in tqdm(images, desc="Downloading images..."):
            existing_images = storage.list(f"{collection}*.tif")
            dates = [image.split("_")[1].split(".")[0] for image in existing_images]
            date = image["datetime"].split("T")[0]
            # check if image is already downloaded
            if date in dates or image in existing_images:
                continue
            print("Downloading new image:", date)
            path = download_satellite_imagery(storage, aoi, date, collection)
            print("Image saved at", path)

        # Process and run the water quality monitoring pipeline
        collection = "sentinel-2-l2a"
        downloaded_images = storage.list(f"{collection}*.tif")

        dates_in_run = [img.split("_")[1].split(".")[0] for img in downloaded_images]
        for downloaded_image in tqdm(downloaded_images, desc="Processing images..."):
            date = downloaded_image.split("_")[1].split(".")[0]
            water_quality(downloaded_image, date, storage)

        extent_df = _read_table("table_water_extent.json")
        turbidity_df = _read_table("table_turbidity_percent.json")
        chlorophyll_df = _read_table("table_chlorophyll_percent.json")
        doc_df = _read_table("table_DOC_percent.json")

        log.log_results([
            Result("water_extent",        _avg(extent_df,      "Water [Has]"),    "ha"),
            Result("turbidity_bad",       _avg(turbidity_df,   "Bad [%]"),        "%"),
            Result("chlorophyll_bad",     _avg(chlorophyll_df, "Bad [%]"),        "%"),
            Result("doc_bad",             _avg(doc_df,         "Bad [%]"),        "%"),
            Result("turbidity_careful",   _avg(turbidity_df,   "Careful [%]"),    "%"),
            Result("chlorophyll_careful", _avg(chlorophyll_df, "Careful [%]"),    "%"),
            Result("doc_careful",         _avg(doc_df,         "Careful [%]"),    "%"),
            Result("images_processed",    len(dates_in_run),                      "images"),
        ])
    except Exception as e:
        print("An error occurred:", e)
