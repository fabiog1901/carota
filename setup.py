import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="carota",
    version="0.0.1",
    description="CSV Generator for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fabiog1901/carota",
    author="Fabio Ghirardello",
    author_email="",
    license="GPL v3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["carota"],
    include_package_data=True,
    install_requires=[

    ],
    entry_points={
        "console_scripts": [
            "carota=carota.__main__:main",
        ]
    },
)