from dagster import Definitions, load_assets_from_modules
from intelligence_pipeline.assets import (
    cisa_kev,
    epss,
    oasis,
    mitre_attack_enterprise,
    mitre_attack_mobile,
    mitre_attack_ics,
    mitre_capec,
    mitre_mbc,
    stix2,
)

import urllib3

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

all_assets = load_assets_from_modules(
    [
        cisa_kev,
        epss,
        oasis,
        mitre_attack_enterprise,
        mitre_attack_mobile,
        mitre_attack_ics,
        mitre_capec,
        mitre_mbc,
        stix2,
    ]
)

defs = Definitions(
    assets=all_assets,
)
