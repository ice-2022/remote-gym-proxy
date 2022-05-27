from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0'

setup(
    name='remote-gym-proxy',  # package name
    version=VERSION,  # package version
    description='a gym env proxy',  # package description
    packages=find_packages(),
    zip_safe=False,
)
