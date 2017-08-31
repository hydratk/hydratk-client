.. _module_ext_client_syntaxchecker:

syntaxchecker
=============

This sections contains module documentation of syntaxchecker module.

SyntaxChecker
^^^^^^^^^^^^^

Class for code syntax check.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _tb_idx - traceback index

**Properties (Getters)** :

* root - returns _root

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references.

* get_instance

Returns instance reference, singleton pattern.

* check

Method checks text syntax according to file extensions.

* _check_python

Method checks syntax of Python file using compile. Error is read from traceback.

* _check_jedi

Method checks syntax of jedi file, YAML format, Yoda format, Python syntax.

* _reformat_test

Method modified test content, lowercase keys for better parsing.

* _check_scenario

Method checks syntax of test scenario, mandatory tags, test case ordering, python blocks syntax.

* _check_case

Method checks syntax of test case, mandatory tags, test condition ordering, python blocks syntax.

* _check_condition

Method checks syntax of test condition, mandatory tags, python blocks syntax.

* _check_python_block

Method checks syntax of Python block using compile. Error is read from traceback.