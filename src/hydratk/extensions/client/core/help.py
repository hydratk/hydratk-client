# -*- coding: utf-8 -*-
"""Help

.. module:: client.core.help
   :platform: Windows, Unix
   :synopsis: Help
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from webbrowser import open

from hydratk.extensions.client.core.tkimport import tk

class Help(object):
    """Class help
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None

    # gui elements
    _win = None
    _text = None
    _btn_web = None
    _btn_email = None
    _btn_ok = None

    def __init__(self):
        """Class constructor

        Called when object is initialized

        Args:
           none

        Raises:
           error: ValueError

        """

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

    @staticmethod
    def get_instance():
        """Method gets Help singleton instance

        Args:
            none

        Returns:
            obj

        """

        if (Help._instance is None):
            Help._instance_created = True
            Help._instance = Help()

        return Help._instance

    @property
    def root(self):
        """ root property getter """

        if (self._root is None):
            from hydratk.extensions.client.core.gui import Gui
            self._root = Gui.get_instance()

        return self._root

    @property
    def trn(self):
        """ trn property getter """

        if (self._trn is None):
            self._trn = self.root.trn

        return self._trn

    def win_about(self):
        """Method displays About window

        Args:
            none

        Returns:
            void

        """

        self._win = tk.Toplevel(self.root)
        self._win.title(self.trn.msg('htk_gui_help_about_title'))
        self._win.transient(self.root)
        self._win.resizable(False, False)
        self._win.geometry('+%d+%d' % (self.root.winfo_screenwidth() / 3, self.root.winfo_screenheight() / 3))
        self._win.tk.call('wm', 'iconphoto', self._win._w, self.root.images['logo'])

        self._text = tk.Text(self._win, background='#FFFFFF')
        self._text.pack(expand=True, fill=tk.BOTH)
        self._text.focus_set()
        content = """Client for HydraTK

Version: 0.1.0
Web: http://hydratk.org

Copyright (c) 2017-2018
Petr Rašek (bowman@hydratk.org)
HydraTK team (team@hydratk.org)
All rights reserved."""
        self._text.insert(tk.END, content)
        self._text.configure(state=tk.DISABLED)

        self._btn_web = tk.Button(self._win, text='Web', command=lambda: open('http://hydratk.org'))
        self._btn_web.pack(side=tk.LEFT, pady=3)
        self._btn_email = tk.Button(self._win, text='E-mail', command=lambda: open('mailto:team@hydratk.org'))
        self._btn_email.pack(side=tk.LEFT, padx=3, pady=3)
        self._btn_ok = tk.Button(self._win, text='OK', command=lambda: self._win.destroy())
        self._btn_ok.pack(side=tk.RIGHT, pady=3)
        self._win.bind('<Escape>', lambda f: self._win.destroy())

    def web_tutor(self):
        """Method opens web tutorial

        Args:
            none

        Returns:
            void

        """

        open('http://hydratk.org/rst/tutor/ext/client/client.html')

    def web_doc(self):
        """Method opens web documentation

        Args:
            none

        Returns:
            void

        """

        open('http://hydratk.org/rst/module/ext/client/client.html')
