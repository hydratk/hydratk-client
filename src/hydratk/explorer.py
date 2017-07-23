# -*- coding: utf-8 -*-
"""Project explorer frame

.. module:: explorer
   :platform: Windows
   :synopsis: Project explorer frame
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
    """Class Explorer
    """
    
    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None
    _config = None
    _editor = None
    _logger = None

    # project parameters
    _projects = None
    
    # gui elements
    _tree = None
    _vsb = None
    _hsb = None

    _menu = None
    _menu_new = None

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

        tk.LabelFrame.__init__(self, root._pane_left, text=self.trn.msg('htk_gui_explorer_label'))
        self._set_gui()
        self._parse_config()

    @staticmethod
    def get_instance(root=None):
        """Method gets Explorer singleton instance

        Args:
            root (obj): root frame

        Returns:
            obj

        """

        if (Explorer._instance is None):
            Explorer._instance_created = True
            Explorer._instance = Explorer(root)

        return Explorer._instance

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
    def editor(self):
        """ editor property getter """

        return self._editor

    @property
    def logger(self):
        """ logger property getter """

        return self._logger

    @property
    def projects(self):
        """ projects property getter """

        return self._projects

    @property
    def tree(self):
        """ tree property getter """

        return self._tree

    def set_late_ref(self):
        """Method sets references to frames initialized later

        Args:
            none

        Returns:
            void

        """

        self._editor = self.root.editor
        self._logger = self.root.logger

        self._menu_new.entryconfig(0, command=self._editor.new_file)

    def _parse_config(self):
        """Method parses configuration

        Args:
            none

        Returns:
            void

        """

        self._projects = self._config.data['Projects'] if ('Projects' in self._config.data and self._config.data['Projects'] != None) else {}
        self.populate_projects()

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # treeview
        self._tree = ttk.Treeview(self, columns=('path', 'type'), show='tree', displaycolumns=(), height=20,
                                  xscrollcommand=lambda f, l: self._autoscroll(self._hsb, f, l),
                                  yscrollcommand=lambda f, l: self._autoscroll(self._vsb, f, l))
        self._tree.pack()
        self._tree.grid(in_=self, row=0, column=0, sticky=tk.NSEW)

        # scrollbars
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

        # events
        self._tree.bind('<<TreeviewOpen>>', self._update_tree)
        self._tree.bind('<Double-1>', self.open)
        self._tree.bind('<Control-c>', self.copy)
        self._tree.bind('<Control-v>', self.paste)
        self._tree.bind('<Delete>', self.delete)
        self._tree.bind('<F5>', self.refresh)

        self._set_menu()

    def _set_menu(self):
        """Method sets menu

        Args:
            none

        Returns:
            void

        """

        self._menu = tk.Menu(self._tree, tearoff=False)
        self._menu_new = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self.trn.msg('htk_gui_explorer_menu_new'), menu=self._menu_new)
        self._menu_new.add_command(label=self.trn.msg('htk_gui_explorer_menu_new_file'), accelerator='Ctrl+N')
        self._menu_new.add_command(label=self.trn.msg('htk_gui_explorer_menu_new_directory'), command=self.new_directory)
        self._menu_new.add_command(label=self.trn.msg('htk_gui_explorer_menu_new_project'), command=self.new_project)
        self._menu.add_command(label=self.trn.msg('htk_gui_explorer_menu_open'), accelerator='Ctrl+O', command=self.open)
        self._menu.add_command(label=self.trn.msg('htk_gui_explorer_menu_copy'), accelerator='Ctrl+C', command=self.copy)
        self._menu.add_command(label=self.trn.msg('htk_gui_explorer_menu_paste'), accelerator='Ctrl+V', command=self.paste)
        self._menu.add_command(label=self.trn.msg('htk_gui_explorer_menu_delete'), accelerato='Delete', command=self.delete)
        self._menu.add_command(label=self.trn.msg('htk_gui_explorer_menu_refresh'), accelerator='F5', command=self.refresh)

        self._tree.bind('<Button-3>', self._context_menu)

    def _autoscroll(self, sbar, idx1, idx2):
        """Method for automatic treeview scroll

        Args:
            sbar (obj): scrollbar
            idx1 (int): start index
            idx2 (int): stop index

        Returns:
            void

        """

        idx1, idx2 = float(idx1), float(idx2)
        if (idx1 <= 0 and idx2 >= 1):
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(idx1, idx2)

    def _context_menu(self, event=None):
        """Method sets context menu

        Args:
            event (obj): event

        Returns:
            void

        """

        self._menu.post(event.x_root, event.y_root)
    
    def populate_projects(self):
        """Method populates all projects

        Args:
            none

        Returns:
            void

        """

        for name, cfg in self._projects.items():
            self.populate_project(name, cfg)

    def populate_project(self, name, cfg):
        """Method populates given project

        Args:
            name (str): project name
            cfg (dict): project configuration

        Returns:
            void

        """
        
        node = self._tree.insert('', 'end', text=name, values=(cfg['path'], 'directory'))
        self._populate_tree(node)

    def _populate_tree(self, node):
        """Method populates project tree

        It displays directory and file name, path is hidden
        Directory is can be expanded/collapsed

        Args:
            node (obj): tree node

        Returns:
            void

        """
        
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

    def _update_tree(self, event=None):
        """Method updates tree

        Args:
            event (obj): event

        Returns:
            void

        """

        self._tree = event.widget
        self._populate_tree(self._tree.focus())

    def new_project(self):
        """Method creates new project

        File dialog is displayed, choose existing directory or create new one
        Project is stored to configuration

        Args:
            none

        Returns:
            void

        """
        
        dirpath = tkFileDialog.askdirectory()
        proj_name = os.path.split(dirpath)[1]
        if (len(proj_name) == 0 or proj_name in self._projects):
            return

        self._projects[proj_name] = {'path': dirpath}
        node = self._tree.insert('', 'end', text=proj_name, values=(dirpath, 'directory'))
        self._populate_tree(node)
        self._logger.info(self.trn.msg('htk_core_project_created', proj_name))
        self._config.data['Projects'] = self._projects
        self._config.save()
        
    def new_directory(self):
        """Method creates new directory

        File dialog is displayed, create new directory

        Args:
            none

        Returns:
            void

        """

        path = tkFileDialog.askdirectory()
        if (len(path) == 0):
            return

        self._logger.debug(self.trn.msg('htk_core_directory_created', path))
        self.refresh(path=path)

    def open(self, event=None):
        """Method opens file from explorer tree

        Args:
            event (obj): event

        Returns:
            void

        """
        
        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        if (item['values'][1] == 'file'):
            self._editor.open_file(path=item['values'][0])
            
    def copy(self, event=None):
        """Method copies file or directory from explorer tree

        Args:
            event (obj): event

        Returns:
            void

        """

        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        self._root.clipboard_clear()
        self._root.clipboard_append(item['values'][0])

    def paste(self, event=None):
        """Method pastes file or directory from explorer tree

        Args:
            event (obj): event

        Returns:
            void

        """

        item = self._tree.selection()
        if (len(item) == 0):
            return

        item = self._tree.item(item)
        path, item_type = item['values']
        if (item_type == 'directory'):
            src = self._root.clipboard_get()
            copy(self._root.clipboard_get(), path)
            self._logger.debug(self.trn.msg('htk_core_copied', src, path))
            self.refresh(path=path)

    def delete(self, event=None):
        """Method deletes file or directory from explorer tree

        Deletion must be confirmed via popup window
        Deleted project is removed from configuration

        Args:
            event (obj): event

        Returns:
            void

        """

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
        
        res = tkMessageBox.askyesno(self.trn.msg('htk_gui_explorer_delete'), self.trn.msg(question, path))
        if (res):
            if (item_type == 'file'):
                os.remove(path)
                self._logger.debug(self.trn.msg('htk_core_file_deleted', path))
                self.refresh(path)
            else:
                rmtree(path)
                if (is_project):
                    self._logger.info(self.trn.msg('htk_core_project_deleted', proj_name))
                    self._tree.delete(self._tree.get_children()[i])
                    del self._projects[proj_name]
                    self._config.data['Projects'] = self._projects
                    self._config.save()
                else:
                    self._logger.debug(self.trn.msg('htk_core_directory_deleted', path))
                    self.refresh(path)

    def refresh(self, event=None, path=None):
        """Method refreshes explorer tree if content is changed

        Args:
            event (obj): event
            path (str): directory of file path

        Returns:
            void

        """

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
                self._populate_tree(node)
                break
            i += 1
