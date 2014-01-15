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
      @set_header 'simplerss'
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
      header.append '<a class="action-button pull-right" href="#simplerss/addfeed">Add Feed</a>'
      
    show_feed: (feed_id) ->
      #@make_main_content()
      feed_data = MSGBUS.reqres.request 'rss:feeddata', feed_id
      window.feed_data = feed_data
      response = feed_data.fetch()
      response.done =>
        view = new Views.FeedDataView
          model: feed_data
        MSGBUS.events.trigger 'rcontent:show', view
        @set_header feed_data.get('feed').title
        $('html, body').animate {scrollTop: 0}, 'fast'
      
      
              
  module.exports = Controller
  
