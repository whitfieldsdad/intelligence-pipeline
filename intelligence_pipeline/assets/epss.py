import datetime
import gzip
import io
import re
from typing import Optional
from dagster import asset
import requests
from intelligence_pipeline.constants import (
    EPSS_V3_RELEASE_DATE,
    PROCESSED_EPSS_DIR,
    TIME,
    RAW_EPSS_DIR,
)
from intelligence_pipeline import util
import pandas as pd
import concurrent.futures

import glob
import os
import logging

logger = logging.getLogger(__name__)


@asset
def download_raw_epss_files() -> None:
    """
    EPSS v3 (v2023.03.01) scores (CSV.GZ).
    """
    if not os.path.exists(RAW_EPSS_DIR):
        os.makedirs(RAW_EPSS_DIR, exist_ok=True)

    downloads = {}
    dates = util.iter_dates_in_range(
        min_date=EPSS_V3_RELEASE_DATE, max_date=get_max_publication_date()
    )
    for date in dates:
        url = get_download_url_by_date(date)
        filename = os.path.basename(url)
        path = os.path.join(RAW_EPSS_DIR, filename)
        if not os.path.exists(path):
            downloads[path] = url

    if downloads:
        util.download_files(downloads)


@asset(deps=[download_raw_epss_files])
def process_raw_epss_files():
    """
    EPSS v3 (v2023.03.01) scores (Parquet).
    """
    if not os.path.exists(PROCESSED_EPSS_DIR):
        os.makedirs(PROCESSED_EPSS_DIR, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for old_path in glob.glob(os.path.join(RAW_EPSS_DIR, "*.csv.gz")):
            filename = os.path.basename(old_path.replace(".csv.gz", ".parquet"))
            new_path = os.path.join(PROCESSED_EPSS_DIR, filename)
            if not os.path.exists(new_path):
                future = executor.submit(process_file, old_path, new_path)
                futures[future] = (old_path, new_path)

        if futures:
            for future in concurrent.futures.as_completed(futures):
                old_path, new_path = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Failed to process {old_path} - {e}")


def process_file(old_path: str, new_path: str) -> None:
    df = parse_raw_file(old_path)
    df.to_parquet(new_path, index=False)


def parse_raw_file(path: str) -> pd.DataFrame:
    with gzip.open(path, "rb") as fp:
        first_line = fp.readline()
        if first_line.startswith(b"#"):
            skiprows = 1
        else:
            skiprows = 0

    df = pd.read_csv(path, compression="gzip", skiprows=skiprows)

    # Insert `date` column if missing.
    if "date" not in df.columns:
        date = util.extract_date_from_filename(os.path.basename(path))
        assert date is not None, f"Failed to extract date from {path}"
        df["date"] = date

    # Cast `date` column to datetime.
    df["date"] = pd.to_datetime(df["date"])

    return df


def download_epss_scores_by_date(date: TIME, path: str) -> None:
    date = util.parse_date(date)
    url = get_download_url_by_date(date)

    response = requests.get(url, verify=False, stream=True)
    response.raise_for_status()

    data = io.BytesIO(response.content)
    if date <= util.parse_date("2022-01-01"):
        skip_rows = 0
    else:
        skip_rows = 1

    df = pd.read_csv(data, compression="gzip", skiprows=skip_rows)
    df["date"] = date.isoformat()
    df.to_csv(path, compression="gzip", index=False)


def get_download_url_by_date(date: Optional[TIME] = None) -> str:
    date = util.parse_date(date) if date else get_max_publication_date()
    return f"https://epss.cyentia.com/epss_scores-{date.isoformat()}.csv.gz"


def get_max_publication_date() -> datetime.date:
    url = "https://epss.cyentia.com/epss_scores-current.csv.gz"

    response = requests.head(url, verify=False)
    location = response.headers["Location"]
    assert location is not None, "No Location header found"
    regex = r"(\d{4}-\d{2}-\d{2})"
    match = re.search(regex, location)
    assert match is not None, f"No date found in {location}"
    date = datetime.date.fromisoformat(match.group(1))
    return date
