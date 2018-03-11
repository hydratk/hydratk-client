import os
from random import randint
from inspect import getsource
from time import sleep
from sys import version_info
from json import dumps, loads

from hydratk.core.masterhead import MasterHead

class GuiClient(object):
    
    _instance = None
    _instance_created = False

    _mh = None
    _pipe_in_path = '/tmp/htkclient_test_in'
    _pipe_in = None
    _pipe_out_path = '/tmp/htkclient_test_out'
    _pipe_out = None

    _msg_id = 0
    _eot = '\x17' if (version_info[0] == 2) else b'\x17'
    
    def __init__(self):

        if (self._instance_created == False):
            raise ValueError('For creating class instance please use the get_instance method instead!')
        if (self._instance is not None):
            raise ValueError('A Class instance already exists, use get_instance method instead!')

        self._mh = MasterHead.get_head()
        self._pipe_out = os.open('/tmp/htkclient_test_out', os.O_RDONLY | os.O_NONBLOCK)
        self._pipe_in = open('/tmp/htkclient_test_in', 'wb', 0)
        self._msg_id = randint(10 ** 9, 10 ** 10 - 1)

    @staticmethod
    def get_instance():

        if (GuiClient._instance is None):
            GuiClient._instance_created = True
            GuiClient._instance = GuiClient()

        return GuiClient._instance

    def prepare_msg(self, code, functions=[], input={}, output=[]):

        for f in functions:
            code = getsource(f) + '\n' + code

        msg = {
               'id'     : self._msg_id,
               'type'   : 'request',
               'code'   : code,
               'input'  : input,
               'output' : output
              }

        self._msg_id += 1
        return msg

    def write_msg(self, code, functions=[], input={}, output=[]):

        msg = self.prepare_msg(code, functions, input, output)
        self._mh.dmsg(msg)
        msg = dumps(msg)
        if (version_info[0] == 3):
            msg = msg.encode('utf8')
        self._pipe_in.write(msg + self._eot)

    def read_msg(self, *args, **kwargs):
        
        msg, found = '' if (version_info[0] == 2) else b'', False
        # read characters until EOT
        while (not found):
            try:
                c = os.read(self._pipe_out, 1)
                if (c == self._eot):
                    found = True
                elif (c):
                    msg += c
            except (OSError):
                sleep(0.1)
            
        msg = loads(msg)
        self._mh.dmsg(msg)

        output = []
        if ('error' not in kwargs or not kwargs['error']):
            assert (msg['result']), msg['error']
        elif (kwargs['error']):
            assert (not msg['result']), 'Error expected'
            output.append(msg['error'])

        for var in args:
            if (var in msg['output']):
                output.append(msg['output'][var])
            else:
                output.append(None)
            
        output = tuple(output) if (len(output) != 1) else output[0]

        return output
