# -*- coding: utf-8 -*-
#
# you can install this to a local test virtualenv like so:
#   virtualenv venv
#   ./venv/bin/pip install --editable .
#   ./venv/bin/pip install --editable .[dev]  # with dev requirements, too

import expmgmt

import glob
import setuptools
import sys

with open("README.md") as fd:
    long_description = fd.read()

if sys.platform == "win32":
    data_files = []
else:
    data_files = []

included_packages = ["expmgmt"] + ["expmgmt." + p for p in setuptools.find_packages("expmgmt")]

setuptools.setup(
    name="expmgmt",
    version=expmgmt.__version__,
    maintainer=expmgmt.__maintainer__,
    maintainer_email=expmgmt.__email__,
    author=expmgmt.__author__,
    author_email=expmgmt.__email__,
    license=expmgmt.__license__,
    url="https://github.com/wbrandenburger/ExpMgmt",
    install_requires=[
        "natsort>=7.0.0"
        # - python project packages - 
        # "colorama>=0.4",
        # "click>=7.0.0",
        # "stevedore>=1.30",
        # "configparser>=3.0.0",
        # "PyYAML>=3.12",
    ],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 1 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    extras_require=dict(
        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[develop]
        optional=[
        ],
        develop=[
        ]
    ),
    description=(
        "Visualization tool for exploring remote sensing data and view processing results"
    ),
    long_description=long_description,
    keywords=[
        "visualization", "remote sensing", "images", "aerial", "satellite", "viewer", "explorer", "science", "research", "command-line", "tui"
    ],
    package_data=dict(
        expmgmt=[
        ],
    ),
    data_files=data_files,
    packages=included_packages,
    entry_points={
        "console_scripts": [
            "expmgmt=expmgmt.commands.default:run",

        ],
        "expmgmt.command": [
            "data=expmgmt.commands.data:cli",
            "run=expmgmt.commands.run:cli",
        ],
    },
    platforms=["linux", "osx", "windows"],
)
