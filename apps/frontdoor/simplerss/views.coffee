define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'simplerss/templates'

  Models = require 'models'

  FormView = require 'common/form_view'
  
  
  class FeedEntryView extends Backbone.Marionette.ItemView
    template: Templates.rss_feed_entry

  class FeedListView extends Backbone.Marionette.CollectionView
    template: Templates.rss_feed_list
    itemView: FeedEntryView

  class FeedDataView extends Backbone.Marionette.ItemView
    template: Templates.viewfeed
    
  class NewFeedView extends FormView
    template: Templates.new_rss_feed

    ui:
      name: '[name="name"]'
      url: '[name="url"]'
      
    createModel: -> new Models.RssFeed

    updateModel: ->
      window.myUI = @ui
      @model.set
        name: @ui.name.val()
        url: @ui.url.val()
      console.log @model

    onSuccess: (model) ->
      Backbone.trigger 'rssfeed:create', model
      
      
  module.exports =
    FeedEntryView: FeedEntryView
    FeedListView: FeedListView
    FeedDataView: FeedDataView
    NewFeedView: NewFeedView
    
  
    