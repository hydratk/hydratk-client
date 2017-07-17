# -*- coding: utf-8 -*-
"""Configuration

.. module:: config
   :platform: Windows
   :synopsis: Configuration
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from yaml import safe_load, safe_dump

class Config(object):

    _instance = None
    _instance_created = False

    _path = 'C:/private/codes/Git/Hydra/hydratk-client/etc/hydratk/hydratk-client.conf'
    _data = None

    def __init__(self):

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self.load()

    @property
    def data(self):

        return self._data

    @staticmethod
    def get_instance():

        if (Config._instance is None):
            Config._instance_created = True
            Config._instance = Config()

        return Config._instance

    def load(self):

        with open(self._path, 'r') as f:
            self._data = safe_load(f.read())
            if (self._data == None):
                self._data = {}

    def save(self):

        with open(self._path, 'w') as f:
            safe_dump(self._data, f, default_flow_style=False)
