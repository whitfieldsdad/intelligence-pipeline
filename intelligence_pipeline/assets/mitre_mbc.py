import os
from dagster import asset
from intelligence_pipeline import util
from intelligence_pipeline.constants import (
    PROCESSED_MITRE_MBC_PATH,
    RAW_MITRE_MBC_PATH,
    MITRE_MBC_URL,
)


@asset
def download_mitre_mbc() -> None:
    """
    MITRE MBC (STIX 2.1).
    """
    output_dir = os.path.dirname(RAW_MITRE_MBC_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    util.download_file(
        url=MITRE_MBC_URL,
        path=RAW_MITRE_MBC_PATH,
    )


@asset(deps=[download_mitre_mbc])
def process_mitre_mbc() -> None:
    """
    MITRE MBC (STIX 2.1) with revoked and deprecated objects removed.
    """
    util.read_repack_and_write_stix2_objects(
        input_path=RAW_MITRE_MBC_PATH,
        output_path=PROCESSED_MITRE_MBC_PATH,
        include_revoked_objects=False,
        include_deprecated_objects=False,
    )