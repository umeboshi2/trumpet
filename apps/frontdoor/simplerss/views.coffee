define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'simplerss/templates'

  Models = require 'models'
  
  class FeedEntryView extends Backbone.Marionette.ItemView
    template: Templates.rss_feed_entry

  class FeedListView extends Backbone.Marionette.CollectionView
    template: Templates.rss_feed_list
    itemView: FeedEntryView

  class FeedDataView extends Backbone.Marionette.ItemView
    template: Templates.viewfeed
    
  class NewFeedView extends Backbone.Marionette.ItemView
    template: Templates.new_rss_feed
    model: new Models.RssFeed
    events:
      'submit form': 'onFormSubmit'

    onFormSubmit: (something) ->
      window.something = something
      console.log 'form submitted'
      
      
      
  module.exports =
    FeedEntryView: FeedEntryView
    FeedListView: FeedListView
    FeedDataView: FeedDataView
    NewFeedView: NewFeedView
    
  
    