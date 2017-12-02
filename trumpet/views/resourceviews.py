import os
from datetime import datetime

from sqlalchemy import func
import transaction
from cornice.resource import resource, view
from chert.alchemy import TimeStampMixin

def apiroot(prefix='/api', version='dev'):
    return os.path.join(prefix, version)

class BaseResource(object):
    def __init__(self, request, context=None):
        self.request = request
        self.db = self.request.dbsession
        self.limit = 25
        self.max_limit = 100
        self._use_pagination = True
        
    def serialize_object(self, dbobj):
        return dbobj.serialize()

    # use this when you do only need  certain model attributes
    # in a collection, rather than return the complete models
    def serialize_object_for_collection_query(self, dbobj):
        return self.serialize_object(dbobj)

    def collection_query(self):
        raise RuntimeError("Implement me in subclass")

    def _apply_pagination(self, query):
        offset = 0
        limit = self.limit
        GET = self.request.GET
        if 'offset' in GET:
            offset = int(GET['offset'])
        if 'limit' in GET:
            limit = int(GET['limit'])
            if limit > self.max_limit:
                limit = self.max_limit
        return query.offset(offset).limit(limit)
    
    def collection_get(self):
        q = self.collection_query()
        total_count = q.count()
        if self._use_pagination:
            q = self._apply_pagination(q)
        objects = q.all()
        data = [self.serialize_object_for_collection_query(o) for o in objects]
        return dict(total_count=total_count, items=data)
    
# /api/{model}/{id}
class SimpleModelResource(BaseResource):
    def __init__(self, request, context=None):
        super(SimpleModelResource, self).__init__(request, context=context)
        self.model = self.model_map.get(self.request.matchdict['model'])

    @property
    def model_map(self):
        raise NotImplementedError

    def _isTimeStampMixin(self):
        return isinstance(self.model(), TimeStampMixin)

    def collection_query(self):
        return self.db.query(self.model)
    
    def collection_post(self):
        with transaction.manager:
            m = self.model()
            for field in self.request.json:
                value = self.request.json[field]
                if type(value) is dict:
                    print("value of field {} is dict".format(field))
                setattr(m, field, value)
            # FIXME 
            if hasattr(m, 'user_id'):
                m.user_id = self.request.user.id
            self.db.add(m)
            self.db.flush()
        return self.serialize_object(m)

    def get(self):
        id = self.request.matchdict['id']
        m = self.db.query(self.model).get(id)
        if m is None:
            raise HTTPNotFound
        return self.serialize_object(m)

    
    def put(self):
        with transaction.manager:
            id = self.request.matchdict['id']
            m = self.db.query(self.model).get(id)
            if m is None:
                raise HTTPNotFound
            fields = set(self.request.json.keys())
            if self._isTimeStampMixin():
                fields.discard('created')
                fields.discard('updated')
            for field in fields:
                setattr(m, field, self.request.json[field])
            self.db.add(m)
            self.db.flush()
        return self.serialize_object(m)
    
    def delete(self):
        with transaction.manager:
            id = self.request.matchdict['id']
            m = self.db.query(self.model).get(id)
            if m is None:
                raise HTTPNotFound
            m.delete()
        
          
          
    
        
