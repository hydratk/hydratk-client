def get_attr(name, get_class_name=False):

    attr = getattr(self.root.help, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_attrs(names, get_class_name=False):

    attrs = []
    for name in names:
        attr = getattr(self.root.help, name)
        if (get_class_name):
            attr = attr.__class__.__name__
        attrs.append(attr)

    return attrs

def get_property(name, get_class_name=False):

    obj = self.root.help
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def click_menu(item):

    menu = {
            'Web tutorial' : 0,
            'Web documentation' : 1,
            'About' : 3
           }

    self.root.menus['help'].invoke(menu[item])

def click_button(button):

    buttons = {
               'web' : '_btn_web',
               'email' : '_btn_email',
               'ok' : '_btn_ok'
              }
    getattr(self.root.help, buttons[button]).invoke()

def get_text():

    text = self.root.help._text.get('1.0', 'end')

    return text
