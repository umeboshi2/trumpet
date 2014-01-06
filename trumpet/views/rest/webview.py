from sqlalchemy.orm.exc import NoResultFound

from pyramid.security import Everyone, Authenticated

from cornice.resource import resource, view

from trumpet.views.rest.base import BaseResource

from trumpet.models.sitecontent import SiteWebview
from trumpet.models.sitecontent import SiteLayoutField
from trumpet.models.sitecontent import SiteLayoutModel
from trumpet.models.sitecontent import SiteLayoutModelField
from trumpet.models.sitecontent import SiteWebviewCSS
from trumpet.models.sitecontent import SiteWebviewJS


from trumpet.managers.admin.sitewebview import SiteWebviewManager

class BaseWebViewResource(BaseResource):
    def __init__(self, request):
        super(BaseWebViewResource, self).__init__(request)
        self.mgr = SiteWebviewManager(self.db)
        
    def collection_get(self):
        q = self.db.query(self.dbmodel)
        return dict(data=[o.serialize() for o in q])

    def get(self):
        id = int(self.request.matchdict['id'])
        return self.db.query(self.dbmodel).get(id).serialize()
    
    
        
        
    
    
@resource(collection_path='/rest/admin/layoutfields',
          path='/rest/admin/layoutfields/{id}',
          permission='admin')
class LayoutFieldResource(BaseWebViewResource):
    dbmodel = SiteLayoutField

    def collection_post(self):
        name = self.request.json['name']
        type = self.request.json['type']
        f = self.mgr.add_field(name, type)
        return dict(obj=f.serialize(), result='success')

    def delete(self):
        raise RuntimeError, "FIXME"
        id = int(self.request.matchdict['id'])
        self.mgr.delete_group(id)
        return dict(result='success')

@resource(collection_path='/rest/admin/layoutmodels',
          path='/rest/admin/layoutmodels/{id}',
          permission='admin')
class LayoutModelResource(BaseWebViewResource):
    dbmodel = SiteLayoutModel

    def collection_post(self):
        name = self.request.json['name']
        f = self.mgr.add_model(name)
        return dict(obj=f.serialize(), result='success')

    def delete(self):
        raise RuntimeError, "FIXME"
        id = int(self.request.matchdict['id'])
        self.mgr.delete_group(id)
        return dict(result='success')        

@resource(collection_path='/rest/admin/layoutmodels/{model_id}/fields',
          path='/rest/admin/layoutmodels/{model_id}/fields/{id}',
          permission='admin')
class LayoutModelFieldResource(BaseWebViewResource):
    dbmodel = SiteLayoutModelField

    def collection_post(self):
        model_id = int(self.request.matchdict['model_id'])
        if 'field_id' in self.request.POST:
            field_id = self.request.POST['field_id']
            content = None
        else:
            field_id = self.request.json['field_id']
            content = self.request.json['content']
        mf = self.mgr.attach_field_to_model(model_id, field_id, content)
        return dict(obj=mf.serialize(), result='success')

    def put(self):
        if 'content' in self.request.POST:
            content = self.request.POST['content']
        else:
            json = self.request.json
            content = json['content']
        model_id = int(self.request.matchdict['model_id'])
        field_id = int(self.request.matchdict['id'])
        mf = self.mgr.update_field_on_model(model_id, field_id, content)
        print model_id, field_id, "CONTENT IS", content
        return dict(obj=mf.serialize(), result='success')

    def get(self):
        model_id = int(self.request.matchdict['model_id'])
        field_id = int(self.request.matchdict['id'])
        mf = self.mgr.model_field_query().get((model_id, field_id))
        print "DB______CONTENT IS", mf.content
        return mf.serialize()
    
    
    def delete(self):
        model_id = int(self.request.matchdict['model_id'])
        field_id = int(self.request.matchdict['id'])
        self.mgr.detach_field_from_model(model_id, field_id)
        return dict(result='success')

    
    
        
        
    
        
@resource(collection_path='/rest/admin/webviews',
          path='/rest/admin/webviews/{id}',
          permission='admin')
