# -*- coding: utf-8 -*-
"""Editor frame

.. module:: editor
   :platform: Windows
   :synopsis: Editor frame
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

from hydratk.notebook import CustomNotebook
from hydratk.utils import fix_path

class Editor(tk.LabelFrame):
    """Class Explorer
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None
    _config = None
    _logger = None
    _explorer = None
    _colorizer = None
    _formatter = None

    # gui elements
    _nb = None
    _show_line_number = None
    _show_info_bar = None

    # font
    _font_family = None
    _font_size = None
    _font_style = None

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
        self._trn = self.root.trn
        self._config = self.root.cfg

        tk.LabelFrame.__init__(self, root._pane_right, text=self.trn.msg('htk_gui_editor_label'))
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

        if (Editor._instance is None):
            Editor._instance_created = True
            Editor._instance = Editor(root)

        return Editor._instance

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
    def logger(self):
        """ logger property getter """

        return self._logger

    @property
    def explorer(self):
        """ explorer property getter """

        return self._explorer

    @property
    def colorizer(self):
        """ colorizer property getter """

        return self._colorizer

    @property
    def formatter(self):
        """ formatter property getter """

        return self._formatter

    @property
    def nb(self):
        """ nb property getter """

        return self._nb

    def set_late_ref(self):
        """Method sets references to frames initialized later

        Args:
            none

        Returns:
            void

        """

        self._logger = self.root.logger
        self._explorer = self.root.explorer
        self._colorizer = self.root.colorizer
        self._formatter = self.root.formatter

    def _parse_config(self):
        """Method parses configuration

        Args:
            none

        Returns:
            void

        """

        self._show_line_number = tk.BooleanVar(value=True) if (self.config._data['Core']['show_line_number'] == 1) else tk.BooleanVar(value=False)
        self._show_info_bar = tk.BooleanVar(value=True) if (self.config._data['Core']['show_info_bar'] == 1) else tk.BooleanVar(value=False)

        self._font_family = self._config._data['Core']['font']['family']
        self._font_size = self._config._data['Core']['font']['size']
        self._font_style = self._config._data['Core']['font']['style']

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self._nb = CustomNotebook(self, height=650)
        self._nb.pack(expand=True, fill=tk.BOTH, padx=2, pady=3)

    def new_file(self, event=None):
        """Method opens new file tab

        Args:
            event (obj): event

        Returns:
            void

        """

        self.nb.new_cnt += 1
        tab_text = '{0}_{1}.txt'.format(self.trn.msg('htk_gui_editor_tab_new_text'), self.nb.new_cnt)
        self.nb.add_tab(text=tab_text)
        
    def open_file(self, event=None, path=None):
        """Method opens file

        File is opened from dialog or path, the content is displayed in tab

        Args:
            event (obj): event
            path (str): file path

        Returns:
            void

        """

        if (path is None):
            path = tkFileDialog.askopenfilename(filetypes=[(self.trn.msg('htk_gui_editor_filetypes'), '*.*')])
            if (len(path) == 0):
                return

        path = fix_path(path)
        name = os.path.split(path)[1]
        res, idx = self.nb.is_tab_present(path)
        if (not res):
            with open(path, 'r') as f:
                self.nb.add_tab(path=path, content=f.read(), text=name)
                self.logger.debug(self.trn.msg('htk_core_file_opened', path))
        else:
            self.nb.select(idx)

    def save_as_file(self, event=None):
        """Method saves new file as

        Choose file name in dialog, content is stored to file

        Args:
            event (obj): event

        Returns:
            void

        """

        path = tkFileDialog.asksaveasfilename(filetypes=[(self.trn.msg('htk_gui_editor_filetypes'), '*.*')])
        if (len(path) == 0):
            return

        with open(path, 'w') as f:
            f.write(self.nb.get_current_content())
            self.logger.debug(self.trn.msg('htk_core_file_saved', path))
            name = os.path.split(path)[1]
            self.nb.set_current_tab(name, path, False)
            self.explorer.refresh(path=path)
            
    def save_file(self, event=None, path=None, idx=None):
        """Method saves file

        From current tab, file path or requested tab

        Args:
            event (obj): event
            path (str): file path
            idx (int): tab index

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            if (path is None):
                path = tab.path
            if (path is None):
                self.save_as_file()
            else:
                with open(path, 'w') as f:
                    content = self.nb.get_current_content() if (idx is None) else self._nb.get_content(idx)
                    f.write(content)
                    self.logger.debug(self.trn.msg('htk_core_file_saved', path))
                    tab.text.edit_modified(False)

    def undo(self, event=None):
        """Method undos last text change

        Args:
            event (obj): event

        Returns:
            void

        """

        try:
            tab = self.nb.get_current_tab()
            if (tab is not None):
                tab.text.edit_undo()
                tab.update_line_numbers()
        except tk.TclError:
            pass

    def redo(self, event=None):
        """Method redos next text change

        Args:
            event (obj): event

        Returns:
            void

        """

        try:
            tab = self.nb.get_current_tab()
            if (tab is not None):
                tab.text.edit_redo()
                tab.update_line_numbers()
        except tk.TclError:
            pass

    def cut(self, event=None):
        """Method cuts marked text and stores it in clipboard

        Args:
            event (obj): event

        Returns:
            void

        """

        content = self.nb.get_marked_content()
        if (content is not None):
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            tab = self.nb.get_current_tab()
            tab.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            tab.update_line_numbers()

    def copy(self, event=None):
        """Method copies marked text and stores it in clipboard

        Args:
            event (obj): event

        Returns:
            void

        """

        content = self.nb.get_marked_content()
        if (content is not None):
            self.root.clipboard_clear()
            self.root.clipboard_append(content)

    def paste(self, event=None):
        """Method pastes text from clipboard

        Args:
            event (obj): event

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            content = self.root.clipboard_get()
            start = tab._text.index(tk.INSERT)
            stop = '{0}+{1}c'.format(start, len(content))
            tab.text.insert(tk.INSERT, content)
            tab.update_line_numbers()
            tab.colorize(start, stop)
            return 'break'

    def delete(self, event=None):
        """Method deletes marked text

        Args:
            event (obj): event

        Returns:
            void

        """

        content = self.nb.get_marked_content()
        if (content is not None):
            tab = self.nb.get_current_tab()
            tab.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            tab.update_line_numbers()

    def select_all(self, event=None):
        """Method marks tab text content

        Args:
            event (obj): event

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            tab.text.tag_add(tk.SEL, '1.0', 'end')

    def save_tabs(self):
        """Method saves all tab content

        Dialog is displayed for new files

        Args:
            event (obj): event

        Returns:
            void

        """

        for i in range(0, len(self.nb._tabs)):
            tab = self.nb._tabs[i]
            if (tab.text.edit_modified()):
                res = tkMessageBox.askyesno(self.trn.msg('htk_gui_editor_close_save_title'),
                                            self.trn.msg('htk_gui_editor_close_save_question', tab.name))
                if (res):
                    self.save_file(path=tab.path, idx=i)

    def show_line_number(self, event=None):
        """Method enables/disables showing of line numbers

        Args:
            event (obj): event

        Returns:
            void

        """

        for tab in self.nb._tabs:
            tab.update_line_numbers()

        self.config.data['View']['show_line_number'] = 1 if (self._show_line_number.get()) else 0

    def show_info_bar(self, event=None):
        """Method enables/disables showing of info bar

        Args:
            event (obj): event

        Returns:
            void

        """
        
        for tab in self.nb._tabs:
            tab.update_info_bar()

        self.config.data['View']['show_info_bar'] = 1 if (self._show_info_bar.get()) else 0
        
    def win_goto(self, event=None):
        """Method displays Goto window

        Args:
            event (obj): event

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            win = tk.Toplevel(self._root)
            win.title(self.trn.msg('htk_gui_editor_goto_title'))
            win.transient(self._root)
            win.resizable(False, False)
            win.geometry('+%d+%d' % (self._root.winfo_screenwidth() / 2, self._root.winfo_screenheight() / 2))

            tk.Label(win, text=self.trn.msg('htk_gui_editor_goto_text')).pack(side=tk.LEFT, padx=3)
            entry = tk.Entry(win, width=15)
            entry.pack(side=tk.LEFT, padx=3)
            entry.focus_set()
            btn = tk.Button(win, text='OK', command=lambda: self.goto(entry.get(), win))
            btn.pack(side=tk.LEFT, padx=3)

            win.bind('<Return>', lambda f: self.goto(entry.get(), win))
            win.bind('<Escape>', lambda f: win.destroy())

    def goto(self, line, win=None):
        """Method goes to given line

        Args:
            line (int): line number
            win (obj): window reference

        Returns:
            void

        """

        if (len(line) > 0):
            tab = self.nb.get_current_tab()
            tab.goto(line)

        if (win is not None):
            win.destroy()

    def win_find(self, event=None):
        """Method displays Find window

        Args:
            event (obj): event

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            win = tk.Toplevel(self._root)
            win.title(self.trn.msg('htk_gui_editor_find_title'))
            win.transient(self._root)
            win.resizable(False, False)
            win.geometry('+%d+%d' % (self._root.winfo_screenwidth() / 2, self._root.winfo_screenheight() / 2))

            tk.Label(win, text=self.trn.msg('htk_gui_editor_find_text')).grid(row=0, column=0, sticky='e')
            entry = tk.Entry(win, width=50)
            entry.grid(row=0, column=1, padx=3, sticky='e')
            entry.focus_set()

            find_all = tk.BooleanVar(value=True)
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_find_find_all'), variable=find_all).grid(row=1, column=1, pady=3, sticky='w')
            ignore_case = tk.BooleanVar(value=True)
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_find_ignore_case'), variable=ignore_case).grid(row=2, column=1, sticky='w')
            regexp = tk.BooleanVar()
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_find_regexp'), variable=regexp).grid(row=3, column=1, sticky='w')

            btn = tk.Button(win, text='OK', command=lambda: self.find(entry.get(), find_all.get(), ignore_case.get(), regexp.get(), win))
            btn.grid(row=0, column=2, padx=3, sticky='e')

            win.bind('<Return>', lambda f: self.find(entry.get(), find_all.get(), ignore_case.get(), regexp.get(), win))
            win.bind('<Escape>', lambda f: win.destroy())

    def find(self, find_str, find_all, ignore_case, regexp, win=None):
        """Method finds given string and highlights it

        Args:
            find_str (str): string to find
            find_all (bool): find all occurrences, otherwise only next one
            ignore_case (bool): ignore case
            regexp (bool): regular expression
            win (obj): window reference

        Returns:
            void

        """

        if (len(find_str) > 0):
            tab = self.nb.get_current_tab()
            tab.find(find_str=find_str, find_all=find_all, ignore_case=ignore_case, regexp=regexp)

        if (win is not None):
            win.destroy()

    def win_replace(self, event=None):
        """Method displays Replace window

        Args:
            event (obj): event

        Returns:
            void

        """

        tab = self.nb.get_current_tab()
        if (tab is not None):
            win = tk.Toplevel(self._root)
            win.title(self.trn.msg('htk_gui_editor_replace_title'))
            win.transient(self._root)
            win.resizable(False, False)
            win.geometry('+%d+%d' % (self._root.winfo_screenwidth() / 2, self._root.winfo_screenheight() / 2))

            tk.Label(win, text=self.trn.msg('htk_gui_editor_replace_find')).grid(row=0, column=0, sticky='e')
            find_entry = tk.Entry(win, width=50)
            find_entry.grid(row=0, column=1, padx=3, sticky='e')
            find_entry.focus_set()

            tk.Label(win, text=self.trn.msg('htk_gui_editor_replace_replace')).grid(row=1, column=0, pady=3, sticky='e')
            replace_entry = tk.Entry(win, width=50)
            replace_entry.grid(row=1, column=1, padx=3, sticky='e')

            replace_all = tk.BooleanVar(value=True)
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_replace_replace_all'), variable=replace_all).grid(row=2, column=1, pady=3, sticky='w')
            ignore_case = tk.BooleanVar(value=True)
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_replace_ignore_case'), variable=ignore_case).grid(row=3, column=1, sticky='w')
            regexp = tk.BooleanVar()
            tk.Checkbutton(win, text=self.trn.msg('htk_gui_editor_replace_regexp'), variable=regexp).grid(row=4, column=1, sticky='w')

            btn = tk.Button(win, text='OK', command=lambda: self.replace(find_entry.get(), replace_entry.get(), replace_all.get(), ignore_case.get(), regexp.get(), win))
            btn.grid(row=0, column=2, padx=3, sticky='e')

            win.bind('<Return>', lambda f: self.replace(find_entry.get(), replace_entry.get(), replace_all.get(), ignore_case.get(), regexp.get(), win))
            win.bind('<Escape>', lambda f: win.destroy())
            
    def replace(self, find_str, replace_str, replace_all, ignore_case, regexp, win=None):
        """Method finds given string and replaces it

        Args:
            find_str (str): string to find
            replace_str (str): string to replace
            replace_all (bool): replace all occurrences, otherwise only next one
            ignore_case (bool): ignore case
            regexp (bool): regular expression
            win (obj): window reference

        Returns:
            void

        """

        if (len(find_str) > 0):
            tab = self.nb.get_current_tab()
            tab.replace(find_str, replace_str, replace_all, ignore_case, regexp)

        if (win is not None):
            win.destroy()
            return 'break'

    def increase_font(self):
        """Method increases font size

        Args:
            none

        Returns:
            void

        """
        
        if (self._font_size < 50):
            self._font_size += 1
            for tab in self.nb._tabs:
                tab.set_font(self._font_family, self._font_size, self._font_style)
        
    def decrease_font(self):
        """Method decreases font size

        Args:
            none

        Returns:
            void

        """

        if (self._font_size > 1.0):
            self._font_size -= 1
            for tab in self.nb._tabs:
                tab.set_font(self._font_family, self._font_size, self._font_style)
