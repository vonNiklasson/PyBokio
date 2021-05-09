from setuptools import find_packages, setup

packages = find_packages(exclude=["tests"])

setup(
    packages=packages,
    install_requires=[
        "dataclasses==0.8; python_version>='3.6' and python_version<'3.7'",
        "requests>=2.20,<3",
        "jsonschema>=3.0,<4"
    ],
)
