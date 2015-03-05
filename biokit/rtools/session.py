# -*- python -*-
#
#  This file is part of biokit software
#
#  Copyright (c) 2014-
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/biokit
#
##############################################################################
from biokit.rtools import pyper

__all__ = ['RSession']


class RSession(pyper.R):
    """Interface to a R session

    This class uses the pyper package to provide an access to R (via 
    a subprocess). You can call R script and get back the results
    into the session as Python objects. Returned objects may be transformed
    into numpy arrays or Pandas datafranes.

    Here is a very simple example but any complex R scripts can be provided
    inside the :meth:`run` method::

        from biokit.rtools import RSession
        session = RSession()
        session.run("mylist = c(1,2,3)")
        a = session("mylist") # access to the R object
        a.sum() # a is numpy array

    There are different ways to access to the R object::

        # getter
        session['a']
        # method-wise:
        session.get('a')
        # attribute:
        session.a

    For now, this is just to inherit from **pyper.R** class but there is no
    additional features. This is to create a common API.

    """
    def __init__(self, RExecutable='R', max_len=1000,
            use_dict=None, host='localhost', user=None, ssh='ssh',
            verbose=False, return_err=True):
        """

        :param str RCMD: the name of the R executable
        :param max_len: define the upper limitation for the length of command string. A
           command string will be passed to R by a temporary file if it is longer
           than this value.
        :param host: The computer name (or IP) on which the R interpreter is
           installed. The value "localhost" means that the R locates on the
           the localhost computer. On POSIX systems (including Cygwin
           environment on Windows), it is possible to use R on a remote
           computer if the command "ssh" works. To do that, the user need set
           this value, and perhaps the parameter "user".
        :param user: The user name on the remote computer. This value need to be set
           only if the user name is different on the remote computer. In
           interactive environment, the password can be input by the user if
           prompted. If running in a program, the user need to be able to
           login without typing password! (i.e., you need to set your SSH keys)
        :param ssh: The program to login to remote computer.
        :param kargs: must be empty. Error raised otherwise
        """
        from easydev import cmd_exists
        if host == 'localhost' and cmd_exists(RExecutable) is False:
            raise Exception('Could not find the R executable %s in your path' % RExecutable)

        super(RSession, self).__init__(RCMD=RExecutable, max_len=max_len,
            use_dict=use_dict, host=host, user=user, ssh=ssh, return_err=return_err,
            dump_stdout=verbose)


    def get_version(self):
        """Return the R version"""
        return self.version

    def __repr__(self):
        txt = "Rsession information:" 
        txt += "\nverbosity: " + str(self.verbose)
        txt += "\ndump_stdout: " + str(self.dump_stdout)
        txt += "\ndebug mode: " + str(self._DEBUG_MODE)
        return txt



