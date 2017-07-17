# -*- coding: utf-8 -*-
"""Main HydraTK client module

.. module:: client
   :platform: Windows
   :synopsis: Main HydraTK client module
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.gui import Gui

def main():

    htk = Gui.get_instance()
    htk.set_gui()
    htk.mainloop()

if __name__ == '__main__':
    main()
