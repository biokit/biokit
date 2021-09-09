BioKit
==========

General Bioinformatics tools in Python


.. image:: https://badge.fury.io/py/biokit.svg
    :target: https://pypi.python.org/pypi/biokit

.. image:: https://img.shields.io/pypi/pyversions/biokit.svg
    :target: https://www.python.org

.. image:: https://github.com/biokit/biokit/actions/workflows/main.yml/badge.svg
    :target: https://github.com/biokit/biokit/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/biokit/biokit/badge.png?branch=master 
   :target: https://coveralls.io/r/biokit/biokit?branch=master 

.. image:: http://readthedocs.org/projects/biokit/badge/?version=master
    :target: http://biokit.readthedocs.org/en/master/?badge=master
    :alt: Documentation Status



:note: BioKit is tested with Travis for the following Python version: 3.7, 3.8, 3.9

:contributions: Please join https://github.com/biokit/biokit 
:issues: Please use https://github.com/biokit/biokit/issues


.. image:: http://pythonhosted.org/biokit/_images/biokit.gif
    :target: http://pythonhosted.org/biokit/_images/biokit.gif

Contents
===============

BioKit is a set of tools gathered from several other Python packages. The goal
is to gather tools that should be useful to develop computational biology
software. Biokit contains a few plotting tools (viz module), some statistical
analysis (mixture model), some tools to access to Taxon and GO identifier, some basic tools to manipulate sequences and so on. It is linked to BioServices package to provide access to biological resources. Lots of biological software are developed in R. We have also added a module to ease the installation and usage of R tools within BioKit.

**WARNING**: This package is maintained and used in production but its
contents are moving slowly to another project called sequana
(sequana.readthedocs.io) (.e.g mixture model from biokit.stats and biokit.viz
will most probably be moved in the current of 2021-2022).

Installation
==============

::

    pip install biokit


or from bioconda::

    conda install bioconda
