# -*- coding: utf-8 -*-
"""Notebook

.. module:: notebook
   :platform: Windows
   :synopsis: Notebook
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 2):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk

import tkMessageBox
import os

from hydratk.filetab import FileTab

class CustomNotebook(ttk.Notebook):
    """Class CustomNotebook
    """

    # references
    _parent = None

    # tabs
    _tabs = []
    _new_cnt = 0

    def __init__(self, parent, *args, **kwargs):
        """Class constructor

        Called when object is initialized

        Args:
           parent (obj): parent frame
           args (list): arguments
           kwargs (dict): key value arguments

        Raises:
           error: ValueError

        """

        self._parent = parent
        kwargs['style'] = 'CustomNotebook'
        self._set_custom_style()
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self._set_gui()

    @property
    def parent(self):
        """ parent property getter """

        return self._parent

    @property
    def new_cnt(self):
        """ new_cnt property getter """

        return self._new_cnt

    def _set_custom_style(self):
        """Method sets custom style

        Args:
            none

        Returns:
            void

        """

        style = ttk.Style()
        self.parent.root.images['close'] = tk.PhotoImage('close', file=os.path.join(self.parent.root.imgdir, 'close.gif'))
        self.parent.root.images['close_active'] = tk.PhotoImage('close_active', file=os.path.join(self.parent.root.imgdir, 'close_active.gif'))

        style.element_create('close', 'image', 'close',
                            ('active', '!disabled', 'close_active'), border=8, sticky='')
        style.layout('CustomNotebook', [('CustomNotebook.client', {'sticky': 'nswe'})])
        style.layout('CustomNotebook.Tab', [
            ('CustomNotebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('CustomNotebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('CustomNotebook.focus', {
                                'side': 'top',
                                'sticky': 'nswe',
                                'children': [
                                    ('CustomNotebook.label', {'side': 'left', 'sticky': ''}),
                                    ('CustomNotebook.close', {'side': 'left', 'sticky': ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self.enable_traversal()
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Control-F4>', self.close_tab)

    def is_tab_present(self, path):
        """Method checks if tab with given file path is present

        Args:
            path (str): file path

        Returns:
            tuple: result (bool), index (int)

        """

        res, idx = False, None
        for i in range(0, len(self._tabs)):
            if (self._tabs[i].path == path):
                res, idx = True, i

        return res, idx

    def add_tab(self, path=None, content=None, **kwargs):
        """Method adds file tab

        Args:
            path (str): file path
            content (str): file content
            kwargs (dict): key values arguments

        Returns:
            void

        """

        tab = FileTab(self, kwargs['text'], path, content)
        self._tabs.append(tab)
        self.add(tab, **kwargs)
        self.select(len(self._tabs) - 1)

        if (len(self._tabs) == 1):
            self.set_tab_related_controls(True)

    def get_current_index(self):
        """Method gets index of current tab

        Args:
            none

        Returns:
            int

        """

        return self.index(self.select())

    def get_current_tab(self):
        """Method gets current tab

        Args:
            none

        Returns:
            obj

        """

        try:
            return self._tabs[self.get_current_index()]
        except tk.TclError:
            return None

    def get_current_content(self):
        """Method gets content of current tab

        Args:
            none

        Returns:
            str

        """

        tab = self.get_current_tab()
        return tab.text.get('1.0', 'end-1c') if (tab is not None) else None

    def get_content(self, idx):
        """Method gets content of given tab

        Args:
            idx (int): index

        Returns:
            str

        """

        return self._tabs[idx].text.get('1.0', 'end-1c')

    def get_marked_content(self):
        """Method gets marked content

        Args:
            none

        Returns:
            str

        """

        tab = self.get_current_tab()
        return tab.text.get(tk.SEL_FIRST, tk.SEL_LAST) if (tab is not None) else None

    def set_current_tab(self, name, path, modified):
        """Method sets various tab parameters

        Args:
            name (str): file name
            path (str): file path
            modified (bool): modified flag

        Returns:
            void

        """

        idx = self.get_current_index()
        self.tab(idx, text=name)
        self._tabs[idx].name = name
        self._tabs[idx].path = path
        self._tabs[idx].text.edit_modified(modified)

    def set_tab_related_controls(self, enable):
        """Method sets controls enabled by tab presence

        Args:
            enable (bool): enable/disable controls

        Returns:
            void

        """

        state = tk.NORMAL if (enable) else tk.DISABLED

        menu = self.parent.root._menu_file
        menu.entryconfig(2, state=state)
        menu.entryconfig(3, state=state)

        menu = self.parent.root._menu_edit
        menu.entryconfig(0, state=state)
        menu.entryconfig(1, state=state)
        menu.entryconfig(2, state=state)
        menu.entryconfig(3, state=state)
        menu.entryconfig(4, state=state)
        menu.entryconfig(5, state=state)
        menu.entryconfig(6, state=state)
        menu.entryconfig(7, state=state)
        menu.entryconfig(8, state=state)
        menu.entryconfig(9, state=state)

        menu = self.parent.root._menu_view
        menu.entryconfig(2, state=state)
        menu.entryconfig(3, state=state)

        tools = self.parent.root.tools
        tools['save'].config(state=state)
        tools['undo'].config(state=state)
        tools['redo'].config(state=state)
        tools['cut'].config(state=state)
        tools['copy'].config(state=state)
        tools['paste'].config(state=state)
        tools['delete'].config(state=state)
        tools['find'].config(state=state)

    def on_release(self, event=None):
        """Method handles tab close button

        Args:
            event (obj): event

        Returns:
            void

        """

        if (event.widget.identify(event.x, event.y) == 'close'):
            index = self.index('@%d,%d' % (event.x, event.y))
            self.close_tab(index=index)

    def close_tab(self, event=None, index=None):
        """Method closes tab

        Popup is displayed for unsaved file

        Args:
            event (obj): event
            index (int): index

        Returns:
            void

        """

        if (index is None):
            index = self.get_current_index()

        tab = self._tabs[index]
        if (tab.text.edit_modified()):
            res = tkMessageBox.askyesno(self.parent.trn.msg('htk_gui_editor_close_save_title'),
                                        self.parent.trn.msg('htk_gui_editor_close_save_question', tab.name))
            if (res):
                self.parent.save_file(path=tab._path)

        self.forget(index)
        self.event_generate('<<NotebookTabClosed>>')
        del self._tabs[index]

        if (len(self._tabs) == 0):
            self.set_tab_related_controls(False)
