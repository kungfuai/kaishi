import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


print(find_packages())
setup(
    name="kaishi",
    version="0.0.1",
    author="KUNGFU.AI",
    author_email="michael@kungfu.ai",
    description=("Tool kit to accelerate the first steps of the data science process"),
    url="https://github.com/kungfuai/kaishi",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
