import glob
import os
import shutil
import tarfile
from dagster import asset
from intelligence_pipeline import util

import requests

from intelligence_pipeline.constants import (
    PROCESSED_OASIS_CTI_OBJECTS_PATH,
    RAW_OASIS_CTI_OBJECTS_DIR,
    RAW_OASIS_CTI_URL,
    RAW_OASIS_CTI_PATH,
)


@asset
def download_oasis_cti() -> None:
    """
    Download the latest version of the oasis-open/cti-stix-common-objects repository.
    """
    response = requests.head(RAW_OASIS_CTI_URL, allow_redirects=True, verify=False)
    response.raise_for_status()

    url = response.url
    response = requests.get(url, stream=True, verify=False)
    response.raise_for_status()

    with open(RAW_OASIS_CTI_PATH, "wb") as output_file:
        shutil.copyfileobj(response.raw, output_file)

    print("Downloaded oasis-open/cti-stix-common-objects repository.")


@asset(deps=[download_oasis_cti])
def unpack_oasis_cti_stix2_bundles() -> None:
    """
    Unpack STIX 2 objects from the oasis-open/cti-stix-common-objects repository.
    """
    input_path = RAW_OASIS_CTI_PATH
    output_dir = RAW_OASIS_CTI_OBJECTS_DIR

    # Extract everything in the */objects folder to the ouput directory.
    with tarfile.open(input_path, "r:gz") as f:
        root_dir = os.path.commonpath(f.getnames())
        f.extractall(output_dir, filter="data")

    old_dir = os.path.join(output_dir, root_dir, "objects")
    new_dir = os.path.join(output_dir, "objects")

    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.rename(old_dir, new_dir)

    # Remove the temporary directory created during extraction.
    shutil.rmtree(os.path.join(output_dir, root_dir))


@asset(deps=[unpack_oasis_cti_stix2_bundles])
def merge_oasis_cti_stix2_bundles() -> None:
    """
    Merge all STIX 2 objects from the oasis-open/cti-stix-common-objects repository into a single bundle.
    """
    input_files = glob.glob(os.path.join(RAW_OASIS_CTI_OBJECTS_DIR, "*", "*--*.json"))
    output_file = PROCESSED_OASIS_CTI_OBJECTS_PATH
    util.merge_stix2_bundles(input_files, output_file)
