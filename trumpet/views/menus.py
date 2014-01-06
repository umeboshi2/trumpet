from formencode.htmlgen import html, Element

from trumpet import import_OrderedDict
OrderedDict = import_OrderedDict()


class Table(Element):
    def __init__(self, **kw):
        Element.__init__(self, 'table', {})


class UL(Element):
    def __init__(self, **kw):
        Element.__init__(self, 'ul', {})


class Nav(Element):
    def __init__(self, **kw):
        Element.__init__(self, 'nav', {})


class Div(Element):    
    def __init__(self, **kw):
        Element.__init__(self, 'div', {})


class BaseMenu(UL):
    def __init__(self, header='BaseMenu', **args):
        super(BaseMenu, self).__init__(**args)
        super(BaseMenu, self).set('class', 'ctx-menu nav navbar-nav')
        self._menu = {}

        # setup dropdown menu and header anchor
        self.dropdown = html.li()
        self.dropdown.set('class', 'dropdown')
        self.header_anchor = html.a(header, class_='dropdown-toggle')
        self.header_anchor.set('data-toggle', 'dropdown')
        # we append a caret to the end of the header
        # to demonstrate that this is a dropdown menu
        caret = html.b(' ', class_="caret")
        # append the objects
        self.header_anchor.append(caret)
        self.append(self.dropdown)
        self.dropdown.append(self.header_anchor)
        # create and append the menu container
        self.menu_list = UL()
        self.menu_list.set('class', 'dropdown-menu')
        self.dropdown.append(self.menu_list)

    # setting the anchor text doesn't seem to
    # bother the caret appended to the anchor
    def set_header(self, header=None):
        self.header_anchor.text = header
        
    def append_new_entry(self, name, page):
        self._menu[name] = html.a(name, href=page)
        li = html.li(self._menu[name])
        self.menu_list.append(li)
        

    def set_new_entries(self, entries, header=None):
        self.menu_list.clear()
        self.menu_list.set('class', 'dropdown-menu')
        self.set_header(header)
        for name, page in entries:
            self.append_new_entry(name, page)

    def output3(self):
        from warnings import warn
        msg = ".output() is deprecated, use .render()"
        warn(msg, DeprecationWarning)
        return unicode(self)

    def render(self):
        return unicode(self)
    
    
class TopBar(object):
    def __init__(self, title):
        self.title = title
        self.entries = OrderedDict()

    def render(self):
        data = ''
        template = '<li class="top-bar-button"><a href="%s">%s</a></li>'
        for name, page in self.entries.items():
            data += template % (page, name)
        return data
    
ALERT_PRIORITY = ['success', 'info', 'warning', 'danger']

class Alert(Div):
    def __init__(self, priority, *args):
        super(Alert, self).__init__(*args)
        self.set_priority(priority)
        
    def set_priority(self, priority, dismissable=False):
        if priority not in ALERT_PRIORITY:
            raise RuntimeError, "Bad priority %s" % priority
        self.priority = priority
        cl = 'alert alert-%s' % priority
        if dismissable:
            cl = '%s alert-dismissable' % cl
        self.set('class', cl)
        

    def set_dismiss_button(self):
        if self.priority is None:
            raise NoPrioritySetError, "set a priority first."
        b = html.button('&times;')
        b.set('type', 'button')
        b.set('class', 'close')
        b.set('data-dismiss', 'alert')
        # FIXME: look at this later
        b.set('aria-hidden', 'true')
        self.append(b)
        self.set_priority(self.priority, dismissable=True)
        
    
