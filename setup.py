#!/usr/bin/env python

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=6.0",
    # TODO: put package requirements here
]

test_requirements: list[str] = [
    # TODO: put package test requirements here
]

setup(
    name="coastline",
    version="0.1.0",
    description="Scripted Report Generator",
    long_description=readme + "\n\n" + history,
    author="Kevin Wierman",
    author_email="kwierman@gmail.com",
    url="https://github.com/CaspianDataLabs/coastline",
    packages=[
        "coastline",
    ],
    package_dir={"coastline": "coastline"},
    entry_points={"console_scripts": ["coastline=coastline.cli:main"]},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license': 'License :: OSI Approved :: MIT License",
    zip_safe=False,
    keywords="coastline",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "MIT license': 'License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.14",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
