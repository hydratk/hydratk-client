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

import ttk
import tkFileDialog
import tkMessageBox
import os

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

    # gui elements
    _nb = None
    _show_line_number = None
    _show_info_bar = None

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

    def _parse_config(self):
        """Method parses configuration

        Args:
            none

        Returns:
            void

        """

        self._show_line_number = tk.BooleanVar(value=True) if (self.config._data['View']['show_line_number'] == 1) else tk.BooleanVar(value=False)
        self._show_info_bar = tk.BooleanVar(value=True) if (self.config._data['View']['show_info_bar'] == 1) else tk.BooleanVar(value=False)

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
            tab.text.insert(tk.INSERT, self.root.clipboard_get())
            tab.update_line_numbers()

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

    def goto(self, line, win=None):
        """Method highlights given line

        Args:
            line (int): line number
            win (obj): window reference

        Returns:
            void

        """

        if (len(line) > 0):
            tab = self.nb.get_current_tab()
            tab.text.mark_set(tk.INSERT, '%s.1' % line)
            tab.text.see(tk.INSERT)

        if (win is not None):
            win.destroy()

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

        tools = self.parent.root.tools
        tools['save'].config(state=state)
        tools['undo'].config(state=state)
        tools['redo'].config(state=state)
        tools['cut'].config(state=state)
        tools['copy'].config(state=state)
        tools['paste'].config(state=state)
        tools['delete'].config(state=state)

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

