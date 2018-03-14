.. _module_ext_client_core_msgqueue:

httpclient
==========

This sections contains module documentation of msgqueue module.

MsgQueue
^^^^^^^^

Class for message queue to support background tasks processes in separate threads.
Task operate with GUI in asynchronous way not blocking main thread.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _queue - quere reference
* _thread_cnt - thread count
* _threads - thread rereferences
* _time_check - time interval between queue check
* _msg_id - message id

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* logger - returns _logger

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references and queue.

* get_instance

Returns instance reference, singleton pattern.

* _create_threads

Method creates queue and worker threads.

* write_msg

Method writes message to queue.

* _prepare_msg

Method prepares message in required format.

* _worker

Worker processing method. Method reads message from queue if any and processes it.
Worker runs in infinite loop, thread sleeps after processing.