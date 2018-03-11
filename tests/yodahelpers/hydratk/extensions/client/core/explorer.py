def get_attr(name, get_class_name=False):

    attr = getattr(self.root.explorer, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root.explorer
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def click_menu(item):

    menu = {
            'New File' : 0,
            'New Directory' : 1,
            'New Project' : 2,
            'New Helper' : 3,
            'New Library' : 4,
            'New Test' : 5,
            'New Archive' : 6,
            'New Draft' : 7,
            'Open' : 1,
            'Save As' : 2,
            'Save' : 3,
            'Exit' : 5
           }

    if ('New' in item):
        self.root.menus['file_new'].invoke(menu[item])
    else:
        self.root.menus['file'].invoke(menu[item])

def click_context_menu(item):

    menu = {
            'New File' : 0,
            'New Directory' : 1,
            'New Project' : 2,
            'New Helper' : 3,
            'New Library' : 4,
            'New Test' : 5,
            'New Archive' : 6,
            'New Draft' : 7,
            'Open' : 1,
            'Copy' : 2,
            'Paste' : 3,
            'Delete' : 4,
            'Refresh' : 5
           }

    if ('New' in item):
        self.root.explorer._menu_new.invoke(menu[item])
    else:
        self.root.explorer._menu.invoke(menu[item])

def get_tab_cnt():

    cnt = len(self.root.editor.nb.tab_refs)

    return cnt

def close_tabs():

    nb = self.root.editor.nb

    for i in range(len(nb._tab_refs) - 1, -1, -1):
        nb.close_tab(i, force=True)

def create_project(path):

    self.root.explorer.new_project(path)
    proj_name = path.split('/')[-1]
    config = self.root.explorer._projects[proj_name]

    return config

def clean():

    from shutil import rmtree
    exp = self.root.explorer

    for k, v in exp._projects.items():
        path = exp._projects[k]['path']
        rmtree(path)

    exp._tree.delete(*exp._tree.get_children())
    exp._projects = {}
    exp.config.data['Projects'] = exp._projects
    exp.config.save()

def select(tree_path):

    exp = self.root.explorer
    tree = exp._tree
    item, found = None, False
    for t in tree_path:
        items = tree.get_children(item) if (item != None) else tree.get_children()
        for i in items:
            text = tree.item(i)['text']
            if (text == t):
                item, found = i, True
        if (found):
            found = False
            exp._populate_tree(item)
            tree.item(item, open=True)
        else:
            return False

    tree.selection_set(item)
    return True
