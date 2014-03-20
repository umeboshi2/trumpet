define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  
  { User, Group } = require 'models'
  MSGBUS = require 'msgbus'
      

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

  MainUserList = new UserList
  MainGroupList = new GroupList

  make_ug_collection = (user_id) ->
    class uglist extends BaseCollection
      model Group
      url: '/rest/users/' + user_id + '/groups'
    return new uglist
    
  MSGBUS.reqres.setHandler 'useradmin:userlist', ->
    MainUserList
  MSGBUS.reqres.setHandler 'useradmin:grouplist', ->
    MainGroupList

            
  
  module.exports =
    MainUserList: MainUserList
    MainGroupList: MainGroupList
    make_ug_collection: make_ug_collection
    
    