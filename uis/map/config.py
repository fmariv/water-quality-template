"""
UI constants
"""

import os
from spai.config import SPAIVars

vars = SPAIVars()

ANALYTICS_URL = f'http://{os.getenv("ANALYTICS_URL")}'
XYZ_URL = f'http://{os.getenv("XYZ_URL")}'

WATER_COLS = ["Water [Has]", "Not Water [Has]", "Percentage [%]"]

analytics_tables = {
    "Water extent": "table_water_extent",
    "DOC": "table_DOC_percent",
    "Turbidity": "table_turbidity_percent",
    "Chlorophyll": "table_chlorophyll_percent",
}

WATER_MARKDOWN = """
### Water extent

The water extent is calculated using the [NDWI](https://en.wikipedia.org/wiki/Normalized_difference_water_index) index. The percentage of water extent is calculated using as reference the image with the highest water extent.
"""

DOC_MARKDOWN = """
### Dissolved organic carbon

Dissolved Organic Carbon (DOC) in water refers to the fraction of total organic carbon that is dissolved in water.. The categories N0, N1, N2 and N3 indicate the difference between the DOC value in each pixel with respect to the average DOC of the body of water over time.
"""

TURBIDITY_MARKDOWN = """
### Turbidity

Turbidity is the cloudiness or haziness of a fluid caused by large numbers of individual particles that are generally invisible to the naked eye, similar to smoke in air. It is calculated using the [NDTI](https://linkinghub.elsevier.com/retrieve/pii/S0034425706002811) index. The categories have been calculated taking into account the thresholds defined in the scientific literature.
"""

CHLOROPHYLL_MARKDOWN = """
### Chlorophyll

Chlorophyll is a green pigment found in cyanobacteria and the chloroplasts of algae and plants. It is an extremely important biomolecule, critical in photosynthesis, which allows plants to absorb energy from light. It is calculated using the [NDCI](https://linkinghub.elsevier.com/retrieve/pii/S0034425711003737) index. The categories have been calculated taking into account the thresholds defined in the scientific literature.
"""

MARKDOWN_DICT = {
    "Water extent": WATER_MARKDOWN,
    "DOC": DOC_MARKDOWN,
    "Turbidity": TURBIDITY_MARKDOWN,
    "Chlorophyll": CHLOROPHYLL_MARKDOWN,
}

COLORS_DICT = {
    "Water extent": ["#D80707", "#01438E", "#00D4FF"],
    "DOC": ["#FF0000", "#CDFF00", "#01CA13"],
    "Turbidity": ["#FF0000", "#CDFF00", "#01CA13"],
    "Chlorophyll": ["#FF0000", "#CDFF00", "#01CA13"],
}
