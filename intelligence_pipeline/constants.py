import datetime
import os
from typing import Union

JSON_INDENT = 4

# Type hints
TIME = Union[int, float, str, datetime.date, datetime.datetime]

# Data directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_LAYER_DIR = os.path.join(DATA_DIR, "layers/raw")
PROCESSED_LAYER_DIR = os.path.join(DATA_DIR, "layers/processed")
AGGREGATE_LAYER_DIR = os.path.join(DATA_DIR, "layers/aggregated")
EXAMPLE_LAYER_DIR = os.path.join(DATA_DIR, "layers/examples")

OASIS_CTI = "oasis-cti"
CISA_KEV = "cisa-kev"
EPSS = "epss"

# OASIS CTI
RAW_OASIS_CTI_URL = (
    "https://github.com/oasis-open/cti-stix-common-objects/tarball/master"
)
RAW_OASIS_CTI_PATH = os.path.join(
    RAW_LAYER_DIR, f"{OASIS_CTI}/cti-stix-common-objects.tar.gz"
)
RAW_OASIS_CTI_OBJECTS_DIR = os.path.join(RAW_LAYER_DIR, OASIS_CTI, "objects")
PROCESSED_OASIS_CTI_OBJECTS_PATH = os.path.join(
    PROCESSED_LAYER_DIR, OASIS_CTI, "stix2-objects.json"
)

# CISA Known Exploited Vulnerabilities (KEV) catalog
RAW_CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
RAW_CISA_KEV_PATH = os.path.join(
    RAW_LAYER_DIR, f"{CISA_KEV}/known_exploited_vulnerabilities.json"
)
PROCESSED_CISA_KEV_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{CISA_KEV}/known_exploited_vulnerabilities.parquet"
)

# Exploit Prediction Scoring System (EPSS)
EPSS_V1_RELEASE_DATE = "2021-04-14"
EPSS_V2_RELEASE_DATE = "2022-02-04"  # EPSS v2 (v2022.01.01)
EPSS_V3_RELEASE_DATE = "2023-03-07"  # EPSS v3 (v2023.03.01)

RAW_EPSS_DIR = os.path.join(RAW_LAYER_DIR, EPSS)
PROCESSED_EPSS_DIR = os.path.join(PROCESSED_LAYER_DIR, EPSS)
