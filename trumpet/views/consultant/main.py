from trumpet.views.base import prepare_layout
from trumpet.views.base import BaseViewer

from trumpet.views.consultant.base import prepare_base_layout

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Consultant Main'
    layout.header = 'Consultant Main'
    layout.subheader = 'Main Page'
    

    

class MainViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.layout.resources.fancybox.need()
        self.layout.resources.fullcalendar.need()
        template = 'trumpet:templates/consult/main-view.mako'
        env = dict()
        content = self.render(template, env)
        from haberdashery.resources import maincalendar
        maincalendar.need()
        self.layout.content = content
        
