import sys

from setuptools import find_packages, setup


if sys.version_info[:2] < (2, 7):
    raise Exception("Vast lib only work on Python 2.7 and greater or PyPy")



setup(
    name="vast",
    description="Utility to parse vast XML documents",
    url="https://github.com/ofreshy/vast",
    author="Offer Sharabi",
    author_email="sharoffer@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['attrs=17.1.0', 'enum34==1.1.6', 'xmltodict==0.11.0'],
    setup_requires=["vcversioner"],
    vcversioner={"version_module_paths": ["vast/_version.py"]},
)
