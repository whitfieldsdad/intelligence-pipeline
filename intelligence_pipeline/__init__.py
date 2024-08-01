from dagster import Definitions, load_assets_from_modules
from intelligence_pipeline.assets import cisa_kev, epss, oasis

import urllib3

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

all_assets = load_assets_from_modules([cisa_kev, epss, oasis])

defs = Definitions(
    assets=all_assets,
)
