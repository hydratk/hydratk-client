def get_instance():

    from hydratk.extensions.client.core.plugin import Plugin
    inst = Plugin(self.root)

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
