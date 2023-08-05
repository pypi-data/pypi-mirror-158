###############################################################################
# WaterTAP Copyright (c) 2021, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National
# Laboratory, National Renewable Energy Laboratory, and National Energy
# Technology Laboratory (subject to receipt of any required approvals from
# the U.S. Dept. of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#
###############################################################################
"""
Project setup with setuptools
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
import pathlib

cwd = pathlib.Path(__file__).parent.resolve()  # this will come in handy, probably

long_description = """WaterTAP is an open-source, integrated suite of predictive multi-scale models
for design and optimization of water treatment processes and systems. Specifically, WaterTAP is a new
library of water treatment-specific property, process unit, and network models that depend on the IDAES Platform,
an open source, next generation process systems engineering platform developed at the National Energy Technology
Laboratory with other partners. The WaterTAP project is funded by the NAWI  as a part of U.S. Department of
Energy’s Energy-Water Desalination Hub. The goal of WaterTAP is to assist the hub and the broader water R&D
community in assessing existing and emerging water treatment technologies by 1) providing predictive capabilities
involving the design, optimization, and performance of water treatment systems that will lead to improved energy
efficiency and lower cost, 2) advancing the state of the art for the design of water treatment components, systems
and networks to be comparable with, or even surpass, that in the chemical industry, and 3) disseminating these tools
for active use by water treatment researchers and engineers.""".replace(
    "\n", " "
).strip()


SPECIAL_DEPENDENCIES_FOR_RELEASE = [
    "idaes-pse>=2.0.0a2",  # from PyPI
]

SPECIAL_DEPENDENCIES_FOR_PRERELEASE = [
    # update with a tag from the nawi-hub/idaes-pse
    # when a version of IDAES newer than the latest stable release from PyPI
    # will become needed for the watertap development
    "idaes-pse @ https://github.com/IDAES/idaes-pse/archive/2.0.0a2.zip"
]

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="watertap",
    url="https://github.com/watertap-org/watertap",
    version="0.5.0",
    description="WaterTAP modeling library",
    long_description=long_description,
    long_description_content_type="text/plain",
    author="NAWI team",
    license="BSD",
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="water systems, chemical engineering, process modeling, filtration, desalination, nawi",
    packages=find_namespace_packages(),
    python_requires=">=3.7, <4",
    install_requires=[
        # primary requirements for unit and property models
        # maintainers: switch to SPECIAL_DEPENDENCIES_FOR_RELEASE when cutting a release of watertap
        *SPECIAL_DEPENDENCIES_FOR_RELEASE,
        "pyomo>=6.2",  # (also needed for units in electrolyte database (edb))
        # the following requirements are for the electrolyte database (edb)
        "pymongo>3",  # database interface
        "fastjsonschema",  # schema validation
        "click",  # command-line tools with Click
        # tutorial tests
        "nbformat",
        "scipy",
        # for parameter_sweep
        "h5py",
        # for watertap.ui.api_model (though may be generally useful)
        "pydantic",
        "numpy",
    ],
    extras_require={
        "testing": [
            "pytest",
            "json-schema-for-humans",
            "mongomock",
            "pandas",
        ],
        "dev": [
            "myst-parser",  # markdown support for Sphinx
            "nbsphinx",  # jupyter notebook support for sphinx
            "jinja2<3.1.0",  # see watertap-org/watertap#449
            "Sphinx",  # docs
            "sphinx_rtd_theme",  # docs
            # other requirements
            "linkify-it-py",
            "json-schema-for-humans",  # pretty JSON schema in HTML
            "black",  # code formatting
            # other requirements
            "pytest",  # test framework
            "pytest-cov",  # code coverage
            "mongomock",  # mongodb mocking for testing
        ],
    },
    package_data={  # Optional
        "": [
            "*.json",
            "*.yaml",
            "*.yml",
            "*.csv",
        ],
    },
    entry_points={
        # add edb CLI commands
        "console_scripts": [
            "edb = watertap.edb.commands:command_base",
        ]
    },
)
