# -*- coding: utf-8 -*-
"""Editor

.. module:: editor
   :platform: Windows
   :synopsis: Editor
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 2):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk

from ScrolledText import ScrolledText
import tkFileDialog
import os

from hydratk.utils import fix_path

class Editor(tk.LabelFrame):

    _instance = None
    _instance_created = False

    _root = None
    _trn = None
    _logger = None
    _explorer = None
    _nb = None

    def __init__(self, root):

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self._root = root
        self._trn = self._root._trn
        tk.LabelFrame.__init__(self, root._pane_right, text=self._trn.msg('htk_gui_editor_label'))
        self.set_gui()

    @staticmethod
    def get_instance(root=None):

        if (Editor._instance is None):
            Editor._instance_created = True
            Editor._instance = Editor(root)

        return Editor._instance

    def set_ref(self):

        self._logger = self._root._frame_logger
        self._explorer = self._root._frame_explorer

    def set_gui(self):

        self._nb = CustomNotebook(self, height=650)
        self._nb.pack(expand=True, fill=tk.BOTH, padx=2, pady=3)

    def new_file(self):

        self._nb._new_cnt += 1
        tab_text = '{0}_{1}.txt'.format(self._trn.msg('htk_gui_editor_tab_new_text'), self._nb._new_cnt)
        self._nb.add_tab(text=tab_text)
        
    def open_file(self, event=None, path=None):
        
        if (path is None):
            path = tkFileDialog.askopenfilename(filetypes=[(self._trn.msg('htk_gui_editor_filetypes'), '*.*')])
            if (len(path) == 0):
                return

        path = fix_path(path)
        name = os.path.split(path)[1]
        res, idx = self._nb.is_tab_present(path)
        if (not res):
            with open(path, 'r') as f:
                self._nb.add_tab(path=path, content=f.read(), text=name)
                self._logger.debug(self._trn.msg('htk_core_file_opened', path))
        else:
            self._nb.select(idx)
            
    def save_as_file(self, event=None):

        path = tkFileDialog.asksaveasfilename(filetypes=[(self._trn.msg('htk_gui_editor_filetypes'), '*.*')])
        if (len(path) == 0):
            return

        with open(path, 'w') as f:
            f.write(self._nb.get_current_content())
            self._logger.debug(self._trn.msg('htk_core_file_saved', path))
            name = os.path.split(path)[1]
            self._nb.set_current_tab(name, path)
            self._explorer.refresh(path=path)
            
    def save_file(self, event=None):

        path = self._nb.get_current_tab()._path
        if (path is None):
            self.save_as_file()
        else:
            with open(path, 'w') as f:
                f.write(self._nb.get_current_content())
                self._logger.debug(self._trn.msg('htk_core_file_saved', path))

class CustomNotebook(ttk.Notebook):

    __initialized = False
    _parent = None
    _tabs = []
    _new_cnt = 0

    def __init__(self, parent, *args, **kwargs):

        if (not self.__initialized):
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs['style'] = 'CustomNotebook'
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self._parent = parent
        self.set_gui()

    def __initialize_custom_style(self):

        style = ttk.Style()
        imgdir = os.path.join(os.path.dirname(__file__), 'img')
        self.images = (
            tk.PhotoImage('img_close', file=os.path.join(imgdir, 'close.gif')),
            tk.PhotoImage('img_closeactive', file=os.path.join(imgdir, 'close_active.gif'))
        )

        style.element_create('close', 'image', 'img_close',
                            ('active', '!disabled', 'img_closeactive'), border=8, sticky='')
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
        
    def set_gui(self):

        self.enable_traversal()
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Control-F4>', self.close_tab)

    def is_tab_present(self, path):

        res, idx = False, None
        for i in range(0, len(self._tabs)):
            if (self._tabs[i]._path == path):
                res, idx = True, i

        return res, idx

    def add_tab(self, path=None, content=None, **kwargs):
        
        tab = FileTab(self, kwargs['text'], path, content)
        self._tabs.append(tab)
        self.add(tab, **kwargs)
        self.select(len(self._tabs) - 1)
        
        if (len(self._tabs) == 1):
            self._parent._root._menu_file.entryconfig(2, state=tk.NORMAL)
            self._parent._root._menu_file.entryconfig(3, state=tk.NORMAL)

    def get_current_index(self):

        return self.index(self.select())

    def get_current_tab(self):

        return self._tabs[self.get_current_index()]

    def get_current_content(self):

        return self._tabs[self.get_current_index()]._text.get(1.0, 'end-1c')
    
    def set_current_tab(self, name, path):

        idx = self.get_current_index()
        self.tab(idx, text=name)
        self._tabs[idx]._name = name
        self._tabs[idx]._path = path

    def on_release(self, event=None):

        if (event.widget.identify(event.x, event.y) == 'close'):
            index = self.index('@%d,%d' % (event.x, event.y))
            self.close_tab(index=index)

    def close_tab(self, event=None, index=None):
        
        if (index is None):
            index = self.get_current_index()

        self.forget(index)
        self.event_generate('<<NotebookTabClosed>>')
        del self._tabs[index]

        if (len(self._tabs) == 0):
            self._parent._root._menu_file.entryconfig(2, state=tk.DISABLED)
            self._parent._root._menu_file.entryconfig(3, state=tk.DISABLED)

class FileTab(tk.Frame):

    _parent = None
    _name = None
    _path = None

    def __init__(self, parent, name, path=None, content=None):

        tk.Frame.__init__(self)
        self._parent = parent
        self._name = name
        self._path = path

        self.set_gui(content)

    def set_gui(self, content=None):

        self._text = ScrolledText(self)
        self._text.pack(expand=True, fill=tk.BOTH)
        self._text.focus_set()

        if (content != None):
            self._text.insert(tk.END, content)

        self._text.bind('<Control-F4>', self._parent.close_tab)
