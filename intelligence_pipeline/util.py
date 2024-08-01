import datetime
import itertools
import json
import re
from typing import Dict, Iterable, Iterator, Optional
import uuid

from intelligence_pipeline.constants import JSON_INDENT, TIME
import concurrent.futures
import requests
import os


def merge_stix2_bundles(
    input_files: Iterable[str], output_file: str, indent: int = JSON_INDENT
) -> None:
    objects = read_objects_from_stix2_bundles(paths=input_files)
    bundle = {
        "id": f"bundle--{uuid.uuid4()}",
        "type": "bundle",
        "spec_version": "2.1",
        "objects": list(objects),
    }

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as fp:
        json.dump(bundle, fp, indent=indent)


def read_objects_from_stix2_bundles(paths: Iterable[str]) -> Iterator[dict]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        yield from itertools.chain.from_iterable(
            executor.map(read_objects_from_stix2_bundle, paths)
        )


def read_objects_from_stix2_bundle(path: str) -> Iterator[dict]:
    with open(path) as file:
        bundle = json.load(file)
        yield from bundle["objects"]


def download_files(downloads: Dict[str, str]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for path, url in downloads.items():
            if not os.path.exists(path):
                future = executor.submit(download_file, url=url, path=path)
                futures[future] = (url, path)

        if futures:
            for future in concurrent.futures.as_completed(futures):
                url, path = futures[future]
                try:
                    future.result()
                except Exception as e:
                    raise RuntimeError(f"Failed to download {url} to {path}") from e


def download_file(url: str, path: str) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(path, "wb") as fp:
        fp.write(response.content)


def iter_dates_in_range(min_date: TIME, max_date: TIME) -> Iterator[datetime.date]:
    min_date = parse_date(min_date)
    max_date = parse_date(max_date)
    delta = max_date - min_date
    for i in range(delta.days + 1):
        day = min_date + datetime.timedelta(days=i)
        yield day


def parse_date(d: Optional[TIME]) -> Optional[datetime.date]:
    if d is not None:
        if isinstance(d, datetime.datetime):
            return d.date()
        elif isinstance(d, datetime.date):
            return d
        elif isinstance(d, str):
            return datetime.datetime.strptime(d, "%Y-%m-%d").date()
        elif isinstance(d, (int, float)):
            return datetime.datetime.fromtimestamp(d).date()
        else:
            raise ValueError(f"Unsupported data format: {d}")


def parse_datetime(t: Optional[TIME]) -> datetime.datetime:
    if t is not None:
        if isinstance(t, datetime.datetime):
            return t
        elif isinstance(t, datetime.date):
            return datetime.datetime.combine(t, datetime.time())
        elif isinstance(t, str):
            return datetime.datetime.fromisoformat(t)
        elif isinstance(t, (int, float)):
            return datetime.datetime.fromtimestamp(t)
        else:
            raise ValueError(f"Unsupported data format: {t}")


def extract_date_from_filename(filename: str) -> Optional[datetime.date]:
    regex = "(\d{4}\-\d{2}\-\d{2})"
    match = re.search(regex, filename)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
