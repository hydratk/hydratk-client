# -*- coding: utf-8 -*-
"""Logger frame

.. module:: logger
   :platform: Windows
   :synopsis: Logger frame
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
    """Class Logger
    """
    
    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None
    _config = None

    # log parameters
    _log = None
    _level = None
    _msg_format = None
    _logdir = None
    _logfile = None
    
    def __init__(self, root):
        """Class constructor

        Called when object is initialized

        Args:
           root (obj): root frame

        Raises:
           error: ValueError

        """

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self._root = root
        self._trn = root.trn
        self._config = root.cfg

        tk.LabelFrame.__init__(self, root._pane_right, text=self.trn.msg('htk_gui_log_label'))
        self._set_gui()
        self._parse_config()

    @staticmethod
    def get_instance(root=None):
        """Method gets Logger singleton instance

        Args:
            root (obj): root frame

        Returns:
            obj

        """

        if (Logger._instance is None):
            Logger._instance_created = True
            Logger._instance = Logger(root)

        return Logger._instance

    @property
    def root(self):
        """ root property getter """

        return self._root

    @property
    def trn(self):
        """ trn property getter """

        return self._trn

    @property
    def config(self):
        """ config property getter """

        return self._config

    @property
    def log(self):
        """ log property getter """

        return self._log

    @property
    def level(self):
        """ level property getter """

        return self._level

    @property
    def msg_format(self):
        """ msg_format property getter """

        return self._msg_format

    @property
    def logdir(self):
        """ logdir property getter """

        return self._logdir

    @property
    def logfile(self):
        """ logfile property getter """

        return self._logfile

    def _parse_config(self):
        """Method parses configuration

        Args:
            none

        Returns:
            void

        """

        self._level = log_levels[self.config.data['Logger']['level']]
        self._msg_format = self.config.data['Logger']['format']

        self._logdir = self.config.data['Logger']['logdir']
        self._logfile = open(path.join(self._logdir, datetime.now().strftime('%Y%m%d') + '.log'), 'a')

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self._log = ScrolledText(self, state=tk.DISABLED)
        self._log.pack(expand=True, fill=tk.BOTH)
        self._log.focus_set()

    def write_msg(self, msg, level=3):
        """Method writes to log (GUI and file)

        Args:
            msg (str): message
            level (int): level, 1-ERROR, 2-WARN, 3-INFO, 4-DEBUG

        Returns:
            void

        """

        if (self._level >= level):
            level = list(log_levels.keys())[list(log_levels.values()).index(level)]
            msg = self._msg_format.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level=level, message=msg)
            self._log.configure(state=tk.NORMAL)
            self._log.insert(tk.END, msg + '\n')
            self._log.see('end')
            self._log.configure(state=tk.DISABLED)

            self._logfile.write(msg + '\n')
            self._logfile.flush()

    def debug(self, msg):
        """Method writes DEBUG message

        Args:
            msg (str): message

        Returns:
            void

        """

        self.write_msg(msg, 4)

    def info(self, msg):
        """Method writes INFO message

        Args:
            msg (str): message

        Returns:
            void

        """

        self.write_msg(msg, 3)

    def warn(self, msg):
        """Method writes WARN message

        Args:
            msg (str): message

        Returns:
            void

        """

        self.write_msg(msg, 2)

    def error(self, msg):
        """Method writes ERROR message

        Args:
            msg (str): message

        Returns:
            void

        """

        self.write_msg(msg, 1)
