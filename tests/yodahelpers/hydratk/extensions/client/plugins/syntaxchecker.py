def get_instance():

    inst = self.root.plugins['syntaxchecker']

    return inst

def get_attr(name, get_class_name=False):

    attr = getattr(self.root.plugins['syntaxchecker'], name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root.plugins['syntaxchecker']
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def get_plugin_attrs():

    obj = self.root.plugins['syntaxchecker']
    attrs = [obj.plugin_id, obj.plugin_name, obj.plugin_version, obj.plugin_author, obj.plugin_year]

    return attrs
