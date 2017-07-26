


BioKit
####################


.. image:: biokit.gif
    :width: 30%


.. image:: https://badge.fury.io/py/biokit.svg
       :target: https://pypi.python.org/pypi/biokit

.. image:: https://secure.travis-ci.org/biokit/biokit.png
       :target: http://travis-ci.org/biokit/biokit

.. image:: https://coveralls.io/repos/biokit/biokit/badge.png?branch=master 
      :target: https://coveralls.io/r/biokit/biokit?branch=master 



:note: BioKit is tested with Travis for the following Python version: 2.7.9
       3.4.2 and 3.5.0

:contributions: Please join https://github.com/biokit/biokit 
:issues: Please use https://github.com/biokit/biokit/issues


Overview
###############

BioKit is a set of tools gathered from several other Python packages. 
So far, it contains a few plotting tools (viz module), some statistical
analysis, some tools to access to Taxon and GO identifier, some basic tools to
manipulate sequences and so on. Many biological software are developed in R so we
also added a module to ease the installation and usage of R tools within BioKit.


In order to install biokit, you can use **pip**::

    pip install biokit


Or using bioconda channel from the Anaconda project::

    conda install biokit



Overview
#############

.. autosummary::

    biokit.converters
    biokit.network
    biokit.viz
    biokit.rtools
    biokit.sequence
    biokit.stats


.. toctree::
    :maxdepth: 2 
    :numbered:

    auto_examples/index
    references
    glossary
    ChangeLog.rst


Examples in notebooks
########################

Set of `Notebooks <http://nbviewer.ipython.org/github/biokit/biokit/tree/master/notebooks/>`_



