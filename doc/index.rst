


BioKit
####################


.. image:: https://badge.fury.io/py/biokit.svg
       :target: https://pypi.python.org/pypi/biokit

.. image:: https://img.shields.io/pypi/pyversions/biokit.svg
       :target: https://www.python.org

.. image:: https://secure.travis-ci.org/biokit/biokit.png
       :target: http://travis-ci.org/biokit/biokit

.. image:: https://coveralls.io/repos/cokelaer/biokit/badge.png?branch=master 
      :target: https://coveralls.io/r/cokelaer/biokit?branch=master 

.. image:: http://readthedocs.org/projects/biokit/badge/?version=master
    :target: http://biokit.readthedocs.org/en/master/?badge=master
    :alt: Documentation Status



:note: BioKit is tested with Travis for the following Python 
    version: 2.7, 3.5, 3.6
:contributions: Please join https://github.com/biokit/biokit 
:issues: Please use https://github.com/biokit/biokit/issues


Overview
###############

BioKit is a set of tools dedicated to bioinformatics, data visualisation (:mod:`biokit.viz`), 
access to online biological data (e.g. UniProt, NCBI thanks to bioservices). It also contains
more advanced tools related to data analysis (e.g., :mod:`biokit.stats`). Since R is quite common in bioinformatics, we also provide a convenient module to run R inside your Python 
scripts or shell (:mod:biokit.rtools module).

In order to install biokit, you can use **pip**::

    pip install biokit

Or using bioconda channel from the Anaconda project::

    conda install biokit


Overview
#############

.. autosummary::

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



