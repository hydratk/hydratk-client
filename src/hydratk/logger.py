# -*- coding: utf-8 -*-
"""Logger

.. module:: logger
   :platform: Windows
   :synopsis: Logger
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 2):
    import Tkinter as tk
else:
    import tkinter as tk

from ScrolledText import ScrolledText
from datetime import datetime
from os import path

log_levels = {
  'ERROR': 1,
  'WARN': 2,
  'INFO': 3,
  'DEBUG': 4
}

class Logger(tk.LabelFrame):
    
    _instance = None
    _instance_created = False

    _root = None
    _trn = None
    _config = None

    _log = None
    _level = None
    _format = None

    _logdir = None
    _file = None
    
    def __init__(self, root):

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self._root = root
        self._trn = self._root._trn
        self._config = self._root._config
        self._level = self._config.data['Logger']['level']
        self._format = self._config.data['Logger']['format']
        
        self._logdir = self._config.data['Logger']['logdir']
        self._file = open(path.join(self._logdir, datetime.now().strftime('%Y%m%d') + '.log'), 'a')

        tk.LabelFrame.__init__(self, root._pane_right, text=self._trn.msg('htk_gui_log_label'))
        self.set_gui()

    @staticmethod
    def get_instance(root=None):

        if (Logger._instance is None):
            Logger._instance_created = True
            Logger._instance = Logger(root)

        return Logger._instance

    def set_gui(self):

        self._log = ScrolledText(self, state=tk.DISABLED)
        self._log.pack(expand=True, fill=tk.BOTH)
        self._log.focus_set()

    def autoscroll(self, sbar, first, last):

        first, last = float(first), float(last)
        if (first <= 0 and last >= 1):
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def write_msg(self, msg, level='INFO'):

        if (log_levels[self._level] >= log_levels[level]):
            msg = self._format.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level=level, message=msg)
            self._log.configure(state=tk.NORMAL)
            self._log.insert(tk.END, msg + '\n')
            self._log.see('end')
            self._log.configure(state=tk.DISABLED)

            self._file.write(msg + '\n')
            self._file.flush()

    def debug(self, msg):

        self.write_msg(msg, 'DEBUG')

    def info(self, msg):

        self.write_msg(msg, 'INFO')

    def warn(self, msg):

        self.write_msg(msg, 'WARN')

    def error(self, msg):

        self.write_msg(msg, 'ERROR')