class FileTab(tk.Frame):
    """Class FileTab
    """

    # references
    _parent = None
    _editor = None

    # tab parameters
    _name = None
    _path = None

    # gui elements
    _text = None
    _ln_bar = None
    _info_bar = None
    _vbar = None
    _hbar = None
    _menu = None

    def __init__(self, parent, name, path=None, content=None):
        """Class constructor

        Called when object is initialized

        Args:
           parent (obj): notebook reference
           name (str): file name
           path (str): file path
           content (str): file content

        """

        self._parent = parent
        self._editor = parent.parent

        tk.Frame.__init__(self)
        self._name = name
        self._path = path
        self._set_gui(content)

    @property
    def parent(self):
        """ parent property getter """

        return self._parent

    @property
    def editor(self):
        """ editor property getter """

        return self._editor

    @property
    def text(self):
        """ text property getter """

        return self._text

    @property
    def name(self):
        """ name property getter """

        return self._name

    @property
    def path(self):
        """ path property getter """

        return self._path

    def _set_gui(self, content=None):
        """Method sets graphical interface

        Args:
            content (str): file content

        Returns:
            void

        """

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._vbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)

        # line number bar
        self._ln_bar = tk.Text(self, width=4, padx=3, takefocus=0, state=tk.DISABLED, yscrollcommand=self._vbar.set)
        self._ln_bar.pack(side=tk.LEFT, fill=tk.Y)
        self._ln_bar.grid(in_=self, row=0, column=0, sticky=tk.NSEW)

        # text area
        self._text = tk.Text(self, wrap=tk.NONE, xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._text.pack(expand=True, side=tk.LEFT, fill=tk.BOTH)
        self._text.grid(in_=self, row=0, column=1, sticky=tk.NSEW)

        # scrollbars
        self._vbar.configure(command=self._text.yview)
        self._vbar.pack(side=tk.LEFT, fill=tk.Y)
        self._vbar.grid(in_=self, row=0, column=2, sticky=tk.NS)
        self._hbar.configure(command=self._text.xview)
        self._hbar.pack(side=tk.RIGHT, fill=tk.X)
        self._hbar.grid(in_=self, row=1, column=1, sticky=tk.EW)

        # info bar
        info_text = '1 : 1' if (self._editor._show_info_bar.get()) else ''
        self._info_bar = tk.Label(self._text, text=info_text)
        self._info_bar.pack(side=tk.RIGHT, anchor=tk.SE)

        self._text.focus_set()

        # initial text content
        if (content != None):
            self._text.insert(tk.END, content)
            self._text.edit_modified(False)
            self.update_line_numbers()
            self.update_info_bar()

        # events
        self._text.configure(undo=True)
        self._text.bind('<Control-F4>', self._parent.close_tab)
        self._text.bind('<Any-KeyPress>', self.on_key)
        self._text.bind('<Any-KeyRelease>', self.on_key)
        self._text.bind('<ButtonRelease-1>', self.on_mouse_click)
        self._vbar.configure(command=self.on_vsb)
        self._ln_bar.bind('<MouseWheel>', self.on_mouse_wheel)
        self._text.bind('<MouseWheel>', self.on_mouse_wheel)

        self._set_menu()

    def _set_menu(self):
        """Method sets menu

        Args:
            none

        Returns:
            void

        """

        self._menu = tk.Menu(self._text, tearoff=False)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_undo'), accelerator='Ctrl+Z', command=self.editor.undo)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_redo'), accelerator='Ctrl+Y', command=self.editor.redo)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_cut'), accelerator='Ctrl+X', command=self.editor.cut)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_copy'), accelerator='Ctrl+C', command=self.editor.copy)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_paste'), accelerator='Ctrl+V', command=self.editor.paste)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_delete'), accelerator='Delete', command=self.editor.delete)
        self._menu.add_command(label=self.editor.trn.msg('htk_gui_editor_menu_select_all'), accelerator='Ctrl+A', command=self.editor.select_all)

        self._text.bind('<Button-3>', self.context_menu)

    def context_menu(self, event=None):
        """Method sets context menu

        Args:
            event (obj): event

        Returns:
            void

        """

        self._menu.post(event.x_root, event.y_root)

    def _get_line_numbers(self):
        """Method calculates line numbers for current tab

        Args:
            none

        Returns:
            str

        """

        output = ''
        row, col = self._text.index('end').split('.')
        i = 0
        for i in range(1, int(row) - 1):
            output += str(i) + '\n'

        return output + str(i + 1)

    def update_line_numbers(self, event=None):
        """Method updates line numbers bar after event

        Args:
            event (obj): event

        Returns:
            void

        """

        if (self.editor._show_line_number.get()):
            line_numbers = self._get_line_numbers()
            self._ln_bar.config(state=tk.NORMAL)
            self._ln_bar.delete('1.0', 'end')
            self._ln_bar.insert('1.0', line_numbers)
            self._ln_bar.yview_moveto(self._text.yview()[0])
            self._ln_bar.config(state=tk.DISABLED)
        else:
            self._ln_bar.config(state=tk.NORMAL)
            self._ln_bar.delete('1.0', 'end')
            self._ln_bar.config(state=tk.DISABLED)
        
    def update_info_bar(self, event=None):
        """Method updates info bar after event

        Args:
            event (obj): event

        Returns:
            void

        """
        
        if (self.editor._show_info_bar.get()):
            row, col = self._text.index(tk.INSERT).split('.')
            row, col = str(int(row)), str(int(col) + 1)
            self._info_bar.config(text='{0} : {1}'.format(row, col))
        else:
            self._info_bar.config(text='')
            
    def highlight_line(self, event=None):
        """Method highlits current line

        Args:
            event (obj): event

        Returns:
            void

        """
        
        row, col = self._text.index(tk.INSERT).split('.')
        self._text.tag_remove("highlight", 1.0, "end")
        self._text.tag_add("highlight", row + '.0', row + '.150')
        self._text.tag_configure("highlight", background="bisque")

    def on_key(self, event=None):
        """Method handles key event

        Args:
            event (obj): event

        Returns:
            void

        """

        self.update_line_numbers(event)
        self.update_info_bar(event)
        self.highlight_line(event)

    def on_mouse_click(self, event=None):
        """Method handles mouse click event

        Args:
            event (obj): event

        Returns:
            void

        """

        self.update_info_bar(event)
        self.highlight_line(event)

    def on_vsb(self, *args):
        """Method handles scrollbar event

        Args:
            args (list): arguments

        Returns:
            void

        """

        self._ln_bar.yview(*args)
        self._text.yview(*args)

    def on_mouse_wheel(self, event=None):
        """Method handles mouse wheel event

        Args:
            event (obj): event

        Returns:
            void

        """

        self._ln_bar.yview_scroll(-1 * (event.delta / 120), 'units')
        self._text.yview_scroll(-1 * (event.delta / 120), 'units')
        return 'break'
