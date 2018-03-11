def get_attr(name, get_class_name=False):

    attr = getattr(self.root.trn, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr
