define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'simplerss/views'
  Collections = require 'collections'
  

  class Controller extends Backbone.Marionette.Controller
    make_main_content: ->
      MSGBUS.events.trigger 'rcontent:close'
      @set_header 'Simple RSS'
      feeds = MSGBUS.reqres.request 'rss:feedlist'
      view = new Views.FeedListView
        collection: feeds
      response = feeds.fetch()
      response.done ->
        console.log 'feeds fetched'
      MSGBUS.events.trigger 'sidebar:show', view
          
    start: ->
      @feeds = MSGBUS.reqres.request 'rss:feedlist'
      @make_main_content()

    set_header: (title) ->
      header = $ '#header'
      header.text title
      header.append '<a class="btn btn-default btn-xs pull-left" href="#simplerss/addfeed">Add Feed</a>'
      
    show_feed: (feed_id) ->
      feed_data = MSGBUS.reqres.request 'rss:feeddata', feed_id
      response = feed_data.fetch()
      response.done =>
        view = new Views.FeedDataView
          model: feed_data
        MSGBUS.events.trigger 'rcontent:show', view
        @set_header feed_data.get('feed').title
        $('html, body').animate {scrollTop: 0}, 'fast'

    show_new_feed_form: () ->
      view = new Views.NewFeedView
      MSGBUS.events.trigger 'rcontent:show', view
      #header = $ '#header'
      #header.text 'Add New RSS Feed'
      #header.html ''
      @set_header 'Add New RSS Feed'

    show_edit_feed_form: () ->
      console.log 'show_edit_feed_form'
      MSGBUS.events.trigger 'rcontent:close'
      
    new_feed_added: (model) ->
      MSGBUS.events.trigger 'sidebar:close'
      feeds = MSGBUS.reqres.request 'rss:feedlist'
      view = new Views.FeedListView
        collection: feeds
      response = feeds.fetch()
      response.done ->
        console.log 'feeds fetched'
      MSGBUS.events.trigger 'sidebar:show', view
      MSGBUS.events.trigger 'rcontent:close'
      
              
  module.exports = Controller
  
