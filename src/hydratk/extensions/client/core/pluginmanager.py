# -*- coding: utf-8 -*-
"""Plugin manager

.. module:: client.core.pluginmanager
   :platform: Windows, Unix
   :synopsis: Plugin manager
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.extensions.client.core.tkimport import tk

class PluginManager(object):
    """Class PluginManager
    """

    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None
    _config = None

    # gui elements
    _win = None
    _states = {}
    _btn = None

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
        """Method gets PluginManager singleton instance

        Args:
            none

        Returns:
            obj

        """

        if (PluginManager._instance is None):
            PluginManager._instance_created = True
            PluginManager._instance = PluginManager()

        return PluginManager._instance

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

    @property
    def config(self):
        """ config property getter """

        if (self._config is None):
            self._config = self.root.cfg

        return self._config

    def show_manager(self):
        """Method shows manager window

        Args:
            none

        Returns:
            void

        """
           
        self._win = tk.Toplevel(self.root)
        self._win.title(self.trn.msg('htk_gui_plugin_manager_title'))
        self._win.transient(self.root)
        self._win.resizable(False, False)
        self._win.geometry('+%d+%d' % (self.root.winfo_screenwidth() / 3, self.root.winfo_screenheight() / 3))
        self._win.tk.call('wm', 'iconphoto', self._win._w, self.root.images['logo'])
        self._win.focus_set()

        font = ('Arial', 10, 'bold')
        tk.Label(self._win, text=self.trn.msg('htk_gui_plugin_manager_name'), font=font, width=25, anchor='w', padx=3, pady=3).grid(row=0, column=0)
        tk.Label(self._win, text=self.trn.msg('htk_gui_plugin_manager_enabled'), font=font, anchor='w', padx=3, pady=3).grid(row=0, column=1)
        i = 1

        for name, cfg in self.config.data['Plugins'].items():
            tk.Label(self._win, text=name, width=25, anchor='w', padx=3).grid(row=i, column=0)
            state = True if ('enabled' in cfg and cfg['enabled'] == 1) else False
            var = tk.IntVar(value=state)
            tk.Checkbutton(self._win, variable=var).grid(row=i, column=1, padx=3, sticky='w')
            self._states[name] = var
            i += 1

        self._btn = tk.Button(self._win, text=self.trn.msg('htk_gui_plugin_manager_save'), command=self._update_state)
        self._btn.grid(row=i, column=2, padx=3, pady=3, sticky='e')

        self._win.bind('<Escape>', lambda f: self._win.destroy())

    def _update_state(self):
        """Method update plugin state configuration

        Args:none

        Returns:
            void

        """

        plugins = self.config.data['Plugins']
        update = False
        for name, cfg in plugins.items():
            req_state = self._states[name].get()
            if ('enabled' not in cfg or cfg['enabled'] != req_state):
                cfg['enabled'] = req_state
                update = True

        if (update):
            self.config.save()

        if (self._win is not None):
            self._win.destroy()
