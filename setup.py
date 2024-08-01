from setuptools import find_packages, setup

setup(
    name="intelligence_pipeline",
    packages=find_packages(exclude=["intelligence_pipeline_tests"]),
    install_requires=[
        "dagster-cloud",
        "dagster-duckdb",
        "dagster",
        "pandas[parquet]",
        "polars",,
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
