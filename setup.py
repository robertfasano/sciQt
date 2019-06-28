from distutils.core import setup
from setuptools import find_packages

import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
extra_files = package_files('sciQt/resources')

setup(
    name='sciQt',
    version='0.1',
    description='Rapid GUI building library for scientific applications',
    author='Robert Fasano',
    author_email='robert.j.fasano@colorado.edu',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    package_data={'': extra_files},
    include_package_data = True,
    install_requires=['pyqt5', 'requests', 'pint', 'numpy']
)
