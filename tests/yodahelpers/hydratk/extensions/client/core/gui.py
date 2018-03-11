def get_attr(name, get_class_name=False):

    attr = getattr(self.root, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr
