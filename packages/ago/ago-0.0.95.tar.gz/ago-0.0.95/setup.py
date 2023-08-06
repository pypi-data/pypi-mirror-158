# installation: pip install ago

from setuptools import setup, find_packages

setup(
    name="ago",
    version="0.0.95",
    description="ago: Human readable timedeltas",
    keywords="ago human readable time deltas timedelta datetime timestamp",
    long_description=open("README.rst").read(),
    author="Russell Ballestrini",
    author_email="russell.ballestrini@gmail.com",
    url="https://git.unturf.com/python/ago",
    packages=find_packages(exclude="tests"),
    platforms=["All"],
    license="Public Domain",
    py_modules=["ago"],
    include_package_data=True,
)

# setup keyword args: http://peak.telecommunity.com/DevCenter/setuptools

# built and uploaded to pypi with this:
#python setup.py sdist bdist_egg
#twine upload dist/*

