from configparser import ConfigParser
from io import StringIO

from cornice.resource import resource, view


from trumpet.models.usergroup import User, Group, Password
from trumpet.models.usergroup import UserGroup

from trumpet.managers.admin.users import UserManager

from trumpet.security import encrypt_password

from trumpet.views.rest.base import SimpleResource
    
# FIXME: this needs to be in manager
import transaction

class BaseUserResource(SimpleResource):
    def __init__(self, request):
        super(BaseUserResource, self).__init__(request)
        self.mgr = UserManager(self.db)
        
    

@resource(collection_path='/rest/users', path='/rest/users/{id}',
          permission='admin')
class UserResource(BaseUserResource):
    dbmodel = User

    def collection_get(self):
        get=None
        if self.request.GET:
            get=dict(self.request.GET)
        q = self.mgr.user_query()
        return dict(data=[o.serialize() for o in q], get=get)

    def collection_post(self):
        name = self.request.json['name']
        password = self.request.json['password']
        obj = self.mgr.add_user(name, password)
        data = dict(obj=obj.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_user(id)
        return dict(result='success')


@resource(collection_path='/rest/groups', path='/rest/groups/{id}',
          permission='admin')
class GroupResource(BaseUserResource):
    dbmodel = Group

    def collection_get(self):
        q = self.mgr.group_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        g = self.mgr.add_group(name)
        return dict(obj=g.serialize(), result='success')

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_group(id)
        return dict(result='success')

@resource(collection_path='/rest/users/{uid}/groups', path='/rest/users/{uid}/groups/{id}',
          permission='admin')
class UserGroupResource(BaseUserResource):
    dbmodel = UserGroup
    
    def collection_get(self):
        uid = int(self.request.matchdict['uid'])
        groups = self.mgr.list_groups_for_user(uid)
        data = [g.serialize() for g in groups]
        return dict(data=data)

    def collection_post(self):
        gid = self.request.json['id']
        uid = int(self.request.matchdict['id'])
        self.mgr.add_user_to_group(uid, gid)
        return dict(result='success')

    def delete(self):
        uid = int(self.request.matchdict['uid'])
        gid = int(self.request.matchdict['id'])
        self.mgr.remove_user_from_group(uid, gid)
        return dict(result='success')

    def get(self):
        gid = int(self.request.matchdict['id'])
        return dict(data=self.mgr.get_group(gid).serialize())
    
    
@resource(collection_path='/rest/groups/{gid}/members', path='/rest/groups/{gid}/members/{uid}',
          permission='admin')
class GroupMemberResource(BaseUserResource):
    dbmodel = UserGroup
    
    def collection_get(self):
        gid = int(self.request.matchdict['gid'])
        users = self.mgr.list_members_of_group(gid)
        data = [u.serialize() for u in users]
        return dict(data=data)

    

@resource(path='/rest/current/user')
class CurrentUserResource(BaseUserResource):
    dbmodel = None

    def get(self):
        user = self.get_current_user()
        if user is None:
            data = None
        else:
            data = user.serialize()
            data['groups'] = [g.serialize() for g in user.groups]
            data['config'] = None
            if user.config is not None:
                c = dict()
                config = user.config.get_config()
                for section in config.sections():
                    c[section] = dict()
                    for option in config.options(section):
                        c[section][option] = config.get(section, option)
                data['config'] = c
            else:
                import transaction
                with transaction.manager:
                    user.config.set_config('')
        return data
    
    
    def put(self):
        user = self.get_current_user()
        if user is None:
            raise RuntimeError
        config = self.request.json['config']
        c = ConfigParser()
        for section in config:
            c.add_section(section)
            for option in config[section]:
                c.add_option(option)
                c.set(section, option, config[section][option])
        user.set_config(c)
