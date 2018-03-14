# -*- coding: utf-8 -*-
"""Message queue for background processing

.. module:: client.core.msgqueue
   :platform: Unix
   :synopsis: Message queue for background processing
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from threading import Thread
from time import sleep
from random import randint

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

class MsgQueue(object):

    _instance = None
    _instance_created = False

    # references
    _root = None
    _trn = None
    _logger = None

    _queue = None
    _thread_cnt = 1
    _threads = []
    _time_check = 0.01
    _msg_id = 0

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
        self._trn = root.trn
        self._logger = root.logger

        self._create_threads()

    @property
    def root(self):
        """ root property getter """

        return self._root

    @property
    def trn(self):
        """ trn property getter """

        return self._trn

    @property
    def logger(self):
        """ logger property getter """

        return self._logger

    @staticmethod
    def get_instance(root=None):
        """Method gets MsgQueue singleton instance

        Args:
            root (obj): root frame

        Returns:
            obj

        """

        if (MsgQueue._instance is None):
            MsgQueue._instance_created = True
            MsgQueue._instance = MsgQueue(root)

        return MsgQueue._instance

    def _create_threads(self):
        """Method creates queue and worker threads

        Args:
            none

        Returns:
            void

        """

        self._queue = Queue()
        self._msg_id = randint(10 ** 9, 10 ** 10 - 1)
        
        for i in range(self._thread_cnt):
            thread = Thread(target=self._worker, args=(i + 1,))
            thread.daemon = True
            thread.start()
            self._threads.append(thread)

    def write_msg(self, function, args):
        """Method writes message to queue

        Args:
            function (callable): function
            args (list): function arguments

        Returns:
            void

        """

        msg = self._prepare_msg(function, args)
        self._queue.put_nowait(msg)
        
    def _prepare_msg(self, function, args):
        """Method prepares message in required format

        Args:
            function (callable): function
            args (list): function arguments

        Returns:
            dict

        """

        msg = {
               'id'       : self._msg_id,
               'function' : function,
               'args'     : args
              }
        self._msg_id += 1

        return msg

    def _worker(self, id):
        """Worker thread processing method

        Method reads message from queue if any and processes it.
        Inifinite loop, thread sleeps after processing

        Args:
            id (int): thread id

        Returns:
            void

        """
        
        while (True):
            if (not self._queue.empty()):

                try:
                    msg = self._queue.get_nowait()
                    self.logger.debug(self.trn.msg('htk_core_msg_received', id, msg))
                    msg['function'](*msg['args'])
                    self._queue.task_done()
                    self.logger.debug(self.trn.msg('htk_core_msg_processed', id, msg['id']))
                except Exception as ex:
                    self.logger.error(ex)

            sleep(self._time_check)
