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

MITRE_ATTACK_ENTERPRISE = "mitre-attack-enterprise"
MITRE_ATTACK_MOBILE = "mitre-attack-mobile"
MITRE_ATTACK_ICS = "mitre-attack-ics"
MITRE_CAPEC = "mitre-capec"
MITRE_MBC = "mitre-mbc"
OASIS_CTI = "oasis-cti"
CISA_KEV = "cisa-kev"
EPSS = "epss"

# MITRE ATT&CK
MITRE_ATTACK_ENTERPRISE_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
MITRE_ATTACK_MOBILE_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json"
MITRE_ATTACK_ICS_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json"

RAW_MITRE_ATTACK_ENTERPRISE_PATH = os.path.join(
    RAW_LAYER_DIR, f"{MITRE_ATTACK_ENTERPRISE}/stix2-objects.json"
)
RAW_MITRE_ATTACK_MOBILE_PATH = os.path.join(
    RAW_LAYER_DIR, f"{MITRE_ATTACK_MOBILE}/stix2-objects.json"
)
RAW_MITRE_ATTACK_ICS_PATH = os.path.join(
    RAW_LAYER_DIR, f"{MITRE_ATTACK_ICS}/stix2-objects.json"
)

PROCESSED_MITRE_ATTACK_ENTERPRISE_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{MITRE_ATTACK_ENTERPRISE}/stix2-objects.json"
)
PROCESSED_MITRE_ATTACK_MOBILE_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{MITRE_ATTACK_MOBILE}/stix2-objects.json"
)
PROCESSED_MITRE_ATTACK_ICS_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{MITRE_ATTACK_ICS}/stix2-objects.json"
)

# MITRE CAPEC
MITRE_CAPEC_URL = (
    "https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json"
)
RAW_MITRE_CAPEC_PATH = os.path.join(RAW_LAYER_DIR, f"{MITRE_CAPEC}/stix2-objects.json")
PROCESSED_MITRE_CAPEC_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{MITRE_CAPEC}/stix2-objects.json"
)

# MITRE MBC
MITRE_MBC_URL = (
    "https://raw.githubusercontent.com/MBCProject/mbc-stix2.1/main/mbc/mbc.json"
)
RAW_MITRE_MBC_PATH = os.path.join(RAW_LAYER_DIR, f"{MITRE_MBC}/stix2-objects.json")
PROCESSED_MITRE_MBC_PATH = os.path.join(
    PROCESSED_LAYER_DIR, f"{MITRE_MBC}/stix2-objects.json"
)

# OASIS CTI
OASIS_CTI_URL = "https://github.com/oasis-open/cti-stix-common-objects/tarball/master"
RAW_OASIS_CTI_PATH = os.path.join(
    RAW_LAYER_DIR, f"{OASIS_CTI}/cti-stix-common-objects.tar.gz"
)
RAW_OASIS_CTI_OBJECTS_DIR = os.path.join(RAW_LAYER_DIR, OASIS_CTI, "objects")
PROCESSED_OASIS_CTI_OBJECTS_PATH = os.path.join(
    PROCESSED_LAYER_DIR, OASIS_CTI, "stix2-objects.json"
)

# STIX 2
PROCESSED_STIX2_CONTENT_DIR = os.path.join(PROCESSED_LAYER_DIR, "stix2")
PROCESSED_STIX2_CONTENT_PATH = os.path.join(
    PROCESSED_STIX2_CONTENT_DIR, "stix2-objects.json"
)

# CISA Known Exploited Vulnerabilities (KEV) catalog
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
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
