# -*- coding: utf-8 -*-
__revision__ = "$Id$"
import sys
import os
from setuptools import setup, find_packages
import glob


_MAJOR               = 0
_MINOR               = 5
_MICRO               = 0
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {
        'Cokelaer':('Thomas Cokelaer','cokelaer@gmail.com'),
        },
    'version': version,
    'license' : 'BSD',
    'download_url' : 'http://github.com/biokit/biokit',
    'url' : 'http://github.com/biokit/biokit',
    'description':'Set of tools related to Bioinformatics (e.g., visualisation)' ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['corrplot', 'heatmap'],
    'classifiers' : [
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }

with open('README.rst') as f:
    readme = f.read()

from distutils.core import setup, Extension

sequence = Extension('sequence', sources=['biokit/sequence/sequence.c'])

setup(
    name             = 'biokit',
    version          = version,
    maintainer       = metainfo['authors']['Cokelaer'][0],
    maintainer_email = metainfo['authors']['Cokelaer'][1],
    author           = metainfo['authors']['Cokelaer'][0],
    author_email     = metainfo['authors']['Cokelaer'][1],
    long_description = readme,
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    zip_safe=False,
    packages = find_packages(),
    # package installation
    #package_dir = package_dir,
    #packages = ['biokit'],
    #package_dir  = package_dir,

    # distutils in rtools.package
    # suds-jurko is used by bioservices so we probab ly do not need it in the
    # setup.
    install_requires = open('requirements.txt').read().split(),

     # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},

    package_data = {
        '': ['*.csv'],
        'biokit.data' : ['*csv'],
        'biokit.data.converters' : ['*']
        },

    entry_points = {
        'console_scripts':[
        ]
    }

    )


