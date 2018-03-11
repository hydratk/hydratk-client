def get_attr(name, get_class_name=False):

    attr = getattr(self.root.logger, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def set_attr(name, value):

    setattr(self.root.logger, name, value)

def get_property(name, get_class_name=False):

    obj = self.root.logger
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def get_text():

    text = self.root.logger._log.get('1.0', 'end')

    return text

def click_context_menu(item):

    menu = {
            'Clear' : 0
           }

    self.root.logger._menu.invoke(menu[item])
