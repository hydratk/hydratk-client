# -*- coding: utf-8 -*-
"""Git client plugin

.. module:: client.plugins.gitclient
   :platform: Windows, Unix
   :synopsis: Git client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.extensions.client.core import plugin
from hydratk.extensions.client.core.tkimport import tk, ttk, tkfd
from hydratk.extensions.client.core.utils import fix_path

try:
    from git import Repo
except ImportError:
    pass
    
from shutil import rmtree
import os

class Plugin(plugin.Plugin):
    """Class Plugin
    """

    # gui elements
    # window clone
    _w_clone = None
    _w_clone_url = None
    _w_clone_user = None
    _w_clone_passw = None
    _w_clone_dirpath = None
    _w_clone_error = None
    _w_clone_btn = None

    # window repomanager
    _w_mng = None
    _w_mng_pane = None
    _w_mng_frame_left = None
    _w_mng_frame_right = None

    _w_mng_tree = None
    _w_mng_menu = None
    _w_mng_vbar = None

    # configuration section
    _w_mng_url = None
    _w_mng_user = None
    _w_mng_passw = None
    _w_mng_name = None
    _w_mng_email = None
    _w_mng_btn_save = None

    # commit section
    _w_mng_msg = None
    _w_mng_author = None
    _w_mng_push = None
    _w_mng_select_all = None
    _w_mng_files = None
    _w_mng_files_bar = None
    _w_mng_btn_commit = None

    def _init_plugin(self):
        """Method initializes plugin

        Args:
           none

        Returns:
           void

        """

        self._plugin_id = 'gitclient'
        self._plugin_name = 'GitClient'
        self._plugin_version = '0.1.0'
        self._plugin_author = 'Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>'
        self._plugin_year = '2017 - 2018'

    def _setup(self):
        """Method executes plugin setup

        Args:
           none

        Returns:
           void

        """

        try:
            import git
            self._set_menu('gitclient', 'htk_gitclient_menu', 'plugin')
            self._set_menu_item('gitclient', 'htk_gitclient_menu_clone', self._win_clone)
            self._set_menu_item('gitclient', 'htk_gitclient_menu_repomanager', self._win_repomanager)

        except ImportError:
            self.logger.error(self.trn.msg('htk_gitclient_not_installed'))

    def _win_clone(self):
        """Method displays clone window

        Args:
           none

        Returns:
           void

        """

        self._w_clone = tk.Toplevel(self.root)
        self._w_clone.title(self.trn.msg('htk_gitclient_clone_title'))
        self._w_clone.transient(self.root)
        self._w_clone.resizable(False, False)
        self._w_clone.geometry('+%d+%d' % (self.root.winfo_screenwidth() / 3, self.root.winfo_screenheight() / 3))
        self._w_clone.tk.call('wm', 'iconphoto', self._w_clone._w, self.root.images['logo'])

        tk.Label(self._w_clone, text=self.trn.msg('htk_gitclient_clone_url')).grid(row=0, column=0, sticky='e')
        self._w_clone_url = tk.Entry(self._w_clone, width=70)
        self._w_clone_url.grid(row=0, column=1, padx=3, pady=10, sticky='e')
        self._w_clone_url.focus_set()

        tk.Label(self._w_clone, text=self.trn.msg('htk_gitclient_clone_user')).grid(row=1, column=0, sticky='e')
        self._w_clone_user = tk.Entry(self._w_clone, width=20)
        self._w_clone_user.grid(row=1, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_clone, text=self.trn.msg('htk_gitclient_clone_password')).grid(row=2, column=0, sticky='e')
        self._w_clone_passw = tk.Entry(self._w_clone, width=20)
        self._w_clone_passw.grid(row=2, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_clone, text=self.trn.msg('htk_gitclient_clone_dirpath')).grid(row=3, column=0, sticky='e')
        self._w_clone_dirpath = tk.Entry(self._w_clone, width=70)
        self._w_clone_dirpath.grid(row=3, column=1, padx=3, pady=3, sticky='w')
        tk.Button(self._w_clone, text='...', command=lambda: self._set_dirpath(self._w_clone_dirpath)).grid(row=3, column=2, sticky='w')

        error = tk.Label(self._w_clone, text='', foreground='#FF0000')
        error.grid(row=4, column=1, sticky='w')
        self._w_clone_btn = tk.Button(self._w_clone, text=self.trn.msg('htk_gitclient_clone_button'),
                        command=lambda: self._clone_repo(self._w_clone_url.get(), self._w_clone_dirpath.get(), self._w_clone_user.get(),
                                                         self._w_clone_passw.get(), error))
        self._w_clone_btn.grid(row=4, column=2, padx=3, pady=3, sticky='e')

        self._w_clone.bind('<Escape>', lambda f: self._w_clone.destroy())

    def _win_repomanager(self):
        """Method displays repository manager window

        Args:
           none

        Returns:
           void

        """

        self._w_mng = tk.Toplevel(self.root)
        self._w_mng.title(self.trn.msg('htk_gitclient_repomanager_title'))
        self._w_mng.transient(self.root)
        self._w_mng.resizable(False, False)
        self._w_mng.geometry('+%d+%d' % (self.root.winfo_screenwidth() / 5, self.root.winfo_screenheight() / 10))
        self._w_mng.tk.call('wm', 'iconphoto', self._w_mng._w, self.root.images['logo'])

        self._w_mng_pane = tk.PanedWindow(self._w_mng, orient=tk.HORIZONTAL)
        self._w_mng_pane.pack(expand=True, fill=tk.BOTH)

        # left frame
        self._w_mng_frame_left = tk.Frame(self._w_mng_pane)
        self._set_tree()
        self._w_mng_pane.add(self._w_mng_frame_left)

        # right frame
        self._w_mng_frame_right = tk.Frame(self._w_mng_pane)
        self._set_config()
        self._set_commit()
        self._w_mng_pane.add(self._w_mng_frame_right)

        self._w_mng.bind('<Escape>', lambda f: self._w_mng.destroy())

    def _set_tree(self):
        """Method sets tree gui

        Args:
           none

        Returns:
           void

        """

        self._w_mng_vbar = ttk.Scrollbar(self._w_mng_frame_left, orient=tk.VERTICAL)
        self._w_mng_tree = ttk.Treeview(self._w_mng_frame_left, columns=(), show='tree', displaycolumns=(), height=10, selectmode='browse',
                                        yscrollcommand=self._w_mng_vbar.set)
        self._w_mng_vbar.config(command=self._w_mng_tree.yview)
        self._w_mng_vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._w_mng_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for name, cfg in self.explorer._projects.items():
            if ('git' in cfg):
                self._w_mng_tree.insert('', 'end', text=name)

        # context menu
        self._w_mng_menu = tk.Menu(self._w_mng_tree, tearoff=False)
        self._w_mng_menu.add_command(label=self.trn.msg('htk_gitclient_repomanager_push'), command=self._push)
        self._w_mng_menu.add_command(label=self.trn.msg('htk_gitclient_repomanager_pull'), command=self._pull)

        # events
        self._w_mng_tree.bind('<ButtonRelease-1>', self._fill_repo_detail)
        self._w_mng_tree.bind('<Any-KeyRelease>', self._fill_repo_detail)
        self._w_mng_tree.bind('<Button-3>', self._context_menu)

    def _context_menu(self, event=None):
        """Method sets context menu

        Args:
            event (obj): event

        Returns:
            void

        """

        self._w_mng_menu.tk_popup(event.x_root, event.y_root)

    def _set_config(self):
        """Method sets configuration gui

        Args:
           none

        Returns:
           void

        """

        row = 0
        font = ('Arial', 10, 'bold')
        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_title'), font=font).grid(row=row, column=0, sticky='w')
        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_url')).grid(row=row + 1, column=0, sticky='e')
        self._w_mng_url = tk.Entry(self._w_mng_frame_right, width=70)
        self._w_mng_url.grid(row=row + 1, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_user')).grid(row=row + 2, column=0, sticky='e')
        self._w_mng_user = tk.Entry(self._w_mng_frame_right, width=20)
        self._w_mng_user.grid(row=row + 2, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_password')).grid(row=row + 3, column=0, sticky='e')
        self._w_mng_passw = tk.Entry(self._w_mng_frame_right, width=20)
        self._w_mng_passw.grid(row=row + 3, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_name')).grid(row=row + 4, column=0, sticky='e')
        self._w_mng_name = tk.Entry(self._w_mng_frame_right, width=40)
        self._w_mng_name.grid(row=row + 4, column=1, padx=3, pady=3, sticky='w')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_email')).grid(row=row + 5, column=0, sticky='e')
        self._w_mng_email = tk.Entry(self._w_mng_frame_right, width=40)
        self._w_mng_email.grid(row=row + 5, column=1, padx=3, pady=3, sticky='w')

        error = tk.Label(self._w_mng_frame_right, text='', foreground='#FF0000')
        error.grid(row=row + 6, column=1, sticky='w')
        self._w_mng_btn_save = tk.Button(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_config_save'),
                                         command=lambda: self._save_config(self._w_mng_url.get(), self._w_mng_user.get(), self._w_mng_passw.get(),
                                                         self._w_mng_name.get(), self._w_mng_email.get(), error))
        self._w_mng_btn_save.grid(row=row + 6, column=2, padx=3, pady=3, sticky='e')

    def _set_commit(self):
        """Method sets commit gui

        Args:
           none

        Returns:
           void

        """

        row = 7
        font = ('Arial', 10, 'bold')
        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_title'), font=font).grid(row=row, column=0, sticky='w')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_message')).grid(row=row + 1, column=0, sticky='e')
        self._w_mng_msg = tk.Text(self._w_mng_frame_right, background='#FFFFFF', height=7, width=50)
        self._w_mng_msg.grid(row=row + 1, column=1, rowspan=2, sticky='w')
        row += 1

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_author')).grid(row=row + 3, column=0, sticky='e')
        self._w_mng_author = tk.Entry(self._w_mng_frame_right, width=40)
        self._w_mng_author.grid(row=row + 3, column=1, padx=3, pady=3, sticky='w')

        self._w_mng_push = tk.BooleanVar(value=True)
        tk.Checkbutton(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_push'), variable=self._w_mng_push).grid(row=row + 3, column=2, sticky='e')

        error = tk.Label(self._w_mng_frame_right, text='', foreground='#FF0000')
        error.grid(row=row + 4, column=1, sticky='w')
        self._w_mng_btn_commit = tk.Button(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_commit'),
                                           command=lambda: self._commit(self._w_mng_msg.get('1.0', 'end-1c'), self._w_mng_author.get(), [], self._w_mng_push.get(), error))
        self._w_mng_btn_commit.grid(row=row + 4, column=2, padx=3, pady=3, sticky='e')

        tk.Label(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_files'), font=font).grid(row=row + 5, column=0, sticky='w')

        self._w_mng_select_all = tk.BooleanVar(value=False)
        tk.Checkbutton(self._w_mng_frame_right, text=self.trn.msg('htk_gitclient_repomanager_commit_select_all'), variable=self._w_mng_select_all,
                       command=lambda: self._select_all_files(self._w_mng_select_all.get())).grid(row=row + 6, column=1, sticky='w')

        self._w_mng_files_bar = ttk.Scrollbar(self._w_mng_frame_right, orient=tk.VERTICAL)
        self._w_mng_files = ttk.Treeview(self._w_mng_frame_right, columns=('operation', 'file'), show='tree', displaycolumns=('operation', 'file'), height=10, selectmode='browse',
                                         yscrollcommand=self._w_mng_files_bar.set)
        self._w_mng_files_bar.configure(command=self._w_mng_files.yview)
        self._w_mng_files.grid(row=row + 7, column=1, sticky=tk.NSEW)
        self._w_mng_files_bar.grid(row=row + 7, column=2, sticky='nsw')

        self._w_mng_files.column('#0', stretch=False, width=40)
        self._w_mng_files.column('operation', stretch=False, width=50)
        self._w_mng_files.column('file', stretch=True, width=200)

        self._w_mng_files.bind('<ButtonRelease-1>', self._select_file)
        self._w_mng_files.bind('<Any-KeyRelease>', self._select_file)

    def _set_dirpath(self, entry):
        """Method sets dirpath

        Args:
           entry (obj): entry reference

        Returns:
           void

        """

        entry.delete(0, tk.END)
        entry.insert(tk.END, tkfd.askdirectory())

    def _clone_repo(self, url, dirpath, user='', passw='', error=None):
        """Method clones repository

        Args:
           url (str): repository url
           dirpath (str): directory path
           user (str): username
           pass (str): password
           error (obj): error label reference

        Returns:
           void

        """

        if (error is not None):
            error.config(text='')
            proj_name = dirpath.split('/')[-1]
            if (len(url) == 0):
                error.config(text=self.trn.msg('htk_gitclient_mandatory_field', self.trn.msg('htk_gitclient_clone_url')))
                return
            elif (len(dirpath) == 0):
                error.config(text=self.trn.msg('htk_gitclient_mandatory_field', self.trn.msg('htk_gitclient_clone_dirpath')))
                return
            elif (proj_name in self.explorer._projects):
                error.config(text=self.trn.msg('htk_gitclient_clone_project_exist', proj_name))
                return

        if (self._w_clone is not None):
            self._w_clone.destroy()

        self.logger.info(self.trn.msg('htk_gitclient_clone_start', url))
        self.msgqueue.write_msg(self._task_clone_repo, [url, dirpath, user, passw])

    def _task_clone_repo(self, url, dirpath, user, passw):
        """Method clones repository as task

        Args:
           url (str): repository url
           dirpath (str): directory path
           user (str): username
           pass (str): password

        Returns:
           void

        """

        repo = None
        try:
            url_auth = self._prepare_url(url, user, passw)
            repo = Repo.clone_from(url_auth, dirpath)
            self.logger.info(self.trn.msg('htk_gitclient_clone_finish'))
            self._create_project(url, dirpath, user, passw)
        except Exception as ex:
            self.logger.error(ex)
            if (os.path.exists(dirpath)):
                rmtree(dirpath)
        finally:
            if (repo is not None):
                repo.close()

    def _create_project(self, url, dirpath, user, passw):
        """Method creates project from repository

        Args:
           url (str): repository url
           dirpath (str): directory path
           user (str): username
           pass (str): password

        Returns:
           void

        """

        dirpath = fix_path(dirpath)
        proj_name = dirpath.split('/')[-1]
        self.explorer._projects[proj_name] = {'path': dirpath, 'pythonpath': [dirpath + '/lib/yodalib', dirpath + '/helpers/yodahelpers'],
                                              'git': {'url': url, 'username': user, 'password': passw, 'name': '', 'email': ''}}
        node = self.explorer._tree.insert('', 'end', text=proj_name, values=(dirpath, 'directory'))
        self.explorer._populate_tree(node)
        self.logger.info(self.trn.msg('htk_core_project_created', proj_name))
        self.config.data['Projects'] = self.explorer._projects
        self.explorer.autocompleter.update_pythonpath()
        self.config.save()

    def _fill_repo_detail(self, event=None):
        """Method fills repository detail

        Args:
            event (obj): event

        Returns:
            void

        """

        item = self._w_mng_tree.selection()
        if (len(item) == 0):
            return

        project = self._w_mng_tree.item(item)['text']
        cfg = self.config.data['Projects'][project]
        repo_path = cfg['path']
        cfg = cfg['git']

        self._w_mng_url.delete(0, tk.END)
        self._w_mng_url.insert(tk.END, cfg['url'])
        self._w_mng_user.delete(0, tk.END)
        self._w_mng_user.insert(tk.END, cfg['username'])
        self._w_mng_passw.delete(0, tk.END)
        self._w_mng_passw.insert(tk.END, cfg['password'])
        self._w_mng_name.delete(0, tk.END)
        self._w_mng_name.insert(tk.END, cfg['name'])
        self._w_mng_email.delete(0, tk.END)
        self._w_mng_email.insert(tk.END, cfg['email'])

        self._w_mng_author.delete(0, tk.END)
        author = '{0} <{1}>'.format(cfg['name'], cfg['email']) if (cfg['email'] != '') else ''
        self._w_mng_author.insert(tk.END, author)
        self._w_mng_msg.delete('1.0', 'end')

        self._fill_changed_files(repo_path)

    def _save_config(self, url, user='', passw='', name='', email='', error=None):
        """Method saves configuration

        Args:
           url (str): repository url
           user (str): username
           passw (str): password
           name (str): author name
           email (str): author email
           error (obj): error label reference

        Returns:
           void

        """

        item = self._w_mng_tree.selection()
        if (len(item) == 0):
            return

        if (error is not None):
            error.config(text='')
            if (len(url) == 0):
                error.config(text=self.trn.msg('htk_gitclient_mandatory_field', self.trn.msg('htk_gitclient_repomanager_config_url')))
                return

        project = self._w_mng_tree.item(item)['text']
        repo_path = self.config.data['Projects'][project]['path']
        cfg = self.config.data['Projects'][project]['git']

        repo = None
        try:
            if ([cfg['url'], cfg['username'], cfg['password'], cfg['name'], cfg['email']] != [url, user, passw, name, email]):
                repo = Repo(repo_path)
                repo.git.remote('set-url', 'origin', self._prepare_url(url, user, passw))
                repo.git.config('user.name', name)
                repo.git.config('user.email', email)

                cfg['url'] = url
                cfg['username'] = user
                cfg['password'] = passw
                cfg['name'] = name
                cfg['email'] = email
                self.config.save()
                self.logger.debug(self.trn.msg('htk_gitclient_repomanager_config_saved', project))

        except Exception as ex:
            self.logger.error(ex)
        finally:
            if (repo is not None):
                repo.close()

    def _commit(self, msg, author, files, push=False, error=None):
        """Method performs commit to local repository

        Args:
           msg (str): commit message
           author (str): author
           files (list): files to commit
           push (bool): push commit to remote repository
           error (obj): error label reference

        Returns:
           void

        """

        item = self._w_mng_tree.selection()
        if (len(item) == 0):
            return

        if (error is not None):
            error.config(text='')
            if (len(msg) == 0):
                error.config(text=self.trn.msg('htk_gitclient_mandatory_field', self.trn.msg('htk_gitclient_repomanager_commit_message')))
                return
            elif (len(author) == 0):
                error.config(text=self.trn.msg('htk_gitclient_mandatory_field', self.trn.msg('htk_gitclient_repomanager_commit_author')))
                return

        cnt, files = 0, []
        for i in self._w_mng_files.get_children():
            item = self._w_mng_files.item(i)
            if (item['text'] != ''):
                cnt += 1
                files.append(item['values'][1])

        if (error is not None and cnt == 0):
            error.config(text=self.trn.msg('htk_gitclient_repomanager_commit_no_files_selected'))
            return

        repo = None
        try:
            project = self._w_mng_tree.item(self._w_mng_tree.selection())['text']
            repo_path = self.config.data['Projects'][project]['path']
            repo = Repo(repo_path)
            repo.git.add('--all', files)
            repo.git.commit(message=msg, author=author)
            self.logger.info(self.trn.msg('htk_gitclient_repomanager_commit_finish', project))

            if (push):
                self._push()

        except Exception as ex:
            self.logger.error(ex)
        finally:
            if (repo is not None):
                repo.close()

    def _push(self, event=None):
        """Method performs push to remote repository

        Args:
           event (obj): event

        Returns:
           void

        """

        item = self._w_mng_tree.selection()
        if (len(item) == 0):
            return

        project = self._w_mng_tree.item(item)['text']
        repo_path = self.config.data['Projects'][project]['path']
        self.logger.info(self.trn.msg('htk_gitclient_repomanager_push_start', project))
        self.msgqueue.write_msg(self._task_push, [repo_path])

    def _task_push(self, repo_path):
        """Method performs push to remote repository as task

        Args:
           repo_path (str): repository path

        Returns:
           void

        """

        repo = None
        try:
            repo = Repo(repo_path)
            repo.git.push('origin')
            self.logger.info(self.trn.msg('htk_gitclient_repomanager_push_finish'))

        except Exception as ex:
            self.logger.error(ex)
        finally:
            if (repo is not None):
                repo.close()

    def _pull(self, event=None):
        """Method performs pull from remote repository

        Args:
           event (obj): event

        Returns:
           void

        """

        item = self._w_mng_tree.selection()
        if (len(item) == 0):
            return

        project = self._w_mng_tree.item(item)['text']
        repo_path = self.config.data['Projects'][project]['path']
        self.logger.info(self.trn.msg('htk_gitclient_repomanager_pull_start', project))
        self.msgqueue.write_msg(self._task_pull, [repo_path])

    def _task_pull(self, repo_path):
        """Method performs pull from remote repository as task

        Args:
           repo_path (str): repository path

        Returns:
           void

        """

        repo = None
        try:
            repo = Repo(repo_path)
            repo.git.pull('origin')
            self.explorer.refresh(path=repo_path)
            self.logger.info(self.trn.msg('htk_gitclient_repomanager_pull_finish'))

        except Exception as ex:
            self.logger.error(ex)
        finally:
            if (repo is not None):
                repo.close()

    def _fill_changed_files(self, repo_path):
        """Method fills changed

        Args:
           repo_path (str): repository path

        Returns:
           void

        """

        self._w_mng_files.delete(*self._w_mng_files.get_children())
        changes = self._get_changed_files(repo_path)
        
        for operation, files in changes.items():
            for f in files:
                self._w_mng_files.insert('', 'end', text='', values=(operation, f))

    def _get_changed_files(self, repo_path):
        """Method gets changed files available for commit

        Args:
           repo_path (str): repository path

        Returns:
           dict

        """

        repo, files = None, []
        try:
            repo = Repo(repo_path)
            status = repo.git.status('--porcelain')

            added, modified, deleted = [], [], []
            for rec in status.splitlines():
                operation, fname = rec[:2], rec[3:]
                if ('?' in operation):
                    added.append(fname)
                elif ('M' in operation):
                    modified.append(fname)
                elif ('D' in operation):
                    deleted.append(fname)

            files = {
                     'add'    : added,
                     'modify' : modified,
                     'delete' : deleted
                    }

        except Exception as ex:
            self.logger.error(ex)
        finally:
            if (repo is not None):
                repo.close()

        return files

    def _select_file(self, event=None):
        """Method selects or deselects file for commit

        Args:
           event (obj): event

        Returns:
           void

        """

        sel = self._w_mng_files.selection()
        if (len(sel) == 0):
            return

        item = self._w_mng_files.item(sel)
        self._w_mng_files.item(sel, text='X' if item['text'] == '' else '')
        
    def _select_all_files(self, value):
        """Method selects or deselects all files for commit

        Args:
           value (bool): requested value

        Returns:
           void

        """

        value = 'X' if (value) else ''
        for i in self._w_mng_files.get_children():
            self._w_mng_files.item(i, text=value)

    def _prepare_url(self, url, user=None, passw=None):
        """Method prepares url with authentication

        Args:
           url (str): repository URL
           user (str): username
           passw (str): password

        Returns:
           str

        """

        if (len(user) > 0 and '://' in url):
            url = url.replace('://', '://{0}:{1}@'.format(user, passw))

        return url
