# -*- coding: utf-8 -*-
"""Support for multiple languages

.. module:: translator
   :platform: Windows
   :synopsis: Support for multiple languages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from importlib import import_module

class Translator(object):

    _instance_created = False
    _instance = None

    _language = ''
    _msg_mod = None
    _messages = {}

    def __init__(self, language):
        """Class constructor

        Called when object is initialized

        Args:
           language (str): language

        Raises:
           error: ValueError

        """

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        if (language not in ['en', 'cs']):
            raise ValueError('Not supported language %s' % language)

        self.set_language(language)
        msg_package = 'hydratk.translation.' + self._language + '.messages'
        self._msg_mod = import_module(msg_package)
        self.register_messages(self._msg_mod.msg)

    @staticmethod
    def get_instance(language=None):

        if (Translator._instance is None):
            Translator._instance_created = True
            Translator._instance = Translator(language)

        return Translator._instance

    @property
    def msg_mod(self):
        """ msg_mod property getter, setter """

        return self._msg_mod

    @msg_mod.setter
    def msg_mod(self, msg_module):
        """ msg_mod property setter """

        self._msg_mod = msg_module

    def register_messages(self, messages):
        """Methods registers langtexts

        Args:
           messages (dict): langtexts

        Returns:
           bool: True

        Raises:
           error: ValueError

        """

        if messages != '':
            if type(messages) is dict:
                self._messages = messages
            else:
                raise ValueError('Invalid messages type, dictionary expected')
        else:
            raise ValueError(
                'Cannot assign an empty messages, dictionary expected')
        return True

    def set_language(self, lang):
        """Methods sets language

        Args:
           lang (str): language

        Returns:
           void

        """

        self._language = lang

    def get_language(self):
        """Methods gets language

        Args:
           none

        Returns:
           str: language

        """

        return self._language

    def msg(self, key, *args):
        """Methods resolves langtext according to debug level

        Args:
           key (str): langtext
           args (ags): langtext arguments

        Returns:
           str: resolved langtext

        """

        return self._messages[key].format(*args) if (key in self._messages) else key
