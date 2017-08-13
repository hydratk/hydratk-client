# -*- coding: utf-8 -*-
"""Tkinter import aliases

.. module:: tkimports
   :platform: Windows
   :synopsis: Tkinter import aliases
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import sys

if (sys.version_info[0] == 2):
    reload(sys)
    sys.setdefaultencoding('UTF8')
    import Tkinter as tk
    import ttk as ttk
    import Tix as tix
else:
    import tkinter as tk
    from tkinter import ttk as ttk
    from tk import tix as tix

import tkMessageBox
import tkFileDialog
from ScrolledText import ScrolledText

tk = tk
ttk = ttk
tix = tix
tkmsg = tkMessageBox
tkfd = tkFileDialog
tkst = ScrolledText
