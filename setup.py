import os
import pathlib
import pkg_resources
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]

setup(
    name="kaishi",
    version="0.1",
    author="KUNGFU.AI",
    author_email="michael@kungfu.ai",
    description=("Tool kit to accelerate the first steps of the data science process"),
    url="https://github.com/kungfuai/kaishi",
    packages=find_packages(),
    include_package_data=True,
    download_url="https://github.com/kungfuai/kaishi/archive/0.1.tar.gz",
    classifiers=classifiers,
    install_requires=install_requires,
    zip_safe=False,
)
