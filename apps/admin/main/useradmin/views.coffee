define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'useradmin/templates'

  Models = require 'models'

  FormView = require 'common/form_view'
  
  
  class SideBarView extends Backbone.Marionette.ItemView
    template: Templates.useradmin_sidebar
      
  class BaseFeedView extends FormView
    ui:
      name: '[name="name"]'
      url: '[name="url"]'
      
    updateModel: ->
      @model.set
        name: @ui.name.val()
        url: @ui.url.val()
      #@model.save()
      
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
    
    
  
    