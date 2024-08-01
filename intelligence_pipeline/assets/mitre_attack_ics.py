import os
from dagster import asset
from intelligence_pipeline import util
from intelligence_pipeline.constants import (
    PROCESSED_MITRE_ATTACK_ICS_PATH,
    RAW_MITRE_ATTACK_ICS_PATH,
    MITRE_ATTACK_ICS_URL,
)


@asset
def download_mitre_attack_ics() -> None:
    """
    MITRE ATT&CK ICS (STIX 2.1).
    """
    output_dir = os.path.dirname(RAW_MITRE_ATTACK_ICS_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    util.download_file(
        url=MITRE_ATTACK_ICS_URL,
        path=RAW_MITRE_ATTACK_ICS_PATH,
    )


@asset(deps=[download_mitre_attack_ics])
def process_mitre_attack_ics() -> None:
    """
    MITRE ATT&CK ICS (STIX 2.1) with revoked and deprecated objects removed.
    """
    util.read_repack_and_write_stix2_objects(
        input_path=RAW_MITRE_ATTACK_ICS_PATH,
        output_path=PROCESSED_MITRE_ATTACK_ICS_PATH,
        include_revoked_objects=False,
        include_deprecated_objects=False,
    )
