class BaseLayout(object):
    title = None

    # main bar
    brand = None
    main_menu = None
    shortcut_menu = None
    user_menu = None
    # FIXME: use ordered dict
    options_menus = None

    # page content
    header = None
    subheader = None
    sidebar = None
    content = None
    footer = None

    # status bar
    # FIXME: I don't know what to do here just yet
    status_bar = None
    status_message_box = None
    status = None
    
    # dynamic resources
    js = []
    css = []
    
    # legacy members
    # FIXME: make @property methods with deprecation warnings
    ctx_menu = None
    widgetbox = None
    

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.app_url = self.request.application_url

    

class MobileLayout(object):
    title = "MobileLayout"
    header = 'MobileHeader'
    subheader = 'MobileSubheader'
    main_menu = 'TopBar'
    ctx_menu = 'LeftMenu'
    content = 'Content'
    footer = 'Footer'
    widgetbox = ''
    js = []
    css = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.app_url = self.request.application_url
