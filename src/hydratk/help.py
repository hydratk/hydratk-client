# -*- coding: utf-8 -*-
"""Help

.. module:: help
   :platform: Windows
   :synopsis: Help
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from webbrowser import open

from hydratk.tkimport import tk

class Help(object):
    """Class help
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None

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

    @staticmethod
    def get_instance(root=None):
        """Method gets Help singleton instance

        Args:
            none

        Returns:
            obj

        """

        if (Help._instance is None):
            Help._instance_created = True
            Help._instance = Help(root)

        return Help._instance

    @property
    def root(self):
        """ root property getter """

        return self._root

    @property
    def trn(self):
        """ trn property getter """

        return self._trn

    def win_about(self):
        """Method displays About window

        Args:
            none

        Returns:
            void

        """

        win = tk.Toplevel(self.root)
        win.title(self.trn.msg('htk_gui_help_about_title'))
        win.transient(self.root)
        win.resizable(False, False)
        win.geometry('+%d+%d' % (self.root.winfo_screenwidth() / 3, self.root.winfo_screenheight() / 3))
        win.tk.call('wm', 'iconphoto', win._w, self.root.images['logo'])

        text = tk.Text(win)
        text.pack(expand=True, fill=tk.BOTH)
        text.focus_set()
        content = """Client for HydraTK

Version: 0.1.0
Web: http://hydratk.org

Copyright (c) 2017-2017
Petr Rašek (bowman@hydratk.org)
HydraTK team (team@hydratk.org)
All rights reserved."""
        text.insert(tk.END, content)
        text.configure(state=tk.DISABLED)

        tk.Button(win, text='Web', command=lambda: open('http://hydratk.org')).pack(side=tk.LEFT, pady=3)
        tk.Button(win, text='E-mail', command=lambda: open('mailto:team@hydratk.org')).pack(side=tk.LEFT, padx=3, pady=3)
        tk.Button(win, text='OK', command=lambda: win.destroy()).pack(side=tk.RIGHT, pady=3)
        win.bind('<Escape>', lambda f: win.destroy())
