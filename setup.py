from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

packages = find_packages(exclude=["tests"])

setup(
    name="PyBokio",
    url="https://github.com/vonNiklasson/pybokio",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=packages,
    install_requires=[
        "dataclasses==0.8; python_version>='3.6' and python_version<'3.7'",
        "requests>=2.20,<3",
        "jsonschema>=3.0,<4"
    ],
)