class AdminWebViewResource(BaseWebViewResource):
    dbmodel = SiteWebview

    def collection_post(self):
        if 'model_id' in self.request.POST:
            model_id = self.request.POST['model_id']
            template_id = self.request.POST['template_id']
            name = self.request.POST['name']
        else:
            model_id = self.request.json['model_id']
            template_id = self.request.json['template_id']
            name = self.request.json['name']
        w = self.mgr.add_webview(name, model_id, template_id)
        return dict(obj=w.serialize(), result='success')

    def put(self):
        id = int(self.request.matchdict['id'])
        json = self.request.json
        if 'template' in json:
            template = json['template']
            w = self.mgr.update_webview(id, template=template)
            
    def get(self):
        id = int(self.request.matchdict['id'])
        w = self.mgr.webview_query().get(id)
        data = w.serialize()
        data['model'] = w.model.serialize()
        data['model']['fields'] = [f.serialize() for f in w.model.fields]
        data['template'] = w.template.serialize()
        return data

@resource(collection_path='/rest/admin/webview/{webview_id}/css',
          path='/rest/admin/webview/{webview_id}/css/{id}',
          permission='admin')
class AdminWebViewCSSResource(BaseWebViewResource):
    dbmodel = SiteWebviewCSS

    def collection_get(self):
        webview_id = int(self.request.matchdict['webview_id'])
        csslist = self.mgr.get_css_for_webview(webview_id)
        return dict(data=csslist)

    def collection_post(self):
        webview_id = int(self.request.matchdict['webview_id'])
        css_id = self.request.json['css_id']
        o = self.mgr.attach_css_to_webview(webview_id, css_id)
        return dict(obj=o.serialize(), result='success')
    
    
    
    def delete(self):
        webview_id = int(self.request.matchdict['webview_id'])
        css_id = int(self.request.matchdict['id'])
        self.mgr.detach_css(webview_id, css_id)
        return dict(result='success')


@resource(collection_path='/rest/admin/webview/{webview_id}/js',
          path='/rest/admin/webview/{webview_id}/js/{id}',
          permission='admin')
class AdminWebViewJSResource(BaseWebViewResource):
    dbmodel = SiteWebviewJS

    def collection_get(self):
        webview_id = int(self.request.matchdict['webview_id'])
        jslist = self.mgr.get_js_for_webview(webview_id)
        return dict(data=jslist)

    def collection_post(self):
        webview_id = int(self.request.matchdict['webview_id'])
        #js_id = int(self.request.matchdict['id'])
        js_id = self.request.json['js_id']
        o = self.mgr.attach_js_to_webview(webview_id, js_id)
        return dict(obj=o.serialize(), result='success')
    
    
    
    def delete(self):
        webview_id = int(self.request.matchdict['webview_id'])
        js_id = int(self.request.matchdict['id'])
        self.mgr.detach_js(webview_id, js_id)
        return dict(result='success')



@resource(collection_path='/rest/webviews',
          path='/rest/webviews/{name}',)
class WebViewResource(BaseWebViewResource):
    dbmodel = SiteWebview

    def collection_get(self):
        q = self.mgr.webview_query()
        q = q.filter_by(name='default')
        webview = q.one()
        data = webview.serialize()
        data['model'] = webview.model.serialize()
        fields = dict()
        model = webview.model
        for mf in model.fields:
            name = mf.field.name
            f = dict(type=mf.field.type, name=name, content=mf.content)
            fields[name] = f
            
        data['model']['fields'] = fields
        return data

        
    def get(self):
        name = self.request.matchdict['name']
        query = self.mgr.webview_query().filter_by(name=name)
        # need to handle errors here
        webview = query.one()
        data = webview.serialize()
        data['model'] = webview.model.serialize()
        fields = dict()
        model = webview.model
        for mf in model.fields:
            name = mf.field.name
            f = dict(type=mf.field.type, name=name, content=mf.content)
            fields[name] = f
        
        data['model']['fields'] = fields
        data['template'] = webview.template.serialize()
        return data

    
    
