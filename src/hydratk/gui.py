# -*- coding: utf-8 -*-
"""GUI model

.. module:: gui
   :platform: Windows
   :synopsis: GUI model
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

    _instance = None
    _instance_created = False

    _config = None
    _trn = None

    _frame_main = None
    _pane_main = None
    _pane_left = None
    _pane_right = None

    _menu = None
    _menu_file = None
    _menu_file_new = None
    _menu_edit = None
    _menu_help = None

    _frame_explorer = None
    _explorer_tree = None
    _explorer_vsb = None
    _explorer_hsb = None
    _explorer = None

    _frame_yoda_tree = None

    _frame_editor = None

    _frame_logger = None

    def __init__(self):

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        tk.CallWrapper = ExceptionHandler
        self._config = Config.get_instance()
        self._trn = Translator.get_instance(self._config._data['Core']['language'])
        self._instance = tk.Tk.__init__(self)

    @staticmethod
    def get_instance():

        if (Gui._instance is None):
            Gui._instance_created = True
            Gui._instance = Gui()

        return Gui._instance

    def set_gui(self):

        self.set_window()
        self.set_pane_left()
        self.set_pane_right()
        self.set_menu()
        self.set_frame_ref()

        self._frame_logger.info(self._trn.msg('htk_core_started'))

    def set_window(self):

        self.title('HydraTK')
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=path.join(path.join(path.dirname(__file__), 'img'), 'logo.gif')))
        self.wm_state('zoomed')
        self.protocol('WM_DELETE_WINDOW', self.exit)
        self.clipboard_get()

        self._frame_main = tk.Frame(self)
        self._frame_main.pack(expand=True, fill=tk.BOTH)
        self._pane_main = tk.PanedWindow(self._frame_main, orient=tk.HORIZONTAL, sashwidth=10)
        self._pane_main.pack(expand=True, fill=tk.BOTH, padx=10, pady=(6, 10))

    def set_menu(self):
        
        self._menu = tk.Menu(self._frame_main)
        self.config(menu=self._menu)

        self.set_menu_file()
        self.set_menu_edit()
        self.set_menu_help()

    def set_menu_file(self):

        self._menu_file = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self._trn.msg('htk_gui_menu_file'), menu=self._menu_file)
        self._menu_file_new = tk.Menu(self._menu_file, tearoff=False)
        self._menu_file.add_cascade(label=self._trn.msg('htk_gui_menu_file_new'), menu=self._menu_file_new)
        self._menu_file_new.add_command(label=self._trn.msg('htk_gui_menu_file_new_file'), command=self._frame_editor.new_file)
        self._menu_file_new.add_command(label=self._trn.msg('htk_gui_menu_file_new_directory'), command=self._frame_explorer.new_directory)
        self._menu_file_new.add_command(label=self._trn.msg('htk_gui_menu_file_new_project'), command=self._frame_explorer.new_project)

        self._menu_file.add_command(label=self._trn.msg('htk_gui_menu_file_open'), accelerator='Ctrl+O', command=self._frame_editor.open_file)
        self.bind('<Control-o>', self._frame_editor.open_file)
        self._menu_file.add_command(label=self._trn.msg('htk_gui_menu_file_save_as'), command=self._frame_editor.save_as_file, state=tk.DISABLED)
        self._menu_file.add_command(label=self._trn.msg('htk_gui_menu_file_save'), accelerator='Ctrl+S', command=self._frame_editor.save_file, state=tk.DISABLED)
        self.bind('<Control-s>', self._frame_editor.save_file)
        self._menu_file.add_separator()
        self._menu_file.add_command(label=self._trn.msg('htk_gui_menu_file_exit'), accelerator='Ctrl+Q', command=self.exit)
        self.bind('<Control-q>', self.exit)

    def set_menu_edit(self):
        
        self._menu_edit = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self._trn.msg('htk_gui_menu_edit'), menu=self._menu_edit)

    def set_menu_help(self):

        self._menu_help = tk.Menu(self._menu, tearoff=False)
        self._menu.add_cascade(label=self._trn.msg('htk_gui_menu_help'), menu=self._menu_help)

    def set_pane_left(self):

        self._pane_left = tk.PanedWindow(self._pane_main, orient=tk.VERTICAL, sashwidth=10, sashrelief=tk.RAISED)
        self._pane_main.add(self._pane_left)
        self.set_explorer()
        self.set_yoda_tree()

    def set_pane_right(self):

        self._pane_right = tk.PanedWindow(self._pane_main, orient=tk.VERTICAL, sashwidth=10, sashrelief=tk.RAISED)
        self._pane_main.add(self._pane_right)
        self.set_editor()
        self.set_logger()

    def set_explorer(self):

        self._frame_explorer = Explorer.get_instance(self)
        self._pane_left.add(self._frame_explorer)

    def set_yoda_tree(self):

        self._frame_yoda_tree = tk.LabelFrame(self._pane_left, text='Yoda tree')
        self._pane_left.add(self._frame_yoda_tree)

    def set_editor(self):

        self._frame_editor = Editor.get_instance(self)
        self._pane_right.add(self._frame_editor)

    def set_logger(self):

        self._frame_logger = Logger.get_instance(self)
        self._pane_right.add(self._frame_logger)
        
    def set_frame_ref(self):
        
        self._frame_explorer.set_ref()
        self._frame_editor.set_ref()

    def exit(self, event=None):

        res = tkMessageBox.askyesno(self._trn.msg('htk_gui_exit_title'), self._trn.msg('htk_gui_exit_question'))
        if (res):
            self._frame_logger.info(self._trn.msg('htk_core_stopped'))
            self._frame_logger._file.close()
            self.destroy()

class ExceptionHandler:

    _log = None

    def __init__(self, func, subst, widget):

        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):

        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            raise SystemExit, msg
        except Exception as e:
            if (self._log is None):
                self._log = Logger.get_instance()
            self._log.error(traceback.format_exc())
