# -*- coding: utf-8 -*-
"""Syntax colorizer

.. module:: colorizer
   :platform: Windows
   :synopsis: Syntax colorizer
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import __builtin__
import keyword

from hydratk.tkimport import tk

class Colorizer(object):
    """Class Colorizer
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _config = None

    _patterns = {}

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
        """Method gets Colorizer singleton instance

        Args:
            root (obj): root frame

        Returns:
            obj

        """

        if (Colorizer._instance is None):
            Colorizer._instance_created = True
            Colorizer._instance = Colorizer(root)

        return Colorizer._instance

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

        self._patterns['keyword'] = {'color' : self.config.data['Core']['color']['keyword']}
        self._patterns['string'] = {'color' : self.config.data['Core']['color']['string']}
        self._patterns['yoda'] = {'color' : self.config.data['Core']['color']['yoda']}

    def _make_patterns(self):
        """Method makes patterns for colorized strings

        Args:
            none

        Returns:
            void

        """

        # keyword
        builtin = [str(name) for name in dir(__builtin__) if not name.startswith('_')]
        kw = r'\y(' + '|'.join(keyword.kwlist + builtin) + r')\y'
        self._patterns['keyword']['pattern'] = kw

        # string
        stringprefix = r'(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR)?'
        sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
        dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
        sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
        dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
        string = r'(' + '|'.join([r'#[^\n]*', sq3string, dq3string, sqstring, dqstring]) + r')'
        self._patterns['string']['pattern'] = string

        # yoda
        tags = [
                'TEST-SCENARIO-\d+', 'TEST-CASE-\d+', 'TEST-CONDITION-\d+',
                'ID', 'PATH', 'NAME', 'DESC', 'AUTHOR', 'VERSION',
                'PRE-REQ', 'POST-REQ', 'TEST', 'VALIDATE', 'EVENTS', 'BEFORE_START', 'AFTER_FINISH'
               ]
        yoda = r'\y(' + '|'.join(tags) + r')\y\s*:\s*\|?'
        self._patterns['yoda']['pattern'] = yoda

    def colorize(self, text, start, stop):
        """Method colorizes text

        Args:
            text (obj): Text widget
            start (str): start index
            stop (str): stop index

        Returns:
            bool: yoda tag found

        """

        cnt = tk.IntVar()
        yoda_found = False
        for pattern in ['keyword', 'yoda', 'string']:
            text.tag_remove(pattern, start, stop)
            idx1 = start
            while True:
                # direct Tk call, wrap method search doesn't support nolinestop
                args = [text._w, 'search', '-count', cnt, '-regexp', '-nolinestop']
                if (pattern == 'yoda'):
                    args.append('-nocase')
                args += [self._patterns[pattern]['pattern'], idx1, stop]
                idx1 = str(text.tk.call(tuple(args)))

                if (not idx1):
                    break
                elif (pattern == 'yoda'):
                    yoda_found = True

                idx2 = '{0}+{1}c'.format(idx1, cnt.get())
                text.tag_add(pattern, idx1, idx2)
                idx1 = idx2
            text.tag_config(pattern, foreground=self._patterns[pattern]['color'])

        return yoda_found
