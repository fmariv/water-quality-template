"""
Script to download satellite images and run the water quality monitoring pipeline
"""

from spai.data.satellite import download_satellite_imagery, explore_satellite_imagery
from spai.analytics.water_quality import water_quality
from spai.storage import Storage
from spai.config import SPAIVars
from spai.logging import log
from tqdm import tqdm

storage = Storage()["data"]
vars = SPAIVars()


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

        def _read_rows(table_name):
            if table_name not in storage.list():
                return {}
            df = storage.read(table_name)
            if hasattr(df.index, "strftime"):
                df.index = df.index.strftime("%Y-%m-%d")
            return {d: df.loc[d].round(2).to_dict() for d in dates_in_run if d in df.index}

        log.log_results({
            "images_processed": len(dates_in_run),
            "dates_processed": dates_in_run,
            "water_extent_ha": _read_rows("table_water_extent.json"),
            "turbidity_pct": _read_rows("table_turbidity_percent.json"),
            "chlorophyll_pct": _read_rows("table_chlorophyll_percent.json"),
            "doc_pct": _read_rows("table_DOC_percent.json"),
        })
    except Exception as e:
        print(f"An error occurred: {e}. The process will stop.")
