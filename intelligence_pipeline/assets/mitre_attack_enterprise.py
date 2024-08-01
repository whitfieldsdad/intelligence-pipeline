import os
from dagster import asset
from intelligence_pipeline import util
from intelligence_pipeline.constants import (
    MITRE_ATTACK_ENTERPRISE_URL,
    PROCESSED_MITRE_ATTACK_ENTERPRISE_PATH,
    RAW_MITRE_ATTACK_ENTERPRISE_PATH,
)


@asset
def download_mitre_attack_enterprise() -> None:
    """
    MITRE ATT&CK Enterprise (STIX 2.1).
    """
    output_dir = os.path.dirname(RAW_MITRE_ATTACK_ENTERPRISE_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    util.download_file(
        url=MITRE_ATTACK_ENTERPRISE_URL,
        path=RAW_MITRE_ATTACK_ENTERPRISE_PATH,
    )


@asset(deps=[download_mitre_attack_enterprise])
def process_mitre_attack_enterprise() -> None:
    """
    MITRE ATT&CK Enterprise (STIX 2.1) with revoked and deprecated objects removed.
    """
    util.read_repack_and_write_stix2_objects(
        input_path=RAW_MITRE_ATTACK_ENTERPRISE_PATH,
        output_path=PROCESSED_MITRE_ATTACK_ENTERPRISE_PATH,
        include_revoked_objects=False,
        include_deprecated_objects=False,
    )
