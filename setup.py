from setuptools import setup, find_packages
import os

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

datadir = os.path.join('data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup(
    name='CS839-1',
    version='0.1.0',
    description='Stage One for CS839 Project',
    long_description=readme,
    author='Ankit Maharia',
    author_email='anktimaharia@gmail.com',
    url='https://gitlab.com/Maharia/StageOne',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    data_files = datafiles
)