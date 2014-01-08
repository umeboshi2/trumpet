define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    { User, Group } = require 'models'
    

    ########################################
    # Collections
    ########################################
    class BaseCollection extends Backbone.Collection
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
                
    class UserList extends BaseCollection
        model: User
        url: '/rest/users'

    class GroupList extends BaseCollection
        model: Group
        url: '/rest/groups'

    make_ug_collection = (user_id) ->
        class uglist extends BaseCollection
            model: Group
            url: '/rest/users/' + user_id + '/groups'
        return new uglist

    module.exports =
        UserList: UserList
        GroupList: GroupList
        make_ug_collection: make_ug_collection
    
    
