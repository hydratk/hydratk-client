.. _module_ext_client_core_imagetab:

imagetab
========

This sections contains module documentation of imagetab module.

ImageTab
^^^^^^^^

Class for ImageTab frame.

**Attributes** :

* _nb - Notebook instance reference
* _editor - Editor instance reference
* _name - tab name
* _path - tab filepath
* _canvas - Canvas
* _image - PhotoImage
* _vbar - VerticalBar
* _hbar - HorizontalBar

**Properties (Getters)** :

* nb - returns _nb
* editor - returns _editor
* name - returns _name
* path - returns _path

**Methods** :

* __init__

Constructor. Initialize references and GUI.

* _set_gui

Method initializes GUI - canvas with loaded image and scrollbars.

* _on_vsb

Method handles vertical scrolling, synchronize canvas.

* _on_mouse_wheel

Method handles mouse wheel event, synchronize canvas.
Event names are different for Windows (1 event, direction in event detail) and Linux (2 events for 2 directions).