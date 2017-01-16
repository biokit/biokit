Whats' new, what has changed
================================

:Revision: 0.3.3:

    * EM class has a new plot function so that a plot can be run without doing
      the estimation but by providing the parameter of the model. This is a
      better model/data/view abstraction.

:Revision: 0.3.2:

    * remove deprecated warning 

:Revision: 0.3.1:

    * Update mixture.EM method to speedup the code by factor 4

:Revision: 0.3.0:

    * Cleanup and doc update
    * Update notebooks to be py3.5 compatible
    * Some API changes in the Taxonomy module used in Sequana package


:Revision 0.2.0:

    * NEWS

        * add boxplot module.


:Revision 0.1.4:

    * BUG FIXES: cleanup MANIFEST


:Revision 0.1.3:

    * BUG FIXES: 

        * a py3 typo.
        * fixing complexes module
        * remove useless db package

:Revision 0.0.7:

    * NEWS

      * add taxonomy module.
      * add goid module.
      * Fixed bunch of Python3 issues. most important in rtools packages
        to use Popen instead of popen4 and manipulate bytes vs strings.
      * All tests passes under Python2.7 and Python3.4


:Revision 0.0.6:
  * CHANGES

    * viz package:

      * refactored most of the functions/classes to be have more
        consistent input data for the constructor and more consistent
        parameters for the plot() methods.
      * Hist2d is now called Hist2D

  * BUG FIXES

  * NEWS

    * add new module in viz package: hinton, core (to factorise code)
    * add new notebooks related to the viz package.

