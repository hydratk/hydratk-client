.. _module_ext_client_core_notebook:

notebook
========

This sections contains module documentation of notebook module.

CustomNotebook
^^^^^^^^^^^^^^

Class for code customized Notebook frame.

**Attributes** :

* _editor - Editor instance reference
* _tab_refs - references to FileTab instances
* _new_cnt - count of new files
* _drag_tab - dragged tab index

**Properties (Getters)** :

* editor - returns _editor
* tab_refs - returns _tab_refs
* new_cnt - returns _new_cnt

**Methods** :

* __init__

Constructor. Initialize GUI and custom style.

* _set_custom_style

Method sets own style for Notebook frame. Tab with close button.

* _set_gui

Method initializes GUI.

* is_tab_present

Method checks if tab for given file is present.

* is_filetab

Method checks if tab is FileTab instance.

* add_tab

Method by default adds new FileTab to list and selects it. Some controls are not available if no tab is present.
Other supported tab types: ImageTab.

* _get_current_index

Method returns index of selected tab.

* get_current_tab

Method returns selected tab.

* get_current_content

Method returns content of selected tab.

* get_content

Method returns content of requested tab.

* get_marked_content

Method returns selected text.

* set_current_tab

Method sets parameters of selected tab.

* _set_tab_related_controls

Method enables controls which become available when first tab is added.
The controls are disabled when last tab is closed.

* close_tab

Method closes tab. It asks for saving when tab text has unsaved changes. 
Jedi files are removed from storage and tree is cleared.

* _on_drag

Method handles mouse drag event. Dragged tab index is stored.

* _on_drop

Method handles mouse drop event. Tab is closed or tabs are swapped. 