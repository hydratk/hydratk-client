.. _module_ext_client_core_testhandler:

testhandler
===========

This sections contains module documentation of testhandler module.

TestHandler
^^^^^^^^^^^

Class for test mode handler.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _pipe_in_path - input pipe path /tmp/htkclient_test_in
* _pipe_in - input pipe reference
* _pipe_out_path - output pipe path /tmp/htkclient_test_out
* _pipe_out - output pipe reference
* _time_check - time interval to check input pipe
* _eot - end of transmission character

**Properties (Getters)** :

* root - returns _root

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references.

* get_instance

Returns instance reference, singleton pattern.

* _create_pipes

Method creates input and output pipes to communicate with external testing process (yoda extension, currently used for unit tests).

* clean

Method deletes pipes.

* _read_msg

Method reads request message from input pipe. The message have defined json format followed by EOT character.
Method reads one message and returns control to main process. Method is called after set time_check interval.

* _write_msg

Method writes response message to output pipe.

* _process_msg

Methods processes request message and prepares response message. The message contains python code, input arguments and requested output arguments. 
The code is executed and outputs are sent in response. Helper methods definitions (not in client pythonpath) are included in the code.  