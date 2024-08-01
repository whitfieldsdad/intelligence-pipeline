import json
import os
from dagster import asset
from intelligence_pipeline import util
from intelligence_pipeline.assets.mitre_attack_enterprise import (
    process_mitre_attack_enterprise,
)
from intelligence_pipeline.assets.mitre_attack_ics import process_mitre_attack_ics
from intelligence_pipeline.assets.mitre_attack_mobile import process_mitre_attack_mobile
from intelligence_pipeline.assets.mitre_capec import process_mitre_capec
from intelligence_pipeline.assets.mitre_mbc import process_mitre_mbc
from intelligence_pipeline.assets.oasis import merge_oasis_cti_stix2_bundles
from intelligence_pipeline.constants import (
    PROCESSED_MITRE_ATTACK_ENTERPRISE_PATH,
    PROCESSED_MITRE_ATTACK_MOBILE_PATH,
    PROCESSED_MITRE_ATTACK_ICS_PATH,
    PROCESSED_MITRE_CAPEC_PATH,
    PROCESSED_MITRE_MBC_PATH,
    PROCESSED_OASIS_CTI_OBJECTS_PATH,
    PROCESSED_STIX2_CONTENT_PATH,
)


@asset(
    deps=[
        process_mitre_attack_enterprise,
        process_mitre_attack_mobile,
        process_mitre_attack_ics,
        process_mitre_capec,
        process_mitre_mbc,
        merge_oasis_cti_stix2_bundles,
    ]
)
def merge_stix2_bundles():
    """
    Merge all STIX 2 bundles into a single bundle.
    """
    input_paths = [
        PROCESSED_MITRE_ATTACK_ENTERPRISE_PATH,
        PROCESSED_MITRE_ATTACK_MOBILE_PATH,
        PROCESSED_MITRE_ATTACK_ICS_PATH,
        PROCESSED_MITRE_CAPEC_PATH,
        PROCESSED_MITRE_MBC_PATH,
        PROCESSED_OASIS_CTI_OBJECTS_PATH,
    ]
    objects = util.read_objects_from_stix2_bundles(input_paths)
    objects = util.filter_stix2_objects(
        objects,
        include_revoked_objects=False,
        include_deprecated_objects=False,
    )
    bundle = util.create_stix2_bundle(objects)

    output_dir = os.path.dirname(PROCESSED_STIX2_CONTENT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(PROCESSED_STIX2_CONTENT_PATH, "w") as fp:
        json.dump(bundle, fp, indent=util.JSON_INDENT)
