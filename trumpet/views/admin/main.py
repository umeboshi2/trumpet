from trumpet.resources import Resource


class AdminRoot(Resource):
    __acl__ = [
        (Allow, 'admin', 'admin'),
        ]

    def __init__(self, request):
        for key in ['users', 'images', 'sitetext',
                    'dbadmin', 'site_templates',
                    'sitecontent_mgr']:
            self[key] = Resource(key, self)
            

    
def admin_root_factory(request):
    return AdminRoot(request)

        
