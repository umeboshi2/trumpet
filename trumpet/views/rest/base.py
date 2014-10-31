import os
from datetime import datetime

import transaction
from cornice.resource import resource, view

from trumpet.models.usergroup import User

from trumpet.views.base import BaseUserView


def apiroot(prefix='/api', version='dev'):
    return os.path.join(prefix, version)


class BaseResource(BaseUserView):
    def __init__(self, request):
        super(BaseResource, self).__init__(request)
        self.db = self.request.db
        self.limit = None
        self.max_limit = 100
        
    def serialize_object(self, dbobj):
        return dbobj.serialize()

    def serialize_object_for_collection_query(self, dbobj):
        return self.serialize_object(dbobj)

    def collection_query(self):
        raise RuntimeError, "Implement me in subclass"

    def collection_get(self):
        offset = 0
        limit = self.limit
        GET = self.request.GET
        if 'offset' in GET:
            offset = int(GET['offset'])
        if 'limit' in GET:
            limit = int(GET['limit'])
            if limit > self.max_limit:
                limit = self.max_limit
        q = self.collection_query()
        total_count = q.count()
        q = q.offset(offset).limit(limit)
        objects = q.all()
        return dict(total_count=total_count,
                    data=[self.serialize_object_for_collection_query(o) for o in objects])
    

class BaseManagerResource(BaseResource):
    def get(self):
        id = self.request.matchdict['id']
        c = self.mgr.get(id)
        if c is None:
            # FIXME
            raise RuntimeError, "404"
        return dict(data=c.serialize(), result='success')
        
        
