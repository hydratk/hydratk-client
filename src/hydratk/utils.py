# -*- coding: utf-8 -*-
"""Utilities

.. module:: utils
   :platform: Windows
   :synopsis: Utilities
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 3):
    from string import replace
    
def fix_path(path):
    """Method fixes Windows path
    Args:
        none

    Returns:
        str

    """
    
    path = path.replace('\\', '/') if (version_info[0] == 2) else replace(path, '\\', '/')
    return path
