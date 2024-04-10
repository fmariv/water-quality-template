"""
Script to run the water quality monitoring pipeline
"""

from spai.analytics import water_quality
from spai.storage import Storage
from spai.config import SPAIVars
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    collection = "sentinel-2-l2a"
    images = storage.list(f"{collection}*.tif")
    aoi = vars["AOI"]
    for image in tqdm(images, desc="Processing images..."):
        water_quality(image, aoi, storage)
