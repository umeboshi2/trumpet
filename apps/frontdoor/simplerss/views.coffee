define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'simplerss/templates'

  class FeedEntryView extends Backbone.Marionette.ItemView
    template: Templates.rss_feed_entry

  class FeedListView extends Backbone.Marionette.CollectionView
    template: Templates.rss_feed_list
    itemView: FeedEntryView

  class FeedDataView extends Backbone.Marionette.ItemView
    template: Templates.viewfeed
    
  
  module.exports =
    FeedEntryView: FeedEntryView
    FeedListView: FeedListView
    FeedDataView: FeedDataView
    
  
    