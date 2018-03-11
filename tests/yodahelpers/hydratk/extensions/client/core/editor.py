def get_attr(name, get_class_name=False):

    attr = getattr(self.root.editor, name)
    if (get_class_name):
        attr = attr.__class__.__name__

    return attr

def get_property(name, get_class_name=False):

    obj = self.root.editor
    prop = getattr(obj, name)
    attr = getattr(obj, '_{0}'.format(name))

    if (get_class_name):
        prop = prop.__class__.__name__
        attr = attr.__class__.__name__

    return prop, attr

def get_tab_cnt():

    cnt = len(self.root.editor.nb.tab_refs)

    return cnt

def close_tabs():

    nb = self.root.editor.nb

    for i in range(len(nb._tab_refs) - 1, -1, -1):
        nb.close_tab(i, force=True)
        
def get_tab_content():

    content = self.root.editor.nb.get_current_content()

    return content

def click_menu(key, item):

    menu = {
            'file' : {
                      'Open' : 1,
                      'Save' : 2,
                      'Save As' : 3
                     },
            'edit' : {
                      'Undo' : 0,
                      'Redo' : 1,
                      'Cut' : 3,
                      'Copy' : 4,
                      'Paste' : 5,
                      'Delete' : 6,
                      'Select All' : 7,
                      'Goto' : 9,
                      'Find' : 10,
                      'Replace' : 11
                     },
            'view' : {
                      'Line numbers' : 0,
                      'Info bar' : 1,
                      'Increase font' : 3,
                      'Decrease font' : 4
                     }
           }

    self.root.menus[key].invoke(menu[key][item])

def click_context_menu(item):

    menu = {
            'Undo' : 0,
            'Redo' : 1,
            'Cut' : 2,
            'Copy' : 3,
            'Paste' : 4,
            'Delete' : 5,
            'Select All' : 6,
            'Goto' : 7,
            'Find' : 8,
            'Replace' : 9
           }

    tab = self.root.editor.nb.get_current_tab()
    tab._menu.invoke(menu[item])

def write_text(text):

    tab = self.root.editor.nb.get_current_tab()
    tab._text.insert('end', text)
    tab._text.mark_set('insert', 1.0)

def mark(idx1, idx2):

    tab = self.root.editor.nb.get_current_tab()
    tab._text.tag_remove('sel', '1.0', 'end')
    tab._text.tag_add('sel', idx1, idx2)

def get_ln_bar():

    tab = self.root.editor.nb.get_current_tab()
    content = tab._ln_bar.get('1.0', 'end')

    return content

def get_info_bar():

    tab = self.root.editor.nb.get_current_tab()
    content = tab._info_bar['text']

    return content

def get_font():

    tab = self.root.editor.nb.get_current_tab()
    font = tab._text['font']

    return font

def handle_goto(line):

    ed = self.root.editor
    ed._win_goto_entry.insert('end', line)
    ed._win_goto_btn.invoke()

    tab = ed.nb.get_current_tab()
    line = tab._info_bar['text'][0]

    return line

def handle_find(text, find_all=False, ignore_case=False, regexp=False):

    ed = self.root.editor
    ed._win_find_entry.insert('end', text)
    ed._win_find_find_all.set(find_all)
    ed._win_find_ignore_case.set(ignore_case)
    ed._win_find_regexp.set(regexp)
    ed._win_find_btn.invoke()

    tab = ed.nb.get_current_tab()
    result = len(tab._text.tag_ranges('match')) > 0

    return result

def handle_replace(find_str, replace_str, replace_all=False, ignore_case=False, regexp=False):

    ed = self.root.editor
    ed._win_replace_find_entry.insert('end', find_str)
    ed._win_replace_replace_entry.insert('end', replace_str)
    ed._win_replace_replace_all.set(replace_all)
    ed._win_replace_ignore_case.set(ignore_case)
    ed._win_replace_regexp.set(regexp)
    ed._win_replace_btn.invoke()

    content = ed.nb.get_current_content()
    result = (find_str not in content) and (replace_str in content)

    return result
