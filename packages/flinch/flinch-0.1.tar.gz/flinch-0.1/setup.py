'''
Created on Jul 30, 2018
@author: pankajrawat
'''
import setuptools
import subprocess
import pathlib
import pkg_resources
from glob import glob

version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in version


with open("README.md", "r") as fh:
    long_description = fh.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name="flinch",
    version=version,
    author="Pankaj Rawat",
    author_email="pankajr141@gmail.com",
    description="python functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pankajr141/flinch",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=install_requires
)
