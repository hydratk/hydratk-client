# -*- coding: utf-8 -*-
"""Project explorer

.. module:: explorer
   :platform: Windows
   :synopsis: Project explorer
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from sys import version_info

if (version_info[0] == 2):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk

import tkFileDialog
import tkMessageBox
import os
from shutil import rmtree, copy

from hydratk.utils import fix_path

class Explorer(tk.LabelFrame):
    
    _instance = None
    _instance_created = False

    _root = None
    _trn = None
    _config = None
    _editor = None
    _logger = None
    _projects = None
    
    _tree = None
    _vsb = None
    _hsb = None

    _menu = None
    _menu_new = None

    def __init__(self, root):
        
        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self._root = root
        self._trn = self._root._trn
        tk.LabelFrame.__init__(self, root._pane_left, text=self._trn.msg('htk_gui_explorer_label'))
        self.set_gui()

        self._config = self._root._config
        self._projects = self._config.data['Projects'] if ('Projects' in self._config.data and self._config.data['Projects'] != None) else {}
        self.populate_projects()

    @staticmethod
    def get_instance(root=None):

        if (Explorer._instance is None):
            Explorer._instance_created = True
            Explorer._instance = Explorer(root)

        return Explorer._instance

    def set_ref(self):

        self._editor = self._root._frame_editor
        self._logger = self._root._frame_logger

        self._menu_new.entryconfig(0, command=self._editor.new_file)

    def set_gui(self):

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(self, columns=('path', 'type'), show='tree', displaycolumns=(), height=20,
                                  xscrollcommand=lambda f, l: self.autoscroll(self._hsb, f, l),
                                  yscrollcommand=lambda f, l: self.autoscroll(self._vsb, f, l))
        self._tree.pack()
        self._tree.grid(in_=self, row=0, column=0, sticky=tk.NSEW)

        self._vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)
        self._vsb.pack()
        self._vsb.grid(in_=self, row=0, column=1, sticky=tk.NS)
        self._hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._tree.xview)
        self._hsb.pack()
        self._hsb.grid(in_=self, row=1, column=0, sticky=tk.EW)

        self._tree['yscroll'] = self._vsb.set
        self._tree['xscroll'] = self._hsb.set
        self._tree.heading('#0', text='File', anchor='w')
        self._tree.column('#0', stretch=True, minwidth=300, width=250)

        self._tree.bind('<<TreeviewOpen>>', self.update_tree)
        self._tree.bind('<Double-1>', self.open)
        self._tree.bind('<Control-c>', self.copy)
        self._tree.bind('<Control-v>', self.paste)
        self._tree.bind('<Delete>', self.delete)
        self._tree.bind('<F5>', self.refresh)

        self.set_menu()

    def set_menu(self):

        self._menu = tk.Menu(self._tree, tearoff=False)
        self._menu_new = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self._trn.msg('htk_gui_explorer_menu_new'), menu=self._menu_new)
        self._menu_new.add_command(label=self._trn.msg('htk_gui_explorer_menu_new_file'))
        self._menu_new.add_command(label=self._trn.msg('htk_gui_explorer_menu_new_directory'), command=self.new_directory)
        self._menu_new.add_command(label=self._trn.msg('htk_gui_explorer_menu_new_project'), command=self.new_project)
        self._menu.add_command(label=self._trn.msg('htk_gui_explorer_menu_open'), accelerator='Ctrl+O', command=self.open)
        self._menu.add_command(label=self._trn.msg('htk_gui_explorer_menu_copy'), accelerator='Ctrl+C', command=self.copy)
        self._menu.add_command(label=self._trn.msg('htk_gui_explorer_menu_paste'), accelerator='Ctrl+V', command=self.paste)
        self._menu.add_command(label=self._trn.msg('htk_gui_explorer_menu_delete'), accelerato='Del', command=self.delete)
        self._menu.add_command(label=self._trn.msg('htk_gui_explorer_menu_refresh'), accelerator='F5', command=self.refresh)

        self._tree.bind('<Button-3>', self.context_menu)

    def autoscroll(self, sbar, first, last):

        first, last = float(first), float(last)
        if (first <= 0 and last >= 1):
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def context_menu(self, event):

        self._menu.post(event.x_root, event.y_root)
    
    def populate_projects(self):

        for name, cfg in self._projects.items():
            self.populate_project(name, cfg)

    def populate_project(self, name, cfg):
        
        node = self._tree.insert('', 'end', text=name, values=(cfg['path'], 'directory'))
        self.populate_tree(node)        

    def populate_tree(self, node):
        
        if self._tree.set(node, 'type') != 'directory':
            return

        path = self._tree.set(node, 'path')
        if (len(path) == 0):
            return

        self._tree.delete(*self._tree.get_children(node))

        for p in os.listdir(path):
            ptype = None
            p = os.path.join(path, p)
            if (os.path.isdir(p)):
                ptype = 'directory'
            elif (os.path.isfile(p)):
                ptype = 'file'

            fname = os.path.split(p)[1]
            id = self._tree.insert(node, 'end', text=fname, values=(fix_path(p), ptype))

            if (ptype == 'directory'):
                self._tree.insert(id, 'end')
                self._tree.item(id, text=fname)
            elif (ptype == 'file'):
                self._tree.set(id)

    def update_tree(self, event):

        self._tree = event.widget
        self.populate_tree(self._tree.focus())

    def new_project(self):
        
        dirpath = tkFileDialog.askdirectory()
        proj_name = os.path.split(dirpath)[1]
        if (len(proj_name) == 0 or proj_name in self._projects):
            return

        self._projects[proj_name] = {'path': dirpath}
        node = self._tree.insert('', 'end', text=proj_name, values=(dirpath, 'directory'))
        self.populate_tree(node)
        self._logger.info(self._trn.msg('htk_core_project_created', proj_name))
        self._config.data['Projects'] = self._projects
        self._config.save()
        
    def new_directory(self):

        path = tkFileDialog.askdirectory()
        if (len(path) == 0):
            return

        self._logger.debug(self._trn.msg('htk_core_directory_created', path))
        self.refresh(path=path)

    def open(self, event=None):
        
        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        if (item['values'][1] == 'file'):
            self._editor.open_file(path=item['values'][0])
            
    def copy(self, event=None):

        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        self._root.clipboard_clear()
        self._root.clipboard_append(item['values'][0])

    def paste(self, event=None):

        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        path, item_type = item['values']
        if (item_type == 'directory'):
            src = self._root.clipboard_get()
            copy(self._root.clipboard_get(), path)
            self._logger.debug(self._trn.msg('htk_core_copied', src, path))
            self.refresh(path=path)

    def delete(self, event=None):

        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        path, item_type = item['values']
        path = fix_path(path)
        if (item_type == 'file'):
            question = 'htk_gui_explorer_delete_file'
        else:
            is_project, i = False, 0
            for name, cfg in self._projects.items():
                if (cfg['path'] == path):
                    is_project, proj_name = True, name
                    break
                i += 1
            question = 'htk_gui_explorer_delete_project' if (is_project) else 'htk_gui_explorer_delete_directory'
        
        res = tkMessageBox.askyesno(self._trn.msg('htk_gui_explorer_delete'), self._trn.msg(question, path))
        if (res):
            if (item_type == 'file'):
                os.remove(path)
                self._logger.debug(self._trn.msg('htk_core_file_deleted', path))
                self.refresh(path)
            else:
                rmtree(path)
                if (is_project):
                    self._logger.info(self._trn.msg('htk_core_project_deleted', proj_name))
                    self._tree.delete(self._tree.get_children()[i])
                    del self._projects[proj_name]
                    self._config.data['Projects'] = self._projects
                    self._config.save()
                else:
                    self._logger.debug(self._trn.msg('htk_core_directory_deleted', path))
                    self.refresh(path)

    def refresh(self, event=None, path=None):

        if (path is None):
            item = self._tree.selection()
            if (len(item) == 0):
                return
            path = self._tree.item(item)['values'][0]

        i = 0
        path = fix_path(path)
        for name, cfg in self._projects.items():
            if (cfg['path'] + '/' in path or cfg['path'] == path):
                node = self._tree.get_children()[i]
                self.populate_tree(node)
                break
            i += 1
