import codecs
import io
import os
import re

from setuptools import setup, find_packages

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))


def read(*parts):
    with codecs.open(os.path.join(SETUP_DIR, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)[3:]  # Skip title
source_license = readfile("LICENSE")
requires = ['PySide6', 'cmlibs.exporter', 'cmlibs.zinc']  # Minimal requirements listing. Insert additional dependencies here.


setup(
    name='mapclientplugins.generateflatmapsourcesstep',
    version=find_version('mapclientplugins', 'generateflatmapsourcesstep', '__init__.py'),
    description='',
    long_description='\n'.join(readme) + source_license,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    author='Hugh Sorby',
    author_email='',
    url='',
    packages=find_packages(exclude=['ez_setup', ]),
    namespace_packages=['mapclientplugins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
