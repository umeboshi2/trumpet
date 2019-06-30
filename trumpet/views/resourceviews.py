import os
import types
from uuid import UUID
from datetime import datetime, date

import transaction
from pyramid.httpexceptions import HTTPNotFound
from querystring_parser import parser as qsparser
from hornstone.alchemy import TimeStampMixin


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
        # FIXME test this better
        if hasattr(dbobj, 'keys') and isinstance(dbobj.keys, types.MethodType):
            # FIXME we need to DRY this up and handle coverting
            # types to json compat in a single place
            data = dict()
            for key in dbobj.keys():
                value = getattr(dbobj, key)
                vtype = type(value)
                if vtype is UUID:
                    value = str(value)
                elif vtype in [datetime, date]:
                    value = value.isoformat()
                data[key] = value
            return data
        else:
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
        qs = qsparser.parse(self.request.query_string)
        if 'columns' in qs and '' in qs['columns'] and len(qs['columns']['']):
            _fields = (getattr(self.model, f) for f in qs['columns'][''])
            query = self.db.query(*_fields)
        else:
            query = self.collection_query()

        if 'distinct' in qs:
            # setup distinct and groupby
            raise RuntimeError("No support for distinct yet.")
        if 'where' in qs:
            # setup where clauses
            raise RuntimeError("No support for where yet.")

        q = query
        total_count = q.count()

        if self._use_pagination:
            q = self._apply_pagination(q)
        data = [self.serialize_object_for_collection_query(o) for o in q]
        return dict(total_count=total_count, items=data)


# from bookshelf-csapi
#
# req.query.withRelated - array of related models
# req.query.columns - array of columns
# req.query.where - where clause (two formats?)
# req.query.distinct - distinct values
# req.query.offset
# req.query.limit
# req.query.sort - only one column? always order by key unless present?
# req.query.direction - default is 'asc'
#
# if sort or offset is present set the direction
#
#
#
#

# BaseResource.model must be set in subclass
class BaseModelResource(BaseResource):
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
            self.db.delete(m)

    @property
    def model(self):
        raise NotImplementedError


class SimpleModelResource(BaseModelResource):
    """Handles /api/{model}[/{id}]"""
    @property
    def model(self):
        return self.model_map.get(self.request.matchdict['model'])

    @property
    def model_map(self):
        raise NotImplementedError
