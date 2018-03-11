def get_attr(name, get_class_name=False):

    attr = getattr(self.root.yoda_tree, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root.yoda_tree
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def select(tree_path, get_item=False):

    tree = self.root.yoda_tree._tree
    item, found = None, False
    for t in tree_path:
        items = tree.get_children(item) if (item != None) else tree.get_children()
        for i in items:
            text = tree.item(i)['text']
            if (text == t):
                item, found = i, True
        if (found):
            found = False
            tree.item(item, open=True)
        else:
            return False

    tree.selection_set(item)

    return item if (get_item) else True

def get_tab_content():

    content = self.root.editor.nb.get_current_content()

    return content

def click_context_menu(key, item):

    menu = {
            'scenario'  : {
                           'scenario' : 0,
                           'case' : 1,
                           'postreq' : 2,
                           'events' : 3
                          },
            'case'      : {
                           'condition' : 0,
                           'events' : 1
                          },
            'condition' : {
                           'events' : 0
                          }
           }

    self.root.yoda_tree._menu.invoke(menu[key][item])
