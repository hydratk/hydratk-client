# -*- coding: utf-8 -*-
"""Test mode handler

.. module:: client.core.testhandler
   :platform: Unix
   :synopsis: Test mode handler
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import os
from sys import version_info
from json import dumps, loads

class TestHandler(object):
    
    _instance = None
    _instance_created = False

    _root = None
    _pipe_in_path = '/tmp/htkclient_test_in'
    _pipe_in = None
    _pipe_out_path = '/tmp/htkclient_test_out'
    _pipe_out = None

    _time_check = 10
    _eot = '\x17' if (version_info[0] == 2) else b'\x17'
    
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
        self._create_pipes()
        self._read_msg()

    @property
    def root(self):
        """ root property getter """

        return self._root

    @staticmethod
    def get_instance(root=None):
        """Method gets Colorizer singleton instance

        Args:
            root (obj): root frame

        Returns:
            obj

        """

        if (TestHandler._instance is None):
            TestHandler._instance_created = True
            TestHandler._instance = TestHandler(root)

        return TestHandler._instance

    def _create_pipes(self):
        """Method creates pipes for bi-directional communication with external process

        Args:
            root (obj): root frame

        Returns:
            void

        """
        
        if (os.path.exists(self._pipe_in_path)):
            os.remove(self._pipe_in_path)
        os.mkfifo(self._pipe_in_path)
        
        if (os.path.exists(self._pipe_out_path)):
            os.remove(self._pipe_out_path)
        os.mkfifo(self._pipe_out_path)

        # connect to input pipe
        self._pipe_in = os.open(self._pipe_in_path, os.O_RDONLY | os.O_NONBLOCK)
        self.root.logger.info(self.root.trn.msg('htk_core_test_mode'))

    def clean(self):
        """Method cleans pipes

        Args:
            none

        Returns:
            void

        """
        
        if (os.path.exists(self._pipe_in_path)):
            os.remove(self._pipe_in_path)
        if (os.path.exists(self._pipe_out_path)):
            os.remove(self._pipe_out_path)

    def _read_msg(self):
        """Method reads message from pipe

        Args:
            none

        Returns:
            void

        """

        try:
            msg, found = '' if (version_info[0] == 2) else b'', False
            # read characters until EOT
            while (not found):
                c = os.read(self._pipe_in, 1)
                if (not c or c == self._eot):
                    found = True
                else:
                    msg += c
            if (len(msg) > 0):
                msg = loads(msg)
                self._process_msg(msg)
        except (OSError):
            pass
        finally:
            self.root.after(self._time_check, self._read_msg)
            
    def _write_msg(self, msg):
        """Method writes message to pipe

        Args:
            msg (dict): message

        Returns:
            void

        """        

        try:
            # connect to output pipe, external process must connect first (can't be done in _create_pipes)
            if (self._pipe_out is None):
                self._pipe_out = open(self._pipe_out_path, 'wb', 0)

            msg_out = dumps(msg)

        except Exception as ex:
            msg_out = {'id': msg['id'], 'type': 'response', 'result': False, 'error': repr(ex)}
            msg_out = dumps(msg_out)

        finally:
            if (version_info[0] == 3):
                msg_out = msg_out.encode('utf8')
            self._pipe_out.write(msg_out + self._eot)

    def _process_msg(self, msg_in):
        """Method processes message

        Args:
            msg_in (dict): input message

        Returns:
            void

        """

        msg_out = {
                   'id': msg_in['id'],
                   'type': 'response',
                   'result': False
                  }

        try:
            loc = locals()
            loc.update(msg_in['input'])
            globals().update({'self': self})
            exec(msg_in['code'], globals(), loc)

            out = {}
            for var in msg_in['output']:
                out[var] = loc[var]

            msg_out['result'] = True
            msg_out['output'] = out
        except Exception as ex:
            msg_out['error'] = repr(ex)
        finally:
            self._write_msg(msg_out)
