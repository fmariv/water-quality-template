"""
Script to run the water quality monitoring pipeline
"""
from spai.project import ProjectConfig
from spai.pulses import water_quality
from spai.storage import Storage
from tqdm import tqdm

storage = Storage("data")

project = ProjectConfig()


if __name__ == "__main__":
    sensor = "S2L2A"  # or 'S2L1C'
    images = storage.list(f"{sensor}*.tif")
    aoi = project.aoi
    for image in tqdm(images, desc="Processing images..."):
        water_quality(image, aoi, storage)
