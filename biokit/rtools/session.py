# -*- python -*-
#
#  This file is part of biokit software
#
#  Copyright (c) 2014
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

    ::

        from biokit.rtools import RSession
        session = RSession()
        session.run("mylist = c(1,2,3)")
        a = session("mylist")
        a.sum() # a is numpy array

    For now, this is just to inherit from **pyper.R** class but there is no
    additional features. This is to create a common API.

    .. todo:: connection/pipe breaks sometimes.
    """

    def __init__(self, RCMD='R', max_len=1000, use_numpy=True, use_pandas=True,
            use_dict=None, host='localhost', user=None, ssh='ssh',
            return_err=True, verbose=False):
        """

        :param str RCMD: the name of the R executable
        :param max_len: define the upper limitation for the length of command string. A
           command string will be passed to R by a temporary file if it is longer
           than this value.
        :param bool use_numpy:: A False value will disable numpy even
           if it has been imported.
        :param bool use_pandas: A False value will disable pandas even
           if it has been imported.
        :param use_dict: named list will be returned a dict if use_dict is True, otherwise
           it will be a list of tuples (name, value).
        :parma host: The computer name (or IP) on which the R interpreter is
           installed. The value "localhost" means that the R locates on the
           the localhost computer. On POSIX systems (including Cygwin
           environment on Windows), it is possible to use R on a remote
           computer if the command "ssh" works. To do that, the user need set
           this value, and perhaps the parameter "user".
         :param user: The user name on the remote computer. This value need to be set
           only if the user name is different on the remote computer. In
           interactive environment, the password can be input by the user if
           prompted. If running in a program, the user need to be able to
           login without typing password!
         :param ssh: The program to login to remote computer. not tested


        """
        super(RSession, self).__init__(RCMD=RCMD, max_len=max_len,
                use_numpy=use_numpy, use_pandas=use_pandas,
                use_dict=use_dict, host=host, user=user, ssh=ssh,
                dump_stdout=verbose)

    def get_version(self):
        """Return the R version"""
        return self.version

    def reconnect(self):
        """if Ctrl+C is pressed, the pipe may be broken, in which caes, reconnecting
        would be handy
        """
        raise NotImplementedError


