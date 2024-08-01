import os
from dagster import asset
from intelligence_pipeline.constants import (
    JSON_INDENT,
    PROCESSED_CISA_KEV_PATH,
    RAW_CISA_KEV_PATH,
    CISA_KEV_URL,
)
from intelligence_pipeline import util
import polars as pl
import requests
import json


@asset
def download_raw_cisa_kev_file() -> None:
    """
    CISA KEV (JSON).
    """
    response = requests.get(CISA_KEV_URL, verify=False)
    response.raise_for_status()

    output_dir = os.path.dirname(RAW_CISA_KEV_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(RAW_CISA_KEV_PATH, "w") as fp:
        json.dump(response.json(), fp=fp, sort_keys=True, indent=JSON_INDENT)


@asset(deps=[download_raw_cisa_kev_file])
def process_raw_cisa_kev_file() -> None:
    """
    CISA KEV (Parquet).
    """
    output_dir = os.path.dirname(PROCESSED_CISA_KEV_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(RAW_CISA_KEV_PATH) as fp:
        data = json.load(fp)["vulnerabilities"]
        rows = [parse_vulnerability(o) for o in data]

        df = pl.DataFrame(rows)
        df.write_parquet(PROCESSED_CISA_KEV_PATH)


def parse_vulnerability(o: dict) -> dict:
    return {
        "cve_id": o["cveID"],
        "vendor": o["vendorProject"],
        "product": o["product"],
        "name": o["vulnerabilityName"],
        "description": o["shortDescription"],
        "date_added": util.parse_date(o["dateAdded"]),
        "due_date": util.parse_date(o["dueDate"]),
        "required_action": o["requiredAction"],
        "known_ransomware_campaign_use": o["knownRansomwareCampaignUse"] == "Known",
        "notes": o["notes"],
    }
