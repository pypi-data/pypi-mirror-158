"""Module setup."""

import runpy
import unittest
from setuptools import setup, find_packages

PACKAGE_NAME = "pypws"
version_meta = runpy.run_path("./version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author="DNV",
        author_email="software.support@dnv.com",
        license = "MIT License",
        packages=find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.6",
        scripts=["scripts/pypws-cli"],
        description="Python library supporting Phast Web Services",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        package_data={
            "text": ["*.txt", "*.rst"],
            "images": ["../images/*.png", "../images/*.jpg"],
        },
        project_urls={
            "Phast Web Services": "https://www.phastwebservices.dnv.com",
            "Phast Online": "https://www.phast.dnv.com",            
            "Veracity by DNV": "https://www.veracity.com/",
            "Phast Desktop": "https://www.dnv.com/services/process-hazard-analysis-software-phast-1675",
        },
        keywords="Phast Consequence Analysis QRA CPQRA DNV Discharge Dispersion Fire Explosion Toxic Flammable Hazard Gas",
        url="https://phastwebservices.dnv.com",
    )
