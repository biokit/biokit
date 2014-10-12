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
import pyper

__all__ = ['RSession']


class RSession(pyper.R):
    """Interface to pyper

        session = RSession()
        session.run("a = c(1,2,3)")
        a = session.ge("a")
        a.sum() # a is numpy array



    For now, this is just to inherit from pyper.R class but there is no
    additional feature. This is to create a common API.

    .. todo:: connection/pipe breaks sometimes.
    """

    def __init__(self, RCMD='R', max_len=1000, use_numpy=True, use_pandas=True,
            use_dict=None, host='localhost', user=None, ssh='ssh',
            return_err=True, dump_stdout=False):

        super(RSession, self).__init__(RCMD=RCMD, max_len=max_len,
                use_numpy=use_numpy, use_pandas=use_pandas,
                use_dict=use_dict, host=host, user=user, ssh=ssh,
                dump_stdout=dump_stdout)

    def get_version(self):
        raise NotImplementedError


