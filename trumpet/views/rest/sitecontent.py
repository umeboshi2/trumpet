from cornice.resource import resource, view

from trumpet.models.sitecontent import SiteTemplate
from trumpet.models.sitecontent import SiteCSS, SiteJS
from trumpet.models.sitecontent import SitePath

from trumpet.models.sitecontent import SitePathCSS, SitePathJS


from trumpet.models.sitecontent import  SiteAppResource as DBSiteAppResource


from trumpet.managers.admin.sitecontent import SiteContentManager

from trumpet.managers.admin.sitewebview import SiteAppManager

from trumpet.views.rest.base import BaseResource

# FIXME: this needs to be in manager
import transaction


@resource(collection_path='/rest/sitepath', path='/rest/sitepath/{id}',
          permission='admin')
class SitePathResource(BaseResource):
    dbmodel = SitePath

    def __init__(self, request):
        super(SitePathResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.path_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        obj = self.mgr.add_sitepath(name)
        data = dict(obj=obj.serialize(), result='success')
        return data

    def delete(self):
        # FIXME: THIS NEEDS TO BE IN MANAGER 
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.path_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')

@resource(collection_path='/rest/sitepath/{path_id}/css',
          path='/rest/sitepath/{path_id}/css/{id}',
          permission='admin')
class SitePathCSSResource(BaseResource):
    dbmodel = SitePathCSS

    def __init__(self, request):
        super(SitePathCSSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)

    def collection_get(self):
        path_id = int(self.request.matchdict['path_id'])
        csslist = self.mgr.get_css_for_path(path_id)
        csslist = [o.serialize() for o in csslist]
        return dict(data=csslist, result='success')

    def collection_post(self):
        css_id = self.request.json['id']
        path_id = int(self.request.matchdict['path_id'])
        obj = self.mgr.attach_css_to_path(path_id, css_id)
        return dict(obj=obj.serialize(), result='success')

    def delete(self):
        path_id = int(self.request.matchdict['path_id'])
        css_id = int(self.request.matchdict['id'])
        self.mgr.detach_css(path_id, css_id)

    def get(self):
        css_id = int(self.request.matchdict['id'])
        css = self.mgr.css_query().get(css_id)
        return dict(data=css.serialize(), result='success')
    
        
@resource(collection_path='/rest/sitepath/{path_id}/js',
          path='/rest/sitepath/{path_id}/js/{id}',
          permission='admin')
class SitePathJSResource(BaseResource):
    dbmodel = SitePathJS
    

    def __init__(self, request):
        super(SitePathJSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)

    def collection_get(self):
        path_id = int(self.request.matchdict['path_id'])
        jslist = self.mgr.get_js_for_path(path_id)
        jslist = [o.serialize() for o in jslist]
        return dict(data=jslist, result='success')

    def collection_post(self):
        js_id = self.request.json['id']
        path_id = int(self.request.matchdict['path_id'])
        obj = self.mgr.attach_js_to_path(path_id, js_id)
        return dict(obj=obj.serialize(), result='success')

    def delete(self):
        path_id = int(self.request.matchdict['path_id'])
        js_id = int(self.request.matchdict['id'])
        self.mgr.detach_js(path_id, js_id)

    def get(self):
        js_id = int(self.request.matchdict['id'])
        js = self.mgr.js_query().get(js_id)
        return dict(data=js.serialize(), result='success')
    
        
@resource(collection_path='/rest/sitetmpl', path='/rest/sitetmpl/{id}',
          permission='admin')
class SiteTemplateResource(BaseResource):
    dbmodel = SiteTemplate

    def __init__(self, request):
        super(SiteTemplateResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.tmpl_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_template(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_template(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.tmpl_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')


@resource(collection_path='/rest/sitecss', path='/rest/sitecss/{id}',
          permission='admin')
class SiteCSSResource(BaseResource):
    dbmodel = SiteCSS

    def __init__(self, request):
        super(SiteCSSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.css_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_css(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_css(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.css_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')
    
@resource(collection_path='/rest/sitejs', path='/rest/sitejs/{id}',
          permission='admin')
class SiteJSResource(BaseResource):
    dbmodel = SiteJS

    def __init__(self, request):
        super(SiteJSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.js_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_js(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_js(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.js_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')
    



@resource(collection_path='/rest/siteapp',
          path='/rest/siteapp/{id}', permission='admin')
class RESTSiteAppResource(BaseResource):
    dbmodel = DBSiteAppResource
    def __init__(self, request):
        super(RESTSiteAppResource, self).__init__(request)
        self.mgr = SiteAppManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        user_id = self.get_current_user_id()
        r = self.mgr.add_resource(name, content, user_id)
        return dict(obj=r.serialize(), result='success')

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        user_id = self.get_current_user_id()
        r = self.mgr.update_resource(id, user_id, content=content)
        return dict(obj=r.serialize(), result='success')

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_resource(id)
        return dict(result='success')
