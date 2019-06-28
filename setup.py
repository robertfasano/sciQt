from distutils.core import setup
from setuptools import find_packages

setup(
    name='sciQt',
    version='0.1',
    description='Rapid GUI building library for scientific applications',
    author='Robert Fasano',
    author_email='robert.j.fasano@colorado.edu',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=['pyqt5', 'requests', 'abc', 'os', 'json', 'pint', 'numpy']
)
