# -*- coding: utf-8 -*-
"""Main GUI frame

.. module:: gui
   :platform: Windows
   :synopsis: Main GUI frame
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import sys

if (sys.version_info[0] == 2):
    reload(sys)
    sys.setdefaultencoding('UTF8')
    import Tkinter as tk
else:
    import tkinter as tk

import traceback
import tkMessageBox
from os import path

from hydratk.config import Config
from hydratk.translator import Translator
from hydratk.explorer import Explorer
from hydratk.editor import Editor
from hydratk.logger import Logger

class Gui(tk.Tk):
    """Class Gui
    """

    _instance = None
    _instance_created = False

    # references
    _config = None
    _trn = None
    _explorer = None
    _yoda_tree = None
    _editor = None
    _logger = None

    # frames
    _frame_main = None
    _pane_main = None
    _pane_left = None
    _pane_right = None

    # menu
    _menu = None
    _menu_file = None
    _menu_file_new = None
    _menu_view = None
    _menu_edit = None
    _menu_help = None

    # toolbar
    _tool_bar = None
    _tools = {}
    _images = {}
    _imgdir = None

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

        tk.CallWrapper = ExceptionHandler
        self._config = Config.get_instance()
        self._trn = Translator.get_instance(self._config._data['Core']['language'])

        self._instance = tk.Tk.__init__(self)
        self._set_gui()

    @staticmethod
    def get_instance():
        """Method gets Gui singleton instance

        Args:
            none

        Returns:
            obj

        """

        if (Gui._instance is None):
            Gui._instance_created = True
            Gui._instance = Gui()

        return Gui._instance

    @property
    def cfg(self):
        """ config property getter """

        return self._config

    @property
    def trn(self):
        """ trn property getter """

        return self._trn

    @property
    def explorer(self):
        """ explorer property getter """

        return self._explorer

    @property
    def editor(self):
        """ editor property getter """

        return self._editor

    @property
    def logger(self):
        """ logger property getter """

        return self._logger

    @property
    def tools(self):
        """ tools property getter """

        return self._tools

    @property
    def imgdir(self):
        """ imgdir property getter """

        return self._imgdir

    @property
    def images(self):
        """ images property getter """

        return self._images

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self._set_window()
        self._set_pane_left()
        self._set_pane_right()
        self._set_frame_ref()
        self._set_menu()
        self._set_toolbar()

        self.logger.info(self.trn.msg('htk_core_started'))

    def _set_window(self):
        """Method sets window

        Args:
            none

        Returns:
            void

        """

        self.title('HydraTK')
        self._imgdir = path.join(path.dirname(__file__), 'img')
        self._images['logo'] = tk.PhotoImage(file=path.join(self._imgdir, 'logo.gif'))
        self.tk.call('wm', 'iconphoto', self._w, self._images['logo'])
        self.wm_state('zoomed')
        self.protocol('WM_DELETE_WINDOW', self.exit)

        self._menu = tk.Menu(self)
        self.config(menu=self._menu)

        self._tool_bar = tk.Frame(self)
        self._tool_bar.pack(expand=False, fill=tk.X)

        self._frame_main = tk.Frame(self)
        self._frame_main.pack(expand=True, fill=tk.BOTH)
        self._pane_main = tk.PanedWindow(self._frame_main, orient=tk.HORIZONTAL, sashwidth=10)
        self._pane_main.pack(expand=True, fill=tk.BOTH, padx=10, pady=(6, 10))

    def _set_menu(self):
        """Method sets main menu

        Args:
            none

        Returns:
            void

        """

        self._set_menu_file()
        self._set_menu_edit()
        self._set_menu_view()
        self._set_menu_help()

    def _set_menu_file(self):
        """Method sets file menu

        Args:
            none

        Returns:
            void

        """

        self._menu_file = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self.trn.msg('htk_gui_menu_file'), menu=self._menu_file)

        # submenu new
        self._menu_file_new = tk.Menu(self._menu_file, tearoff=False)
        self._menu_file.add_cascade(label=self.trn.msg('htk_gui_menu_file_new'), menu=self._menu_file_new)
        self._menu_file_new.add_command(label=self.trn.msg('htk_gui_menu_file_new_file'), accelerator='Ctrl+N', command=self.editor.new_file)
        self._menu_file_new.add_command(label=self.trn.msg('htk_gui_menu_file_new_directory'), command=self.explorer.new_directory)
        self._menu_file_new.add_command(label=self.trn.msg('htk_gui_menu_file_new_project'), command=self.explorer.new_project)

        # menu items
        self._menu_file.add_command(label=self.trn.msg('htk_gui_menu_file_open'), accelerator='Ctrl+O', command=self.editor.open_file)
        self._menu_file.add_command(label=self.trn.msg('htk_gui_menu_file_save_as'), command=self.editor.save_as_file, state=tk.DISABLED)
        self._menu_file.add_command(label=self.trn.msg('htk_gui_menu_file_save'), accelerator='Ctrl+S', command=self.editor.save_file, state=tk.DISABLED)
        self._menu_file.add_separator()
        self._menu_file.add_command(label=self.trn.msg('htk_gui_menu_file_exit'), accelerator='Ctrl+Q', command=self.exit)

        # shortcuts
        self.bind('<Control-n>', self.editor.new_file)
        self.bind('<Control-o>', self.editor.open_file)
        self.bind('<Control-s>', self.editor.save_file)
        self.bind('<Control-q>', self.exit)

    def _set_menu_edit(self):
        """Method sets edit menu

        Args:
            none

        Returns:
            void

        """
        
        self._menu_edit = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self.trn.msg('htk_gui_menu_edit'), menu=self._menu_edit)

        # menu items
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_undo'), accelerator='Ctrl+Z', command=self.editor.undo, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_redo'), accelerator='Ctrl+Y', command=self.editor.redo, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_cut'), accelerator='Ctrl+X', command=self.editor.cut, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_copy'), accelerator='Ctrl+C', command=self.editor.copy, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_paste'), accelerator='Ctrl+V', command=self.editor.paste, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_delete'), accelerator='Delete', command=self.editor.delete, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_select_all'), accelerator='Ctrl+A', command=self.editor.select_all, state=tk.DISABLED)
        self._menu_edit.add_command(label=self.trn.msg('htk_gui_menu_edit_goto'), accelerator='Ctrl+G', command=self.editor.win_goto, state=tk.DISABLED)

        # shorcuts
        self.bind('<Control-z>', self.editor.undo)
        self.bind('<Control-y>', self.editor.redo)
        self.bind('<Control-a>', self.editor.select_all)
        self.bind('<Control-g>', self.editor.win_goto)

    def _set_menu_view(self):
        """Method sets view menu

        Args:
            none

        Returns:
            void

        """

        self._menu_view = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self.trn.msg('htk_gui_menu_view'), menu=self._menu_view)

        # menu items
        self._menu_view.add_checkbutton(label=self.trn.msg('htk_gui_menu_view_show_line_number'), variable=self.editor._show_line_number, command=self.editor.show_line_number)
        self._menu_view.add_checkbutton(label=self.trn.msg('htk_gui_menu_view_show_info_bar'), variable=self.editor._show_info_bar, command=self.editor.show_info_bar)

    def _set_menu_help(self):
        """Method sets help menu

        Args:
            none

        Returns:
            void

        """

        self._menu_help = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self.trn.msg('htk_gui_menu_help'), menu=self._menu_help)

    def _set_toolbar(self):
        """Method sets toolbar

        Args:
            none

        Returns:
            void

        """
        
        self._images['new'] = tk.PhotoImage(file=path.join(self._imgdir, 'new.gif'))
        self._images['open'] = tk.PhotoImage(file=path.join(self._imgdir, 'open.gif')),
        self._images['save'] = tk.PhotoImage(file=path.join(self._imgdir, 'save.gif')),
        self._images['undo'] = tk.PhotoImage(file=path.join(self._imgdir, 'undo.gif')),
        self._images['redo'] = tk.PhotoImage(file=path.join(self._imgdir, 'redo.gif')),
        self._images['cut'] = tk.PhotoImage(file=path.join(self._imgdir, 'cut.gif')),
        self._images['copy'] = tk.PhotoImage(file=path.join(self._imgdir, 'copy.gif')),
        self._images['paste'] = tk.PhotoImage(file=path.join(self._imgdir, 'paste.gif')),
        self._images['delete'] = tk.PhotoImage(file=path.join(self._imgdir, 'delete.gif'))

        btn = tk.Button(self._tool_bar, command=self.editor.new_file, image=self._images['new'], relief=tk.FLAT)
        btn.image = self._images['new']
        btn.pack(side=tk.LEFT)
        self._tools['new'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.open_file, image=self._images['open'], relief=tk.FLAT)
        btn.image = self._images['open']
        btn.pack(side=tk.LEFT)
        self._tools['open'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.save_file, state=tk.DISABLED, image=self._images['save'], relief=tk.FLAT)
        btn.image = self._images['save']
        btn.pack(side=tk.LEFT)
        self._tools['save'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.undo, state=tk.DISABLED, image=self._images['undo'], relief=tk.FLAT)
        btn.image = self._images['undo']
        btn.pack(side=tk.LEFT)
        self._tools['undo'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.redo, state=tk.DISABLED, image=self._images['redo'], relief=tk.FLAT)
        btn.image = self._images['redo']
        btn.pack(side=tk.LEFT)
        self._tools['redo'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.cut, state=tk.DISABLED, image=self._images['cut'], relief=tk.FLAT)
        btn.image = self._images['cut']
        btn.pack(side=tk.LEFT)
        self._tools['cut'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.copy, state=tk.DISABLED, image=self._images['copy'], relief=tk.FLAT)
        btn.image = self._images['copy']
        btn.pack(side=tk.LEFT)
        self._tools['copy'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.paste, state=tk.DISABLED, image=self._images['paste'], relief=tk.FLAT)
        btn.image = self._images['paste']
        btn.pack(side=tk.LEFT)
        self._tools['paste'] = btn

        btn = tk.Button(self._tool_bar, command=self.editor.delete, state=tk.DISABLED, image=self._images['delete'], relief=tk.FLAT)
        btn.image = self._images['delete']
        btn.pack(side=tk.LEFT)
        self._tools['delete'] = btn

    def _set_pane_left(self):
        """Method sets left pane

        Args:
            none

        Returns:
            void

        """

        self._pane_left = tk.PanedWindow(self._pane_main, orient=tk.VERTICAL, sashwidth=10, sashrelief=tk.RAISED)
        self._pane_main.add(self._pane_left)
        self._set_explorer()
        self._set_yoda_tree()

    def _set_pane_right(self):
        """Method sets right pane

        Args:
            none

        Returns:
            void

        """

        self._pane_right = tk.PanedWindow(self._pane_main, orient=tk.VERTICAL, sashwidth=10, sashrelief=tk.RAISED)
        self._pane_main.add(self._pane_right)
        self._set_editor()
        self._set_logger()

    def _set_explorer(self):
        """Method sets explorer frame

        Args:
            none

        Returns:
            void

        """

        self.explorer = Explorer.get_instance(self)
        self._pane_left.add(self.explorer)

    def _set_yoda_tree(self):
        """Method sets yoda tree frame

        Args:
            none

        Returns:
            void

        """

        self.yoda_tree = tk.LabelFrame(self._pane_left, text='Yoda tree')
        self._pane_left.add(self.yoda_tree)

    def _set_editor(self):
        """Method sets editor frame

        Args:
            none

        Returns:
            void

        """

        self.editor = Editor.get_instance(self)
        self._pane_right.add(self.editor)

    def _set_logger(self):
        """Method sets logger frame

        Args:
            none

        Returns:
            void

        """

        self.logger = Logger.get_instance(self)
        self._pane_right.add(self.logger)
        
    def _set_frame_ref(self):
        """Method sets frame references

        Args:
            none

        Returns:
            void

        """
        
        self.explorer.set_late_ref()
        self.editor.set_late_ref()

    def exit(self, event=None):
        """Method stops application

        Args:
            event (obj): event

        Returns:
            void

        """

        res = tkMessageBox.askyesno(self.trn.msg('htk_gui_exit_title'), self.trn.msg('htk_gui_exit_question'))
        if (res):
            self.editor.save_tabs()
            self.logger.info(self.trn.msg('htk_core_stopped'))
            self.logger.logfile.close()
            self.cfg.save()
            self.destroy()

class ExceptionHandler:
    """Class ExceptionHandler
    """

    _logger = None

    def __init__(self, func, subst, widget):
        """Class constructor

        Called when object is initialized

        Args:
           func (obj): function
           subst (obj): substrate
           widget (obj): widget

        """

        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        """Method catches unhandled exception

        Args:
            args (list): arguments

        Returns:
            obj

        """

        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            raise SystemExit, msg
        except Exception as e:
            if (self._logger is None):
                self._logger = Logger.get_instance()
            self._logger.error(traceback.format_exc())
