BioKit
==========

Bioinformatics in Python




.. image:: https://badge.fury.io/py/biokit.svg
    :target: https://pypi.python.org/pypi/biokit

.. image:: https://pypip.in/d/biokit/badge.png
    :target: https://crate.io/packages/biokit/

.. image:: https://secure.travis-ci.org/cokelaer/biokit.png
    :target: http://travis-ci.org/cokelaer/biokit

.. image:: https://coveralls.io/repos/cokelaer/biokit/badge.png?branch=master 
   :target: https://coveralls.io/r/cokelaer/biokit?branch=master 

.. image:: https://landscape.io/github/cokelaer/biokit/master/landscape.png
   :target: https://landscape.io/github/cokelaer/biokit/master

.. image:: https://badge.waffle.io/cokelaer/biokit.png?label=ready&title=Ready 
   :target: https://waffle.io/cokelaer/biokit

:note: BioKit is tested under Python 2.7
       Note yet fully compatible with python 3.3 but should be easy to fix (import issue)

:contributions: Please join https://github.com/biokit/biokit and share your notebooks https://github.com/biokit/biobooks/
:issues: Please use https://github.com/biokit/biokit/issues


.. image:: http://pythonhosted.org/biokit/_images/biokit.gif
    :target: http://pythonhosted.org/biokit/_images/biokit.gif


testing
==========

From travis, coverage is about 50% at the moment, which is low because some tests are ignored. Tests ignored are
those that are slow or required R dependencies. To be ignored, we filled the setup.cfg with an option called **attr**. 
IF you comment that attribute in the **setup.cfg** and run ::

    python setup.py nosetests
    
You should reach a higher coverage (about 70%)    
