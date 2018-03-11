.. _module_ext_client_plugins_gitclient:

gitclient
=========

This sections contains module documentation of gitclient module.

Plugin
^^^^^^

Class for GitClient.

**Attributes** :

* _w_mng - repository manager window
* _w_mng_pane - window pane
* _w_mng_frame_left - left frame
* _w_mng_frame_right - right frame
* _w_mng_tree - repositories tree
* _w_mng_menu - context menu
* _w_mng_vbar - repositories scrollbar
* _w_mng_url - url entry
* _w_mng_user - user entry
* _w_mng_passw - password entry
* _w_mng_name - name entry
* _w_mng_email - email entry
* _w_mng_btn_save - button save
* _w_mng_msg - message entry
* _w_mng_author - author entry
* _w_mng_push - push checkbox
* _w_mng_select_all - select all checkbox
* _w_mng_files - changed files tree
* _w_mng_files_bar - files scrollbar
* _w_mng_btn_commit - button commit

**Methods** :

* _init_plugin

Method initializes plugin.

* setup

Method sets plugin menu.

* _win_clone

Method displays form for repository cloning.

* _win_repomanager

Method displays form for repository manager.

* _set_tree

Method sets repository tree in manager.

* _context_menu

Method displays context menu in repository tree.

* _set_config

Method sets configuration section in manager.

* _set_commit

Method sets commit section in manager.

* _set_dirpath

Method sets directory path in from file dialog.

* _clone_repo

Method clones repository from remote via HTTP.

* _create_project

Method creates new project from cloned repository.

* _fill_repo_detail

Method fills details (configuration, commit) for requested repository. 

* _save_config

Method saves repository configuration and updates also git config.

* _commit

Method adds changed files to stage and creates commit (with possible push).

* _push

Method pushes repository to remote. Currently only master branch is supported.

* _pull

Method pulls repository from remote. Currently only master branch is supported.

* _fill_changed_files

Method fills changed files tree.

* _get_changed_files

Method gets repository changed files from git status (added, modified, deleted).

* _select_file

Method selects or deselects item in changed files tree.

* _select_all_files

Method selects or deselects all items in changed files tree.

* _prepare_url

Method prepares url with authentication.