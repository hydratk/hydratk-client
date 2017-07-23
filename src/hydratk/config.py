# -*- coding: utf-8 -*-
"""Configuration

.. module:: config
   :platform: Windows
   :synopsis: Configuration
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from yaml import safe_load, safe_dump
from os import path

class Config(object):
    """Class Config
    """

    _instance = None
    _instance_created = False

    _path = path.join(path.dirname(__file__), '../../etc/hydratk/hydratk-client.conf')
    _data = None

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

        self.load()

    @staticmethod
    def get_instance():
        """Method gets Config singleton instance

        Args:
            none

        Returns:
            obj

        """

        if (Config._instance is None):
            Config._instance_created = True
            Config._instance = Config()

        return Config._instance

    @property
    def data(self):
        """ data property getter """

        return self._data

    @property
    def cfg_path(self):
        """ path property getter """

        return self._path

    def load(self):
        """Method loads configuration from file

        Args:
            none

        Returns:
            void

        """

        with open(self._path, 'r') as f:
            self._data = safe_load(f.read())
            if (self._data == None):
                self._data = {}

    def save(self):
        """Method saves configuration to file

        Args:
            none

        Returns:
            void

        """

        with open(self._path, 'w') as f:
            safe_dump(self._data, f, default_flow_style=False)
