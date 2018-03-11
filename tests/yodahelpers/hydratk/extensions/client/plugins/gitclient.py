def get_instance():

    inst = self.root.plugins['gitclient']

    return inst

def get_attr(name, get_class_name=False):

    attr = getattr(self.root.plugins['gitclient'], name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root.plugins['gitclient']
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def get_plugin_attrs():

    obj = self.root.plugins['gitclient']
    attrs = [obj.plugin_id, obj.plugin_name, obj.plugin_version, obj.plugin_author, obj.plugin_year]

    return attrs

def clone_repo(url, user, passw, dirpath):
    
    obj = self.root.plugins['gitclient']
    obj._win_clone()
    obj._w_clone_url.insert('end', url)
    obj._w_clone_user.insert('end', user)
    obj._w_clone_passw.insert('end', passw)
    obj._w_clone_dirpath.insert('end', dirpath)
    obj._w_clone_btn.invoke()

    proj_name = dirpath.split('/')[-1]
    config = self.root.explorer._projects[proj_name]

    return config

def select_repo(idx):

    obj = self.root.plugins['gitclient']
    obj._win_repomanager()
    tree = obj._w_mng_tree
    items = tree.get_children()
    
    if (len(items) >= idx):
        tree.selection_set(items[idx])
        return True
    else:
        return False

def click_context_menu(item):

    menu = {
            'Push' : 0,
            'Pull' : 1
           }

    obj = self.root.plugins['gitclient']
    obj._w_mng_menu.invoke(menu[item])
    obj._w_mng.destroy()

def save_config(proj_name, url, user, passw, name, email):

    obj = self.root.plugins['gitclient']
    obj._w_mng_url.insert('end', url)
    obj._w_mng_user.insert('end', user)
    obj._w_mng_passw.insert('end', passw)
    obj._w_mng_name.insert('end', name)
    obj._w_mng_email.insert('end', email)
    obj._w_mng_btn_save.invoke()
    obj._w_mng.destroy()

    config = self.root.explorer._projects[proj_name]

    return config

def commit(repo_path, message, author):

    obj = self.root.plugins['gitclient']
    files = obj._get_changed_files(repo_path)

    obj._fill_changed_files(repo_path)
    obj._w_mng_msg.insert('end', message)
    obj._w_mng_author.insert('end', author)
    obj._w_mng_push.set(False)
    obj._w_mng_select_all.set(True)
    obj._select_all_files(True)
    obj._w_mng_btn_commit.invoke()
    obj._w_mng.destroy()

    return files
