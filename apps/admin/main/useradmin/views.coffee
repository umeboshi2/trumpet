define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'useradmin/templates'

  Models = require 'models'

  FormView = require 'common/form_view'
  
  
  class SideBarView extends Backbone.Marionette.ItemView
    template: Templates.useradmin_sidebar

    events:
      'click .listusers': 'list_users_pressed'
      'click .adduser': 'add_user_pressed'
      'click .listgroups': 'list_groups_pressed'
      'click .addgroup': 'add_group_pressed'
      
    _navigate: (url) ->
      r = new Backbone.Router
      r.navigate url, trigger:true
      
    list_users_pressed: () ->
      console.log 'list_users called'
      @_navigate '#useradmin/listusers'
      
    add_user_pressed: () ->
      console.log 'add_user called'
      @_navigate '#useradmin/adduser'
      
    list_groups_pressed: () ->
      console.log 'list_groups_pressed called'
      @_navigate '#useradmin/listgroups'

    add_group_pressed: () ->
      console.log 'add_group_pressed called'
      @_navigate '#useradmin/addgroup'

  class SimpleUserEntryView extends Backbone.Marionette.ItemView
    template: Templates.simple_user_entry

  class UserListView extends Backbone.Marionette.CompositeView
    template: Templates.simple_user_list
    itemView: SimpleUserEntryView
    className: 'listview-list'

  class SimpleGroupEntryView extends Backbone.Marionette.ItemView
    template: Templates.simple_group_entry

  class GroupListView extends Backbone.Marionette.CompositeView
    template: Templates.simple_group_list
    itemView: SimpleGroupEntryView
    className: 'listview-list'
    
  class NewUserFormView extends FormView
    ui:
      name: '[name="name"]'
      password: '[name="password"]'
      confirm: '[name="confirm"]'
      
    template: Templates.new_user_form

    createModel: ->
      new Models.User

    updateModel: ->
      @model.set
        name: @ui.name.val()
        password: @ui.password.val()
        confirm: @ui.confirm.val()
      users = MSGBUS.reqres.request 'useradmin:userlist'
      users.add @model

    onSuccess: (model) ->
      MSGBUS.events.trigger 'useradmin:event:user_added'
      
      
        
      
  class NewGroupFormView extends FormView
    template: Templates.new_group_form

    createModel: ->
      new Models.Group
      
  class BaseFeedView extends FormView
    ui:
      name: '[name="name"]'
      url: '[name="url"]'
      
    updateModel: ->
      @model.set
        name: @ui.name.val()
        url: @ui.url.val()
      #@model.save()

  class ViewUserView extends Backbone.Marionette.ItemView
    template: Templates.view_user_page
          
  class NewFeedView extends BaseFeedView
    template: Templates.new_rss_feed
      
    createModel: ->
      new Models.RssFeed

    onSuccess: (model) ->
      MSGBUS.commands.execute 'rssfeed:create', model
      
  class EditFeedView extends BaseFeedView
    template: Templates.edit_rss_feed

    createModel: ->
      @model
      
    onSuccess: (model) ->
      MSGBUS.commands.execute 'rssfeed:update', model
      
      
  module.exports =
    NewFeedView: NewFeedView
    EditFeedView: EditFeedView
    SideBarView: SideBarView
    SimpleUserEntryView: SimpleUserEntryView
    UserListView: UserListView
    SimpleGroupEntryView: SimpleGroupEntryView
    GroupListView: GroupListView
    NewUserFormView: NewUserFormView
    NewGroupFormView: NewGroupFormView
    ViewUserView: ViewUserView
    
    
    
  

