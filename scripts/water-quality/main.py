"""
Script to run the water quality monitoring pipeline
"""

from spai.analytics.water_quality import water_quality
from spai.storage import Storage
from spai.config import SPAIVars
from tqdm import tqdm

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    try:
        collection = "sentinel-2-l2a"
        images = storage.list(f"{collection}*.tif")
        aoi = vars["AOI"]

        if not images:
            raise ValueError(
                "No images found for the given AoI. The process will stop."
            )

        for image in tqdm(images, desc="Processing images..."):
            date = image.split("_")[1].split(".")[0]  # Extract date from image name
            water_quality(image, date, storage)
    except Exception as e:
        print(f"An error occurred: {e}. The process will stop.")
