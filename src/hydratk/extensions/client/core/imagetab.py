# -*- coding: utf-8 -*-
"""ImageTab

.. module:: client.core.imagetab
   :platform: Windows, Unix
   :synopsis: CanvasTab
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.extensions.client.core.tkimport import tk, ttk, c_os

class ImageTab(tk.Frame):
    """Class CanvasTab
    """

    # references
    _nb = None
    _editor = None

    # tab parameters
    _name = None
    _path = None

    # gui elements
    _canvas = None
    _image = None
    _vbar = None
    _hbar = None

    def __init__(self, nb, name, path):
        """Class constructor

        Called when object is initialized

        Args:
           nb (obj): notebook reference
           name (str): file name
           path (str): file path

        """

        self._nb = nb
        self._editor = self.nb.editor

        tk.Frame.__init__(self)
        self._name = name
        self._path = path

        self._set_gui()

    @property
    def nb(self):
        """ nb property getter """

        return self._nb

    @property
    def editor(self):
        """ editor property getter """

        return self._editor

    @property
    def name(self):
        """ name property getter """

        return self._name

    @property
    def path(self):
        """ path property getter """

        return self._path

    def _set_gui(self):
        """Method sets graphical interface

        Args:
            none

        Returns:
            void

        """

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._vbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)

        # canvas
        self._canvas = tk.Canvas(self, scrollregion=(0, 0, 2000, 1000))
        self._canvas.grid(in_=self, row=0, column=0, sticky=tk.NSEW)
        self._image = tk.PhotoImage(file=self._path)
        self._canvas.create_image(600, 300, image=self._image)
        self._canvas.focus_set()

        # scrollbars
        self._vbar.configure(command=self._canvas.yview)
        self._vbar.grid(in_=self, row=0, column=1, sticky=tk.NS)
        self._hbar.configure(command=self._canvas.xview)
        self._hbar.grid(in_=self, row=1, column=0, sticky=tk.EW)
        self._canvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)

        # events
        self._vbar.configure(command=self._on_vsb)
        if (c_os == 'Windows'):
            self._canvas.bind('<MouseWheel>', self._on_mouse_wheel)
        else:
            self._canvas.bind('<Button-4>', self._on_mouse_wheel)
            self._canvas.bind('<Button-5>', self._on_mouse_wheel)

    def _on_vsb(self, *args):
        """Method handles scrollbar event

        Args:
            args (list): arguments

        Returns:
            void

        """

        self._canvas.yview(*args)

    def _on_mouse_wheel(self, event=None):
        """Method handles mouse wheel event

        Args:
            event (obj): event

        Returns:
            void

        """

        if (c_os == 'Windows'):
            self._canvas.yview_scroll(-1 * (event.delta / 120), 'units')
        else:
            unit = 0
            if (event.num == 4):
                unit = -1
            elif (event.num == 5):
                unit = 1
            self._canvas.yview_scroll(unit, 'units')

        return 'break'
