def get_instance():

    tab = self.root.editor.nb.get_current_tab()
    if (tab != None):
        inst = tab.autocompleter
    else:
        from hydratk.extensions.client.core.autocompleter import AutoCompleter
        inst = AutoCompleter.get_instance()

    return inst

def get_attr(inst, name, get_class_name=False):

    attr = getattr(inst, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(inst, name, get_class_name=False):

    prop = getattr(inst, name)
    attr = getattr(inst, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def complete(text):

    tab = self.root.editor.nb.get_current_tab()
    tab._path = 'test.py'
    tab._text.insert('end', text)
    tab.autocompleter.show_completion(tab)
