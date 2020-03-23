import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]

setup(
    name="kaishi",
    version="0.11",
    author="KUNGFU.AI",
    author_email="michael@kungfu.ai",
    description=("Tool kit to accelerate the first steps of the data science process"),
    url="https://github.com/kungfuai/kaishi",
    packages=find_packages(),
    include_package_data=True,
    download_url="https://github.com/kungfuai/kaishi/archive/0.11.tar.gz",
    classifiers=classifiers,
    zip_safe=False,
)
