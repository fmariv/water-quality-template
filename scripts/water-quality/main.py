"""
Script to run the water quality monitoring pipeline
"""

from spai.pulses import water_quality
from spai.storage import Storage
from spai.config import SPAIVars
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    sensor = "S2L2A"  # or 'S2L1C'
    images = storage.list(f"{sensor}*.tif")
    aoi = vars["AOI"]
    for image in tqdm(images, desc="Processing images..."):
        water_quality(image, aoi, storage)
