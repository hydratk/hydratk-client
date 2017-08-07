# -*- coding: utf-8 -*-
"""Text formatter

.. module:: formatter
   :platform: Windows
   :synopsis: Text formatter
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 2):
    import Tkinter as tk
else:
    import tkinter as tk

class Formatter(object):
    """Class Formatter
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _config = None

    # format
    _patterns = {}
    _ammend_keys = {}

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
        self._config = root.cfg

        self._parse_config()
        self._make_patterns()

    @staticmethod
    def get_instance(root=None):
        """Method gets Formatter singleton instance

        Args:
            oot (obj): root frame

        Returns:
            obj

        """

        if (Formatter._instance is None):
            Formatter._instance_created = True
            Formatter._instance = Formatter(root)

        return Formatter._instance

    @property
    def root(self):
        """ root property getter """

        return self._root

    @property
    def config(self):
        """ config property getter """

        return self._config

    def _parse_config(self):
        """Method parses configuration

        Args:
            none

        Returns:
            void

        """

        self._patterns['python_inc'] = {'indent' : self._config._data['Core']['format']['indent_python']}
        self._patterns['python_dec'] = {'indent' :-self._config._data['Core']['format']['indent_python']}
        self._patterns['yoda'] = {'indent' : self._config._data['Core']['format']['indent_yoda']}

    def _make_patterns(self):
        """Method makes patterns for text formatting

        Args:
            none

        Returns:
            void

        """

        # python increase
        tags = [
                'def', 'class', 'if', 'elif', 'else', 'while', 'for', 'with', 'try', 'except', 'finally'
               ]
        self._patterns['python_inc']['pattern'] = r'\y(' + '|'.join(tags) + r')\y\s*.*:'
        
        # python decrease
        tags = [
                'return', 'break', 'continue', 'pass', 'exit', 'raise'
               ]
        self._patterns['python_dec']['pattern'] = r'\y(' + '|'.join(tags) + r')\y\s+.*'

        # yoda
        tags = [
                'TEST-SCENARIO-\d+', 'TEST-CASE-\d+', 'TEST-CONDITION-\d+', 'PRE-REQ', 'POST-REQ',
                'TEST', 'VALIDATE', 'EVENTS', 'BEFORE_START', 'BEFORE_FINISH'
               ]
        self._patterns['yoda']['pattern'] = r'\y(' + '|'.join(tags) + r')\y\s*:\s*\|?'
        
        # keys to be ammended
        self._ammend_keys = {
                             '(' : ')',
                             '{' : '}',
                             '[' : ']'
                            }

    def format_text(self, event, text):
        """Method formats text

        Args:
            event (obj): event
            text (obj): Text widget

        Returns:
            void

        """

        if (event.keysym == 'Return'):
            self.indent(text)
        elif (event.char in self._ammend_keys):
            self.ammend_key(event.char, text)
            
    def ammend_key(self, key, text):
        """Method ammends predefined key

        Args:
            key (str): key
            text (obj): Text widget

        Returns:
            void

        """

        text.insert(tk.INSERT, self._ammend_keys[key])

    def indent(self, text):
        """Method sets indent

        Args:
            text (obj): Text widget

        Returns:
            void

        """

        row, col = text.index(tk.INSERT).split('.')
        start, stop = '{0}.0'.format(int(row) - 1), '{0}.0-1c'.format(row)
        content = text.get(start, stop)
        indent = len(content) - len(content.lstrip())

        for key, value in self._patterns.items():
            nocase = True if (key == 'yoda') else False
            idx = text.search(value['pattern'], start, stopindex=stop, nocase=nocase, regexp=True)
            if (idx):
                indent += value['indent']
                if (indent < 0):
                    indent = 0
                break

        text.insert(tk.INSERT, ' ' * indent)
